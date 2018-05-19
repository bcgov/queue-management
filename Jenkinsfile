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
    }
}