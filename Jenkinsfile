pipeline {
    agent any
    stages {
        // WebHook에서 감지된 변경 코드를 clone 해서 가져오기
        stage('Prepare') {
            steps {
                sh 'echo "Clone Repository"'
                git branch: 'back/feat63-jenkinstest',
                    url: 'https://lab.ssafy.com/s09-mobility-smarthome-sub2/S09P22B201.git',
                    credentialsId: '69daef35-2872-44f4-8e64-396a1a04dc02'
            }
            post {
                success {
                    sh 'echo "Successfully Cloned Repository"'
                }
                failure {
                    sh 'echo "Failed in Cloning Repository"'
                }
            }
        } 

        stage('Docker container delete') {
            steps {
                script {
                    def containerNames = ['back', 'front']

                    for (String containerName in containerNames) {
                        sh "docker stop ${containerName}"
                        sh "docker rm ${containerName}"
                    }
                }
            }
        }

        stage('Docker image delete') {
            steps {
                script {
                    def imageNames = ['backend-ssak3', 'frontend-ssak3']

                    for (String imageName in imageNames) {
                        sh "docker rmi ${imageName}"
                    }
                }
            }
        }

        stage('Deploy with Docker-Compose') {
            steps {
                script {
                    // sh "echo $pwd"
                    // 권한 설정 해야함
                    sh "cd /jenkins/workspace/ssak3@2"
                    sh "cd /home/ubuntu/S09P22B201"
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}
