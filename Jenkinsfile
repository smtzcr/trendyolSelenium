pipeline {
    agent any
    
    environment {
        CHROME_HEADLESS = 'true'
    }

    stages {
        stage('Install Python') {
            steps {
                echo 'Python kuruluyor...'
                bat '''
                    if not exist python-portable (
                        echo Python Portable indiriliyor...
                        curl -L -o python.zip https://github.com/winpython/winpython/releases/download/4.8.20221024/Winpython64-3.10.8.0dot.exe

                        REM Alternatif basit yöntem
                        curl -L -o python-embed.zip https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
                        powershell -Command "Expand-Archive -Path python-embed.zip -DestinationPath python-portable -Force"

                        REM get-pip.py indir
                        curl -L -o python-portable\\get-pip.py https://bootstrap.pypa.io/get-pip.py

                        REM pip kur
                        python-portable\\python.exe python-portable\\get-pip.py
                    )
                '''
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Environment hazırlanıyor...'
                bat '''
                    python-portable\\python.exe --version
                    python-portable\\python.exe -m pip install selenium webdriver-manager requests
                    if not exist reports mkdir reports
                    if not exist screenshots mkdir screenshots
                    if not exist logs mkdir logs
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    python-portable\\python.exe -m unittest tests.test_home_page -v
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline tamamlandı'
            archiveArtifacts artifacts: 'reports/*.*, screenshots/*.png, logs/*.log', allowEmptyArchive: true
        }

        failure {
            echo '❌ Pipeline başarısız!'
        }
    }
}