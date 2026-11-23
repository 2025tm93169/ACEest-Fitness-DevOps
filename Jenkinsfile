
pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'maneshborkar13/aceest-fitness'
        SONARQUBE_SERVER = 'SonarQube'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest-cov
                '''
            }
        }

        stage('Syntax Check') {
            steps {
                sh '.venv/bin/python -m compileall -q app.py tests'
            }
        }

        stage('Lint') {
            steps {
                sh '.venv/bin/python -m flake8 app.py tests'
            }
        }

        stage('Run Tests and Coverage') {
            steps {
                sh '''
                    .venv/bin/python -m pytest \
                      --cov=app \
                      --cov-report=xml:coverage.xml \
                      --cov-report=term
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'coverage.xml',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t ${DOCKERHUB_REPO}:${BUILD_NUMBER} \
                      -t ${DOCKERHUB_REPO}:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                          -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_REPO}:latest

                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'ACEest CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'ACEest CI/CD pipeline failed. Check the stage logs.'
        }
        always {
            echo 'ACEest Jenkins build finished.'
        }
    }
}
