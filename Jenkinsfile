pipeline {
    agent any
    
    environment {
        PYTHON_PATH = 'python'
        CHROME_HEADLESS = 'true'
    }
    
    triggers {
        // Her commit'te çalıştır
        pollSCM('H/5 * * * *')
        
        // GitHub webhook
        githubPush()
        
        // Günlük çalıştır (gece 2'de)
        cron('0 2 * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Code checkout edildi'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Environment hazırlanıyor...'
                bat '''
                    python --version
                    pip install -r requirements.txt
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
                        bat 'python -m unittest tests.test_home_page -v'
                    }
                }
                stage('Search Tests') {
                    steps {
                        bat 'python -m unittest tests.test_search_basic -v'
                    }
                }
                stage('Login Tests') {
                    steps {
                        bat 'python -m unittest tests.test_login -v'
                    }
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo 'Raporlar oluşturuluyor...'
                bat 'python run_tests.py --report-only'
            }
        }
        
        stage('Publish Results') {
            steps {
                // HTML raporunu yayınla
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: '*.html',
                    reportName: 'Test Report'
                ])
                
                // Artifacts'ı arşivle
                archiveArtifacts artifacts: 'reports/*.*, screenshots/*.png, logs/*.log', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline tamamlandı'
            
            // Email bildirimi
            script {
                def testResults = readJSON file: 'reports/latest_test_results.json'
                def successRate = testResults.success_rate
                
                if (successRate < 80) {
                    emailext (
                        subject: "❌ Test Pipeline Failed - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """
                        Test pipeline başarısız oldu!
                        
                        Başarı Oranı: ${successRate}%
                        Build: ${env.BUILD_URL}
                        
                        Detaylar için Jenkins'e bakın.
                        """,
                        to: "smettommer@gmail.com"
                    )
                }
            }
        }
        
        success {
            echo '✅ Tüm testler başarılı!'
        }
        
        failure {
            echo '❌ Pipeline başarısız!'
        }
    }
}