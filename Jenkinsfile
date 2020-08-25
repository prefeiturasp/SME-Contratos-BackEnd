pipeline {
    agent {
      node {
        label 'py-coad'
	  }
    }
    
    options {
      buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
      disableConcurrentBuilds()              
    }
    
    stages {
	  
      stage('CheckOut') {
        steps {
          checkout scm		
        }
      }
      
      stage('Analise Codigo') {
        when {
          branch 'develop'
        }
         steps {
           sh 'sonar-scanner \
                -Dsonar.projectKey=SME-Contratos-BackEnd \
                -Dsonar.sources=. \
                -Dsonar.exclusions=htmlcov \
                -Dsonar.host.url=http://sonar.sme.prefeitura.sp.gov.br \
                -Dsonar.login=1426bd14e5f9a2d6a3e5af46ba81d196b936e1ce \
                -Dsonar.language=py \
                -Dsonar.sourceEncoding=UTF-8'
         }
      }
      
      stage('Docker Build DEV') {
        when {
          branch 'develop'
        }
        steps {
           sh 'echo Deploying desenvolvimento'
           // Start JOB para build das imagens Docker e push SME Registry
      
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "d1b79a24-e2d3-47e4-936f-3bcc8970986f",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }

      stage('Deploy Dev') {
        when {
          branch 'develop'
        }
        steps {    
                
         //Start JOB para update de deploy Kubernetes 
         
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "819496ff-aaf3-480c-b871-ad0d1a1f3c54",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }
        
      stage('Docker Build HOM') {
        when {
          branch 'homolog'
        }
        steps {
          
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
                             
              //JOB DE BUILD
              jobId: "7c291d48-4b0a-4a6c-856c-d745afaeda9a",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }

      stage('Deploy HOM') {
        when {
          branch 'homolog'
        }
        steps {
          timeout(time: 24, unit: "HOURS") {
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\nBranch name: ${GIT_BRANCH}\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
          input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'ebufaino, marcos_nastri, calvin_rossinhole, kelwy_oliveira'
          }    
                
       //Start JOB Rundeck para update de imagens no host homologação 
         
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "87787c11-4511-4e65-aaf6-b3ae1117980c",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }
      
      stage('Docker Build PROD') {
        when {
          branch 'master'
        }
        steps {
          
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
                             
              //JOB DE BUILD
              jobId: "97a55759-175f-4c1c-b4c3-8923e69bc357",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }

      stage('Deploy Prod') {
        when {
          branch 'master'
        }
        steps {
          timeout(time: 24, unit: "HOURS") {
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\nBranch name: ${GIT_BRANCH}\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
          input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'ebufaino, marcos_nastri, calvin_rossinhole, kelwy_oliveira'
          }    
                
       //Start JOB Rundeck para update de imagens no host homologação 
         
          script {
            step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
              jobId: "83c351fd-c566-4ec2-b313-f18c3e53eafe",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
          }
        }
      }

    }

post {
        always {
          echo 'One way or another, I have finished'
        }
        success {
	  	    step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Esta ok !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n\n Uma nova versão da aplicação esta disponivel!!!")
        }
        unstable {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("O Build ${BUILD_DISPLAY_NAME} <${env.BUILD_URL}> - Esta instavel ...\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        failure {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME}  - Quebrou. \nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        changed {
          echo 'Things were different before...'
        }
        aborted {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("O Build ${BUILD_DISPLAY_NAME} - Foi abortado.\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
    }
}
