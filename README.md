## File Converter App

A lightweight Flask-based image file converter that allows users to upload and convert image files (PNG, JPEG, PDF) using a simple web UI. The application is containerized with Docker, integrated into a Jenkins CI/CD pipeline, and deployed to AWS EC2 via Terraform.


## Features

- Upload and convert image files (PNG, JPEG, PDF)
- Simple, responsive HTML interface
- Image conversion using Python's Pillow library
- Dockerized for consistent deployment
- CI/CD automation with Jenkins
- Hosted on AWS EC2, provisioned using Terraform


## Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Cloud**: AWS EC2
- **IaC**: Terraform
- **Registry**: Docker Hub


## CI/CD Pipeline

1. Code is pushed to GitHub.
2. Jenkins automatically:
   - Clones the repository
   - Builds a Docker image from the Flask app
   - Pushes the image to Docker Hub
   - SSHs into the EC2 instance provisioned via Terraform
   - Runs the container on port 5000


## Infrastructure Setup (Terraform)

Terraform provisions:

- A VPC with public subnets
- Internet gateway and routing
- Security groups (allowing ports 22 & 5000)
- EC2 Launch Template with Docker installed via user_data
- Auto Scaling Group with 2 instances

EC2 user_data script (bootstrap Docker):

```bash
#!/bin/bash
apt-get update -y
apt-get install -y docker.io
systemctl start docker
usermod -aG docker ubuntu
```


## Docker Usage

Build and run locally:

```bash
docker build -t file-converter-app .
docker run -d -p 5000:5000 file-converter-app
```


## Accessing the App

Once deployed via Jenkins, visit:

```
http://<EC2_PUBLIC_IP>:5000
```

Upload an image, select an output format, and download your converted file.


## Sample Jenkinsfile

```groovy
pipeline {
  agent any
  stages {
    stage('Build & Push Docker Image') {
      steps {
        script {
          def imageName = "ngozin/file-converter-app"
          docker.build(imageName)
          docker.withRegistry('https://index.docker.io/v1/', 'docker-hub') {
            sh "docker push ${imageName}"
          }
        }
      }
    }
    stage('Deploy to EC2') {
      steps {
        sshagent(['ec2-key']) {
          sh '''
            ssh -o StrictHostKeyChecking=no ubuntu@<EC2_PUBLIC_IP> "
              docker pull ngozin/file-converter-app:latest &&
              docker stop file-converter || true &&
              docker rm file-converter || true &&
              docker run -d -p 5000:5000 --name file-converter ngozin/file-converter-app:latest
            "
          '''
        }
      }
    }
  }
}
```

## Security Notes

- Ensure your `.pem` private key is stored securely.
- Use Docker Hub tokens instead of passwords in Jenkins.
- Limit open ports in the security group to only what's necessary (22 & 5000).


## Author

**Ngozi Nwadialo**  
Cloud DevOps Engineer  
[LinkedIn](https://linkedin.com/in/ngozi-nwadialo) | [GitHub](https://github.com/Ngozi-N)
