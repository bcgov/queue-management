podTemplate(
    label: 'jenkins-python3nodejs', 
    name: 'jenkins-python3nodejs', 
    serviceAccount: 'jenkins', 
    cloud: 'openshift', 
    containers: [
        containerTemplate(
            name: 'jnlp',
            image: '172.50.0.2:5000/openshift/jenkins-slave-python3nodejs',
            resourceRequestCpu: '500m',
            resourceLimitCpu: '1000m',
            resourceRequestMemory: '1Gi',
            resourceLimitMemory: '2Gi',
            workingDir: '/tmp',
            command: '',
            args: '${computer.jnlpmac} ${computer.name}'
        )
    ]
){
    node('jenkins-python3nodejs') {
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
            openshiftBuild bldCfg: 'queue-management-frontend', showBuildLogs: 'true'
        }
        stage('Deploy API'){
            echo ">>> get api image hash <<<"
            IMAGE_HASH = sh (
                script: 'oc get istag queue-management-api:latest -o template --template="{{.image.dockerImageReference}}"|awk -F ":" \'{print $3}\'',
                returnStdout: true
            ).trim()

            echo ">>> image_hash: $IMAGE_HASH"

            openshiftTag destStream: 'queue-management-api', 
                         verbose: 'true', 
                         destTag: 'dev', 
                         srcStream: 'queue-management-api', 
                         srcTag: "${IMAGE_HASH}"

            // Sleep to ensure that the deployment has started when we begin the verification stage
            sleep 5

            openshiftVerifyDeployment depCfg: 'queue-management-api', 
                                      namespace: 'servicebc-cfms-dev', 
                                      replicaCount: 3, 
                                      verbose: 'false', 
                                      verifyReplicaCount: 'false'

            echo ">>> deployment complete <<<"
        }
        stage('Deploy Frontend'){
            echo ">>> get frontend image hash <<<"
            IMAGE_HASH = sh (
                script: 'oc get istag queue-management-frontend:latest -o template --template="{{.image.dockerImageReference}}"|awk -F ":" \'{print $3}\'',
                returnStdout: true
            ).trim()

            echo ">>> image_hash: $IMAGE_HASH"

            openshiftTag destStream: 'queue-management-frontend', 
                         verbose: 'true', 
                         destTag: 'dev', 
                         srcStream: 'queue-management-frontend', 
                         srcTag: "${IMAGE_HASH}"

            // Sleep to ensure that the deployment has started when we begin the verification stage
            sleep 5

            openshiftVerifyDeployment depCfg: 'queue-management-frontend', 
                                      namespace: 'servicebc-cfms-dev', 
                                      replicaCount: 3, 
                                      verbose: 'false', 
                                      verifyReplicaCount: 'false'

            echo ">>> deployment complete <<<"
        }
        stage('Functional Test Dev') {
            def podlabel = "queue-management-bddstack-${UUID.randomUUID().toString()}"
            podTemplate(
                label: podlabel, 
                name: podlabel, 
                serviceAccount: 'jenkins', 
                cloud: 'openshift', 
                volumes: [
                    emptyDirVolume(mountPath:'/dev/shm', memory: true)
                ],
                containers: [
                    containerTemplate(
                        name: 'jnlp',
                        image: '172.50.0.2:5000/openshift/jenkins-slave-bddstack',
                        resourceRequestCpu: '500m',
                        resourceLimitCpu: '2000m',
                        resourceRequestMemory: '2Gi',
                        resourceLimitMemory: '8Gi',
                        workingDir: '/home/jenkins',
                        command: '',
                        args: '${computer.jnlpmac} ${computer.name}',
                        envVars: [
                            envVar(key:'BASEURL', value: 'https://frontend-servicebc-cfms-dev.pathfinder.gov.bc.ca/')
                        ]
                    )
                ]
            ) {
                node(podlabel) {
                    //the checkout is mandatory, otherwise functional test would fail
                    echo "checking out source"
                    checkout scm
                    dir('functional-tests') {
                        try {
                            sh './gradlew chromeHeadlessTest'
                        } finally { 
                            archiveArtifacts allowEmptyArchive: true, artifacts: 'build/reports/**/*'
                            archiveArtifacts allowEmptyArchive: true, artifacts: 'build/test-results/**/*'
                            junit 'build/test-results/**/*.xml'
                            publishHTML (
                                target: [
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: false,
                                    keepAll: true,
                                    reportDir: 'build/reports/spock',
                                    reportFiles: 'index.html',
                                    reportName: "BDD Spock Report"
                                ]
                            )
                            publishHTML (
                                target: [
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: false,
                                    keepAll: true,
                                    reportDir: 'build/reports/tests/chromeHeadlessTest',
                                    reportFiles: 'index.html',
                                    reportName: "Full Test Report"
                                ]
                            )
                        }
                    }
                }
            }
        }
    }
}