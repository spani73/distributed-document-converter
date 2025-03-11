## Overview
This project addresses the issue of blue light exposure from reading PDFs with white backgrounds for extended periods, which can lead to discomfort and even insomnia. Dark PDF converts these documents to a dark background with white text, enhancing readability and reducing eye strain.

## Key Features
* Scalable Architecture: Built using event-driven and microservice architectures, ensuring high scalability and robustness.

* Containerization and Deployment: Utilizes Docker for containerization and Kubernetes for deployment, ensuring efficient resource management.

# Data Storage:

* MongoDB and GridFS: Used for storing original documents and converted dark PDFs, providing efficient storage and retrieval.

* MySQL: Handles user authentication data securely.

* Decoupling and Scalability: RabbitMQ is used to decouple the converter from the gateway, allowing both components to scale independently.

* Security and Authentication: Employs JWT tokens for secure user authentication.

* Conversion Technology: Leverages advanced image processing algorithms to convert white background PDFs to dark background with white text.

# Technical Highlights
* Event-Driven Architecture: Ensures asynchronous processing and efficient handling of document conversions.

* Microservices: Each service is designed to be modular and independently scalable.

* Container Orchestration: Kubernetes manages and automates deployment, scaling, and maintenance of containers.

# Getting Started
To contribute or deploy this project, follow these steps:

Clone the Repository: Clone this repository to your local machine.

Setup Environment: Ensure Docker, Kubernetes, MongoDB, MySQL, and RabbitMQ are installed.

Build and Deploy: Use Docker to build images and Kubernetes to deploy the microservices.

Feel free to add more details or sections as needed, such as installation instructions, contributing guidelines, or FAQs.
