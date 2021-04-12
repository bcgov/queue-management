def owaspPodLabel = "jenkins-agent-zap"
// Get an image's hash tag
String getImageTagHash(String imageName, String tag = "") {

  if(!tag?.trim()) {
    tag = "latest"
  }

  def istag = openshift.raw("get istag ${imageName}:${tag} -o template --template='{{.image.dockerImageReference}}'")
  return istag.out.tokenize('@')[1].trim()
}
podTemplate(
    label: owaspPodLabel, 
    name: owaspPodLabel, 
    serviceAccount: 'jenkins', 
    cloud: 'openshift', 
    containers: [ containerTemplate(
        name: 'jenkins-agent-zap',
        image: 'image-registry.openshift-image-registry.svc:5000/df1ee0-tools/jenkins-agent-zap:latest',
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
				def STAFFURL = sh (
						script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^zap_url_staff/{print $2}\'',
						returnStdout: true
					).trim()
				def retVal = sh (
					returnStatus: true, 
					script: "/zap/zap-baseline.py -r index1.html -t $STAFFURL",
          )
        }
        stage('ZAP Security Scan') {          
                def retVal = sh (
                    returnStatus: true, 
                    script: "/zap/zap-baseline.py -r index2.html -t $zap_url_appntmnt",
                )
                sh 'echo "<html><head></head><body><a href=index1.html>Staff Front Report</a><br><a href=index2.html>Appointment Front End Report</a></body></html>" > /zap/wrk/index.html'
                publishHTML([
                    allowMissing: false, 
                    alwaysLinkToLastBuild: true, 
                    keepAll: true, 
                    reportDir: '/zap/wrk', 
                    reportFiles: 'index.html', 
                    reportName: 'OWASPReport', 
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