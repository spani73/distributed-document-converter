import pika.spec
import cv2
import re
import tempfile
from fpdf import FPDF
from PIL import Image
import glob
import os
import sys
import fitz  # Import PyMuPDF
import pika, json
from bson.objectid import ObjectId

class Converter:
    """
        Converts PDF Files to Image
        Inverts Image
        Reconvert to PDF and Combine
    """

    def invert_image(self, i_input, i_output):
        """
        :param i_input: image to be inverted
        :param i_output: output image
        """
        image = cv2.imread(i_input)
        print('Inverting image: {}'.format(i_input))
        print(image)
        image = ~(image)
        print(image)
        cv2.imwrite(i_output, image)

    def pdf_to_img(self, file_path, o_dir):
        """
        :param file_path: input PDF file path
        :param o_dir: output directory
        """
        doc = fitz.open(file_path)
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap()
            output = os.path.join(o_dir, f"{i}.png")  # Save as PNG
            pix.pil_save(output)

    def img_to_pdf(self, i_dir, o_dir, file_temp_path):
        """
        :param i_dir: images directory
        :param o_dir: output directory
        """
        imgtopdf = FPDF()
        images = []
        for filepath in glob.iglob(os.path.join(i_dir, '*.png')):  # Look for PNG files
            print('Inverting the images: {}'.format(filepath))
            self.invert_image(filepath, filepath)
            images.append(filepath)

        images = [int(re.findall(r'\d+.png', i)[0].split('.png')[0]) for i in images]
        images.sort()

        for i in images:
            img = os.path.join(i_dir, f"{i}.png")
            print('Converting images to PDF files: {}'.format(img))
            cover = Image.open(img)
            width, height = cover.size

            # Use A4 size directly for simplicity
            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

            # Determine orientation based on image size
            orientation = 'P' if height > width else 'L'

            # Add page with correct orientation
            imgtopdf.add_page(orientation=orientation)

            # Scale image to fit page while maintaining aspect ratio
            scale = min(pdf_size[orientation]['w'] / width, pdf_size[orientation]['h'] / height)
            scaled_width = width * scale
            scaled_height = height * scale

            # Calculate position to center the image
            x = (pdf_size[orientation]['w'] - scaled_width) / 2
            y = (pdf_size[orientation]['h'] - scaled_height) / 2

            imgtopdf.image(img, x, y, scaled_width, scaled_height)

        print('Generating combined PDF file {}'.format(file_temp_path))
        imgtopdf.output(file_temp_path, 'F')

    def clean_up(self, dir):
        """
        :param dir:
        """
        file_list = glob.glob(os.path.join(dir, "*.pdf"))
        for f in file_list:
            os.remove(f)

con = Converter()

def start(message, fs_uploads, fs_downloads, ch):
    message = json.loads(message)
    
    # create empty tempfile.
    tf = tempfile.NamedTemporaryFile()
    td = tempfile.TemporaryDirectory()
    
    # uploaded doc
    doc = fs_uploads.get(ObjectId(message['upload_fid']))
    # add contents to tempfile
    tf.write(doc.read())
    
    
    # create images from pdf
    con.pdf_to_img(tf.name, td.name + os.path.sep)
    tf.close()
    
    # write doc to the file
    tf_path = os.path.join(tempfile.gettempdir(), f"{message['upload_fid']}.pdf")
    con.img_to_pdf(td.name + os.path.sep, './', tf_path)
    
    # save the file to mongodb
    with open(tf_path, 'rb') as f:
        data = f.read()
        fid = fs_downloads.put(data)
    
    os.remove(tf_path)
    
    message['download_fid'] = str(fid)
    try:
        ch.basic_publish(
            exchange='',
            routing_key=os.environ.get('DOWNLOAD_QUEUE'),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE, 
            ),
        )
    except Exception as e:
        fs_downloads.delete(fid)
        print(e)
        return "failed to publish message"