pipeline {
    agent any

    environment {
        DOCKER_USER = "gokumonkey"
        TOKEN = "dckr_pat_vHMjHr6LEPU-5_bZln8EdQf_HzY"
        IMAGE_NAME = "backend"
        DOCKER_SERVER = "ubuntu@65.1.3.254"
    }

    stages {

        stage('Source') {
            steps {
                git branch: 'main',
                url: 'https://github.com/gokumonkey-36/backend.git'
            }
        }

        stage('Dependency Verification'){
            steps{
                sh ''' 
                python3 pip install -r requirements.txt 
                '''
            }
        }

        stage ('Syntax Check'){
            steps{
                sh ''' 
            python -m compileall .
            '''
            }
            
        }

        stage('Lint'){
            steps{
                sh ''' ruff check . 
                '''
            }
            
        }

        stage('Unit Test'){
            steps{
                sh ''' pytest 
                '''
            }
            
        }

        stage('Build Image') {
            steps {
                sh '''
                ssh ${DOCKER_SERVER} "
                    mkdir -p ~/backend
                "

                scp -r ./* ${DOCKER_SERVER}:~/backend/

                ssh ${DOCKER_SERVER} "
                    cd ~/backend &&
                    docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER} .
                   
                "
                '''
            }
        }

        stage('Scan Image'){
            steps{
                sh ''' ssh ${DOCKER_SERVER} "
                trivy image --severity CRITICAL,HIGH --exit-code 1 gokumonkey/backend:${BUILD_NUMBER}  "
                '''
            }
            
        }

        stage('Push Docker Image'){
            steps{
                sh '''
            ssh ${DOCKER_SERVER} "
             docker login -u ${DOCKER_USER} -p ${TOKEN} &&
             docker push ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
            "
            '''
            }
            
        }
        stage('Deploy') {
            steps {
                sh '''
                ssh ${DOCKER_SERVER} "
                    cd ~/backend &&

                    kubectl apply -f deployment.yaml
                "
                '''
            }
        }

        stage('Integration Test') {
            steps {
                echo 'Integration tests will be added later'
            }
        }
    }
}
