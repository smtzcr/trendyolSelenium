pipeline {
    agent any
    
    environment {
        CHROME_HEADLESS = 'true'
    }

    stages {
        stage('Install Python') {
            steps {
                echo 'Python Portable kuruluyor...'
                bat '''
                    if not exist python-portable (
                        echo Python Portable indiriliyor...
                        curl -L -o python-embed.zip https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
                        powershell -Command "Expand-Archive -Path python-embed.zip -DestinationPath python-portable -Force"

                        echo get-pip.py indiriliyor...
                        curl -L -o python-portable\\get-pip.py https://bootstrap.pypa.io/get-pip.py

                        echo pip kuruluyor...
                        python-portable\\python.exe python-portable\\get-pip.py

                        echo pth dosyası düzenleniyor...
                        echo import site >> python-portable\\python311._pth
                    )
                '''
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Environment hazırlanıyor...'
                bat '''
                    python-portable\\python.exe --version
                    python-portable\\python.exe -m pip --version
                    python-portable\\python.exe -m pip install selenium webdriver-manager requests
                    if not exist reports mkdir reports
                    if not exist screenshots mkdir screenshots
                    if not exist logs mkdir logs
                '''
            }
        }

        stage('Run Tests') {
            parallel {
                stage('Home Page Tests') {
                    steps {
                        bat '''
                            set PYTHONPATH=%CD%
                            python-portable\\python.exe -m unittest tests.test_home_page -v
                        '''
                    }
                }
                stage('Search Tests') {
                    steps {
                        bat '''
                            set PYTHONPATH=%CD%
                            python-portable\\python.exe -m unittest tests.test_search_basic -v
                        '''
                    }
                }
            }
        }

        stage('Generate Reports') {
            steps {
                echo 'Raporlar oluşturuluyor...'
                bat '''
                    set PYTHONPATH=%CD%
                    python-portable\\python.exe run_tests.py --report-only
                '''
            }
        }

        stage('Publish Results') {
            steps {
                archiveArtifacts artifacts: 'reports/*.*, screenshots/*.png, logs/*.log', allowEmptyArchive: true

                script {
                    try {
                        publishHTML([
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'reports',
                            reportFiles: '*.html',
                            reportName: 'Test Report'
                        ])
                    } catch (Exception e) {
                        echo "HTML publishing: ${e.getMessage()}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline tamamlandı'
        }

        success {
            echo '✅ Tüm testler başarılı!'
        }

        failure {
            echo '❌ Pipeline başarısız!'
        }

        unstable {
            echo '⚠️ Bazı testler başarısız!'
        }
    }
}