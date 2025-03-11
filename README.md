# Overview
This project addresses the issue of blue light exposure from reading PDFs with white backgrounds for extended periods, which can lead to discomfort and even insomnia. Dark PDF converts these documents to a dark background with white text, enhancing readability and reducing eye strain.

# Key Features
* Scalable Architecture: Built using event-driven and microservice architectures, ensuring high scalability and robustness.

* Containerization and Deployment: Utilizes Docker for containerization and Kubernetes for deployment, ensuring efficient resource management.

## Data Storage:

* MongoDB and GridFS: Used for storing original documents and converted dark PDFs, providing efficient storage and retrieval.

* MySQL: Handles user authentication data securely.

* Decoupling and Scalability: RabbitMQ is used to decouple the converter from the gateway, allowing both components to scale independently.

* Security and Authentication: Employs JWT tokens for secure user authentication.

* Conversion Technology: Leverages advanced image processing algorithms to convert white background PDFs to dark background with white text.

## Technical Highlights
* Event-Driven Architecture: Ensures asynchronous processing and efficient handling of document conversions.

* Microservices: Each service is designed to be modular and independently scalable.

* Container Orchestration: Kubernetes manages and automates deployment, scaling, and maintenance of containers.

## Demo

### Kubernetes Deployed Instances : 
![Kubernetes Pods](https://github.com/user-attachments/assets/aeadd9f3-37b0-4123-8968-aa869a850857)

### Auth Endpoint Response with JWT Token : 
![Auth Endpoint Response](https://github.com/user-attachments/assets/9cf28031-a141-4ab5-ae96-377b694fca33)

### Document Before Conversion With White Background and Black Text :
![Document Before Conversion](https://github.com/user-attachments/assets/2ae70b0c-2d25-49cc-bb9c-129a062141ee)

### Upload Endpoint Call with JWT Token and Document in Body :
![Upload Endpoint Response](https://github.com/user-attachments/assets/1b4fc617-a02a-4a58-86d8-665ac0fdaedd)

### Email Notification Once Conversion is Completed :
![Email Notification once the conversion is completed](https://github.com/user-attachments/assets/087520cd-0967-42e9-a398-2cba1cfb81c0)

### Download Endpoint To Receive the Converted Document : 
![Download Endpoint response with converted pdf](https://github.com/user-attachments/assets/cf86ca4e-f9d4-446c-a6cf-fa279997c4e7)




# Getting Started
To contribute or deploy this project, follow these steps:

Clone the Repository: Clone this repository to your local machine.

Setup Environment: Ensure Docker, Kubernetes, MongoDB, MySQL, and RabbitMQ are installed.

Build and Deploy: Use Docker to build images and Kubernetes to deploy the microservices.

Feel free to add more details or sections as needed, such as installation instructions, contributing guidelines, or FAQs.
