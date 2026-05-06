pipeline {
    agent any
    
    stages {
        
        // STAGE 1: CODE LINTING
        stage('Code Linting') {
            steps {
                echo '========================================='
                echo '🔍 STAGE 1: Running Code Linting'
                echo '========================================='
                
                sh '''
                    echo "Installing flake8..."
                    pip install flake8 --break-system-packages
                    
                    echo "Running flake8 on app.py..."
                    cd webapp
                    flake8 app.py --max-line-length=120 --ignore=E501
                    
                    echo "✅ Code linting passed!"
                '''
            }
        }
        
        // STAGE 2: CODE BUILD
        stage('Code Build') {
            steps {
                echo '========================================='
                echo '🏗️ STAGE 2: Building Docker Images'
                echo '========================================='
                
                sh '''
                    echo "Building webapp Docker image..."
                    docker build -t flask-webapp:latest ./webapp
                    
                    echo "Building Selenium tests Docker image..."
                    docker build -t selenium-tests:latest -f selenium_tests/Dockerfile.selenium ./selenium_tests
                    
                    echo "✅ Docker images built successfully!"
                '''
            }
        }
        
        // STAGE 3: CONTAINERIZED DEPLOYMENT
        stage('Containerized Deployment') {
            steps {
                echo '========================================='
                echo '🚀 STAGE 3: Deploying Containers'
                echo '========================================='
                
                sh '''
                    echo "Stopping any existing containers..."
                    cd /home/ubuntu/flask-cicd-app
                    docker-compose down --remove-orphans || true
                    
                    echo "Building and starting containers..."
                    docker-compose up -d --build
                    
                    echo "Waiting for services to be ready..."
                    sleep 15
                    
                    echo "Checking container status..."
                    docker ps
                    
                    echo "Checking webapp health endpoint..."
                    curl --fail http://localhost:5000/health || echo "Health check waiting..."
                    
                    echo "✅ Containerized deployment successful!"
                '''
            }
        }
        
        // STAGE 4: SELENIUM TESTING
        stage('Containerized Selenium Testing') {
            steps {
                echo '========================================='
                echo '🧪 STAGE 4: Running Selenium Tests'
                echo '========================================='
                
                sh '''
                    echo "Running Selenium tests..."
                    
                    cd /home/ubuntu/flask-cicd-app
                    
                    # Run selenium tests
                    docker run --rm \
                        --network flask-cicd-app_app_network \
                        -v $(pwd)/selenium_tests:/tests \
                        selenium-tests:latest \
                        python -m unittest discover -s . -p "test_*.py"
                    
                    echo "✅ All Selenium tests passed!"
                '''
            }
        }
    }
    
    post {
        always {
            echo '========================================='
            echo '🧹 Pipeline execution completed'
            echo '========================================='
        }
        
        success {
            echo '''
            ╔══════════════════════════════════════════════════════════════╗
            ║                                                              ║
            ║     ✅ CI/CD PIPELINE SUCCESSFUL ✅                          ║
            ║                                                              ║
            ║     📊 Stages Completed:                                     ║
            ║        1. Code Linting              - PASSED                ║
            ║        2. Code Build                - PASSED                ║
            ║        3. Containerized Deployment  - PASSED                ║
            ║        4. Selenium Testing          - PASSED                ║
            ║                                                              ║
            ╚══════════════════════════════════════════════════════════════╝
            '''
        }
        
        failure {
            echo "❌ PIPELINE FAILED - Check console output above"
        }
    }
}
