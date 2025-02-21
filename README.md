# PyProject
This repository contains a service for managing projects, users, and documents, designed to allow users to create, update, share, and delete project information, as well as manage project-related documents (e.g., .docx, .pdf).

**Technology Stack**
Backend: Python 3.10, FastAPI  
Database: PostgreSQL (with optional ORM: SQLAlchemy)  
File Storage: AWS S3
Serverless Functions: AWS Lambda (for image processing)  
Containerization: Docker  
CI/CD: GitHub Actions / GitLab CI for continuous integration and deployment



**Requirements**
Python 3.10
Docker (for containerization)  
AWS credentials for S3 and Lambda functions
Poetry (for dependency management)  

**Running Locally**  
Install dependencies:
$ poetry install  

Start the containers:
$make start-containers

Run the application:
$make run  

Access the API via http://localhost:<your_port>

