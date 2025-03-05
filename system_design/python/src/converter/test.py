from convert import converter
import glob
import tempfile
import os

if __name__ == "__main__":
    pdf_list = [f for f in glob.glob(os.path.join("uploads", "*.pdf"))]
    print(pdf_list)
    con = converter.Converter()
    for pdf in pdf_list:
        file_name = os.path.basename(pdf)
        temp_file = tempfile.TemporaryDirectory()
        con.pdf_to_img(pdf, temp_file.name + os.path.sep)
        con.img_to_pdf(temp_file.name + os.path.sep, './', file_name)
        # os.remove(pdf)
        
        
# if __name__ == '__main__':
#     con = Converter()
#     pdf_list = [f for f in glob.glob("./uploads/*.pdf")]
#     if len(pdf_list)==0:
#         print('There is no given PDF Files under uploads, skipping operation...')
#         sys.exit(0)
#     for pdf in pdf_list:
#         file_name = pdf.split('./uploads/')[1]
#         temp_file = tempfile.TemporaryDirectory()
#         con.pdf_to_img(pdf, temp_file.name + '/')
#         con.img_to_pdf(temp_file.name + '/', './', file_name)
#         os.remove(pdf)
