pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Dependencias') {
            steps {
                sh 'python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt'
            }
        }

        stage('Testes') {
            steps {
                sh '.venv/bin/python run_tests.py'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                    archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/**'
                    sh '''
                        if [ -d /var/relatorios ]; then
                            mkdir -p "/var/relatorios/build-$BUILD_NUMBER" /var/relatorios/ultimo
                            cp -r reports/. "/var/relatorios/build-$BUILD_NUMBER/"
                            rm -rf /var/relatorios/ultimo/*
                            cp -r reports/. /var/relatorios/ultimo/
                        fi
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                sh '''
                    mkdir -p dist
                    tar czf "dist/restful-booker-tests-$BUILD_NUMBER.tar.gz" \
                        conftest.py pytest.ini requirements.txt run_tests.py data tests utils
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }
    }
}
