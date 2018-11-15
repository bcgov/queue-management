// This Jenkins build requires a configmap called jenkin-config with the following in it:
//
// password_qtxn=<cfms-postman-operator userid password>
// password_nonqtxn=<cfms-postman-non-operator userid password>
// client_secret=<keycloak client secret>
// zap_with_url=<zap command including dev url for analysis> 
// dev_namespace=<dev namespace to run tests>
// url=<url of api>/api/v1/
// authurl=<Keycloak domain>
// clientid=<keycload Client ID>
// realm=<keycloak realm>

def label = "mypod-${UUID.randomUUID().toString()}"
podTemplate(
    label: label, 
    name: 'jenkins-python3nodejs', 
    serviceAccount: 'jenkins', 
    cloud: 'openshift', 
    containers: [
        containerTemplate(
            name: 'jnlp',
            image: '172.50.0.2:5000/openshift/jenkins-slave-python3nodejs',
            resourceRequestCpu: '1000m',
            resourceLimitCpu: '2000m',
            resourceRequestMemory: '2Gi',
            resourceLimitMemory: '4Gi',
            workingDir: '/tmp',
            command: '',
            args: '${computer.jnlpmac} ${computer.name}'
        )
    ]
){
    node(label) {
        stage('Checkout Source') {
            echo "checking out source"
            checkout scm
        }
        
        stage('SonarQube Analysis') {
          echo ">>> Performing static analysis <<<"
          SONARQUBE_PWD = sh (
            script: 'oc env dc/sonarqube --list | awk  -F  "=" \'/SONARQUBE_ADMINPW/{print $2}\'',
            returnStdout: true
          ).trim()

          SONARQUBE_URL = sh (
            script: 'oc get routes -o wide --no-headers | awk \'/sonarqube/{ print match($0,/edge/) ?  "https://"$2 : "http://"$2 }\'',
            returnStdout: true
          ).trim()

          echo "PWD: ${SONARQUBE_PWD}"
          echo "URL: ${SONARQUBE_URL}"

          dir('sonar-runner') {
            sh (
              returnStdout: true, 
              script: "./gradlew sonarqube -Dsonar.host.url=${SONARQUBE_URL} --stacktrace --info"
            )
          }
        }
        stage('Build API') {
            echo ">>> building queue-management-api <<<"
            openshiftBuild bldCfg: 'queue-management-api', showBuildLogs: 'true'
        }
        stage('Build Frontend') {
            echo ">>> building intermediate image: queue-management-npm-build <<<"
            openshiftBuild bldCfg: 'queue-management-npm-build', showBuildLogs: 'true'

            echo ">>> building final image: queue-management-frontend <<<"
            openshiftBuild bldCfg: 'queue-management-frontend',
                           showBuildLogs: 'true'
        }
        stage('Deploy API'){
            echo ">>> get api image hash <<<"
            API_IMAGE_HASH = sh (
                script: 'oc get istag queue-management-api:latest -o template --template="{{.image.dockerImageReference}}"|awk -F ":" \'{print $3}\'',
                returnStdout: true
            ).trim()

            echo ">>> image_hash: $API_IMAGE_HASH"

            openshiftTag destStream: 'queue-management-api', 
                         verbose: 'true', 
                         destTag: 'dev', 
                         srcStream: 'queue-management-api', 
                         srcTag: "${API_IMAGE_HASH}"

            // Sleep to ensure that the deployment has started when we begin the verification stage
            sleep 5

            DEV_NAMESPACE = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^dev_namespace/{print $2}\'',
                    returnStdout: true
                ).trim()
            openshiftVerifyDeployment depCfg: 'queue-management-api', 
                                      namespace: "${DEV_NAMESPACE}", 
                                      replicaCount: 3, 
                                      verbose: 'false', 
                                      verifyReplicaCount: 'false'

            echo ">>> deployment complete <<<"
        }
        stage('Deploy Frontend'){
            echo ">>> get frontend image hash <<<"
            FRONTEND_IMAGE_HASH = sh (
                script: 'oc get istag queue-management-frontend:latest -o template --template="{{.image.dockerImageReference}}"|awk -F ":" \'{print $3}\'',
                returnStdout: true
            ).trim()

            echo ">>> image_hash: $FRONTEND_IMAGE_HASH"

            openshiftTag destStream: 'queue-management-frontend', 
                         verbose: 'true', 
                         destTag: 'dev', 
                         srcStream: 'queue-management-frontend', 
                         srcTag: "${FRONTEND_IMAGE_HASH}"

            // Sleep to ensure that the deployment has started when we begin the verification stage
            sleep 5

            openshiftVerifyDeployment depCfg: 'queue-management-frontend', 
                                      namespace: "${DEV_NAMESPACE}", 
                                      replicaCount: 3, 
                                      verbose: 'false', 
                                      verifyReplicaCount: 'false'

            echo ">>> deployment complete <<<"
        }
        stage('Newman Tests') {
            dir('api/postman') {
                sh "ls -alh"

                sh (
                  returnStdout: true,
                  script: "npm init -y"
                )

                sh (
                  returnStdout: true,
                  script: "npm install newman"
                )

                PASSWORD = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^password_qtxn/{print $2}\'',
                    returnStdout: true
                ).trim()

                PASSWORD_NONQTXN = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^password_nonqtxn/{print $2}\'',
                    returnStdout: true
                ).trim()

                CLIENT_SECRET = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^client_secret/{print $2}\'',
                    returnStdout: true
                ).trim()

                REALM = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^realm/{print $2}\'',
                    returnStdout: true
                ).trim()

                API_URL = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^url/{print $2}\'',
                    returnStdout: true
                ).trim()

                AUTH_URL = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/auth_url/{print $2}\'',
                    returnStdout: true
                ).trim()

                CLIENTID = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^clientid/{print $2}\'',
                    returnStdout: true
                ).trim()

                sh (
                    returnStdout: true,
                    script: "./node_modules/newman/bin/newman.js run postman_tests.json -e postman_env.json --global-var 'password=${PASSWORD}' --global-var 'password_nonqtxn=${PASSWORD_NONQTXN}' --global-var 'client_secret=${CLIENT_SECRET}' --global-var 'url=${API_URL}' --global-var 'auth_url=${AUTH_URL}' --global-var 'clientid=${CLIENTID}' --global-var 'realm=${REALM}'"
                )
            }
        }
    }
}

def owaspPodLabel = "owasp-zap-${UUID.randomUUID().toString()}"
podTemplate(
    label: owaspPodLabel, 
    name: owaspPodLabel, 
    serviceAccount: 'jenkins', 
    cloud: 'openshift', 
    containers: [ containerTemplate(
        name: 'jnlp',
        image: '172.50.0.2:5000/openshift/jenkins-slave-zap',
        resourceRequestCpu: '500m',
        resourceLimitCpu: '1000m',
        resourceRequestMemory: '3Gi',
        resourceLimitMemory: '4Gi',
        workingDir: '/home/jenkins',
        command: '',
        args: '${computer.jnlpmac} ${computer.name}'
    )]
) {
    node(owaspPodLabel) {
        stage('ZAP Security Scan') {
            sleep 60
            ZAP_WITH_URL = sh (
                script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^zap_with_url/{print $2}\'',
                returnStdout: true
            ).trim()            
            def retVal = sh (
                returnStatus: true, 
                script: "${ZAP_WITH_URL}"
            )
            publishHTML([
                allowMissing: false, 
                alwaysLinkToLastBuild: false, 
                keepAll: true, 
                reportDir: '/zap/wrk', 
                reportFiles: 'baseline.html', 
                reportName: 'ZAP Baseline Scan', 
                reportTitles: 'ZAP Baseline Scan'
            ])
            echo "Return value is: ${retVal}"

            script {
                if (retVal != 0) {
                    echo "MARKING BUILD AS UNSTABLE"
                    currentBuild.result = 'UNSTABLE'
                }
            }
        }
    }
} 
node {
    stage('deploy test') {
        input "Deploy to test?"
        openshiftTag destStream: 'queue-management-api',
                     verbose: 'true',
                     destTag: 'test',
                     srcStream: 'queue-management-api',
                     srcTag: "${API_IMAGE_HASH}"

        openshiftTag destStream: 'queue-management-frontend',
                     verbose: 'true',
                     destTag: 'test',
                     srcStream: 'queue-management-frontend',
                     srcTag: "${FRONTEND_IMAGE_HASH}"
    }
} 
node {
    stage('deploy prod') {
        input "Deploy to prod?"
        openshiftTag destStream: 'queue-management-api',
                     verbose: 'true',
                     destTag: 'production',
                     srcStream: 'queue-management-api',
                     srcTag: "${API_IMAGE_HASH}"

        openshiftTag destStream: 'queue-management-frontend',
                     verbose: 'true',
                     destTag: 'production',
                     srcStream: 'queue-management-frontend',
                     srcTag: "${FRONTEND_IMAGE_HASH}"
    }
}
