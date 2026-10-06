pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv && .venv/bin/pip install -r requirements.txt'
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

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest -q'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-fitness:jenkins-build .'
            }
        }
    }

    post {
        always {
            echo 'ACEest Jenkins build completed.'
        }
    }
}
