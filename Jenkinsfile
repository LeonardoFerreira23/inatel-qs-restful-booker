pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        PYTHON_VERSION = '3.12.10'
    }

    stages {

        stage('Dependencias') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            set -eu

                            echo "Verificando Python..."
                            python3 --version

                            python3 -c "import sys; sys.exit(0 if sys.version_info[:3] == (3, 12, 10) else 1)"

                            echo "Criando ambiente virtual..."
                            python3 -m venv .venv

                            echo "Atualizando pip..."
                            .venv/bin/python -m pip install --upgrade pip

                            echo "Instalando dependencias..."
                            .venv/bin/python -m pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            @echo off

                            echo Verificando Python...
                            python --version

                            python -c "import sys; sys.exit(0 if sys.version_info[:3] == (3, 12, 10) else 1)"
                            if errorlevel 1 exit /b 1

                            echo Criando ambiente virtual...
                            python -m venv .venv
                            if errorlevel 1 exit /b 1

                            echo Atualizando pip...
                            .venv\\Scripts\\python.exe -m pip install --upgrade pip
                            if errorlevel 1 exit /b 1

                            echo Instalando dependencias...
                            .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                            if errorlevel 1 exit /b 1
                        '''
                    }
                }
            }
        }

        stage('Testes') {
            steps {
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python run_tests.py'
                    } else {
                        bat '.venv\\Scripts\\python.exe run_tests.py'
                    }
                }
            }

            post {
                always {
                    junit(
                        allowEmptyResults: true,
                        testResults: 'reports/junit.xml'
                    )

                    archiveArtifacts(
                        allowEmptyArchive: true,
                        artifacts: 'reports/**'
                    )
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python scripts/package_project.py'
                    } else {
                        bat '.venv\\Scripts\\python.exe scripts\\package_project.py'
                    }
                }

                archiveArtifacts(
                    artifacts: 'dist/*.tar.gz',
                    fingerprint: true
                )
            }
        }
    }

    post {

        success {
            script {
                echo 'Pipeline finalizado com sucesso. Enviando notificacao...'

                def status

                if (isUnix()) {
                    status = sh(
                        returnStatus: true,
                        script: 'python3 scripts/send_email.py SUCCESS'
                    )
                } else {
                    status = bat(
                        returnStatus: true,
                        script: 'python scripts\\send_email.py SUCCESS'
                    )
                }

                if (status != 0) {
                    echo 'AVISO: nao foi possivel enviar o e-mail de sucesso.'
                } else {
                    echo 'Notificacao de sucesso enviada ao servidor SMTP.'
                }
            }
        }

        failure {
            script {
                echo 'Pipeline finalizado com falha. Enviando notificacao...'

                def status

                if (isUnix()) {
                    status = sh(
                        returnStatus: true,
                        script: 'python3 scripts/send_email.py FAILURE'
                    )
                } else {
                    status = bat(
                        returnStatus: true,
                        script: 'python scripts\\send_email.py FAILURE'
                    )
                }

                if (status != 0) {
                    echo 'AVISO: nao foi possivel enviar o e-mail de falha.'
                } else {
                    echo 'Notificacao de falha enviada ao servidor SMTP.'
                }
            }
        }
    }
}
```