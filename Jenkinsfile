pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Ngozi-N/file-converter-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("file-converter-app:${env.BUILD_ID}")
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['ec2-key']) {
                    sh 'scp -o StrictHostKeyChecking=no docker-compose.yml ec2-user@YOUR_EC2_IP:/home/ec2-user/'
                    sh 'ssh ec2-user@YOUR_EC2_IP "docker-compose down && docker-compose up -d"'
                }
            }
        }
    }
}
