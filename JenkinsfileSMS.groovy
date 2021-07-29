// This Jenkins build requires a configmap called jenkin-config with the following in it:
//
// client_secret=<keycloak client secret>
// zap_with_url_staff=<queue frontend for staff URL>
// zap_with_url=<zap command including dev url for analysis> 
// namespace=<openshift project namespace>
// url=<url of api>/api/v1/
// auth_url=<Keycloak domain>
// clientid=<keycload Client ID>
// realm=<keycloak realm>
// dev_namespace=<openshift dev namepaces for testing>
// userid_qtxn=postman tester
// password_qtxn=<cfms-postman-operator password>
// userid_nonqtxn=cfms-postman-non-operator userid>
// password_nonqtxn=<cfms-postman-non-operator password>
// public_user_id=cfms-postman-public-user
// public_user_password=<cfms-postman-public-user password>
// public_url=<public api url>
// sonarqube_key=<sonarqube key>


def WAIT_TIMEOUT = 20
def TAG_NAMES = ['dev', 'test', 'prod']
def BUILDS = ['queue-management-api','queue-management-frontend','appointment-frontend','send-appointment-reminder-crond','notifications-api','feedback-api']
def DEP_ENV_NAMES = ['dev', 'test', 'prod']
def label = "mypod-${UUID.randomUUID().toString()}"
def API_IMAGE_HASH = ""
def FRONTEND_IMAGE_HASH = ""
def APPOINTMENT_IMAGE_HASH = ""
def REMINDER_IMAGE_HASH = ""
def NOTIFICATION_IMAGE_HASH = ""
def FEEDBACK_IMAGE_HASH = ""

String getNameSpace() {
    def NAMESPACE = sh (
        script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^namespace/{print $2}\'',
        returnStdout: true
    ).trim()
    return NAMESPACE
}

// Get an image's hash tag
String getImageTagHash(String imageName, String tag = "") {

  if(!tag?.trim()) {
    tag = "latest"
  }

  def istag = openshift.raw("get istag ${imageName}:${tag} -o template --template='{{.image.dockerImageReference}}'")
  return istag.out.tokenize('@')[1].trim()
}

podTemplate(
    label: label, 
    name: 'jenkins-agent-nodejs', 
    serviceAccount: 'jenkins', 
    cloud: 'openshift', 
    containers: [
        containerTemplate(
            name: 'jnlp',
            image: 'registry.redhat.io/openshift3/jenkins-agent-nodejs-12-rhel7',
            resourceRequestCpu: '500m',
            resourceLimitCpu: '1000m',
            resourceRequestMemory: '3Gi',
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
            SONAR_ROUTE_NAME = 'sonarqube'
            SONAR_ROUTE_NAMESPACE = sh (
                script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^namespace/{print $2}\'',
                returnStdout: true
            ).trim()
            SONAR_PROJECT_NAME = 'Queue Management'
            SONAR_PROJECT_KEY = 'queue-management'
            SONAR_PROJECT_BASE_DIR = sh (
                    script: "pwd",
                    returnStdout: true
            ).trim()
            SONAR_SOURCES = 'api,frontend,appointment-frontend,jobs,feedback-api,notifications-api'
            SONARQUBE_PWD = sh (
                script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^sonarqube_key/{print $2}\'',
                returnStdout: true
            ).trim()

            SONARQUBE_URL = sh (
                script: 'oc get routes -o wide --no-headers | awk \'/sonarqube/{ print match($0,/edge/) ?  "https://"$2 : "http://"$2 }\'',
                returnStdout: true
            ).trim()

            dir('sonar-runner') {
                sh (
                    returnStdout: true,
                    script: "./gradlew sonarqube --stacktrace --info \
                        -Dsonar.verbose=true \
                        -Dsonar.login=${SONARQUBE_PWD} \
                        -Dsonar.host.url=${SONARQUBE_URL} \
                        -Dsonar.projectName='${SONAR_PROJECT_NAME}' \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.projectBaseDir=${SONAR_PROJECT_BASE_DIR} \
                        -Dsonar.sources=${SONAR_SOURCES}"
                )
            }
        }
        parallel Build_Staff_FE: {
            stage("Build Front End..") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Building Front End "
                            openshift.selector("bc", "${BUILDS[1]}").startBuild("--wait")
                        }
                        echo "Staff Front End Completed ..."
                    }
                }
            }
        }, Build_Appointment_FE: {
            stage("Build Appointment") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Bulding Appoitment Front End NPM"
                            openshift.selector("bc", "${BUILDS[2]}").startBuild("--wait")
                        }
                        echo "Appointment NPM ..."
                    }
                }
            }
        }, Build_Api: {
            stage("Build API..") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            openshift.selector("bc", "${BUILDS[0]}").startBuild("--wait")
                        }
                        echo "API Build complete ..."
                    }
                }
            }
        }, Build_Cron_Pod: {
            stage("Build Mail Cron Pod..") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            openshift.selector("bc", "${BUILDS[3]}").startBuild("--wait")
                        }
                        echo "Cron Mail Build complete ..."
                    }
                }
            }
        }, Build_notifications_api: {
            stage("Build notification api") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            openshift.selector("bc", "${BUILDS[4]}").startBuild("--wait")
                        }
                        echo "notification api complete ..."
                    }
                }
            }
        }, Build_feedback_api: {
            stage("Build feedback api") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            openshift.selector("bc", "${BUILDS[5]}").startBuild("--wait")
                        }
                        echo "notification api complete ..."
                    }
                }
            }
        }        
        parallel Depoy_API_Dev: {
            stage("Deploy API to Dev") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Tagging ${BUILDS[0]} for deployment to ${TAG_NAMES[0]} ..."

                            // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                            // Tag the images for deployment based on the image's hash
                            API_IMAGE_HASH = getImageTagHash("${BUILDS[0]}")
                            echo "API_IMAGE_HASH: ${API_IMAGE_HASH}"
                            openshift.tag("${BUILDS[0]}@${API_IMAGE_HASH}", "${BUILDS[0]}:${TAG_NAMES[0]}")
                        }

                        def NAME_SPACE = getNameSpace()
                        openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[0]}") {
                            def dc = openshift.selector('dc', "${BUILDS[0]}")
                            // Wait for the deployment to complete.
                            // This will wait until the desired replicas are all available
                            dc.rollout().status()
                        }
                        echo "API Deployment Complete."
                    }
                }
            }
        }, Depoy_Cron_Dev: {
            stage("Deploy Email Cron to Dev") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Tagging ${BUILDS[3]} for deployment to ${TAG_NAMES[0]} ..."

                            // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                            // Tag the images for deployment based on the image's hash
                            REMINDER_IMAGE_HASH = getImageTagHash("${BUILDS[3]}")
                            echo "REMINDER_IMAGE_HASH: ${REMINDER_IMAGE_HASH}"
                            openshift.tag("${BUILDS[3]}@${REMINDER_IMAGE_HASH}", "${BUILDS[3]}:${TAG_NAMES[0]}")
                        }
                    }
                }
            }
        }, Depoy_notifications_api_Dev: {
            stage("Deploy notifications api pod") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Tagging ${BUILDS[4]} for deployment to ${TAG_NAMES[0]} ..."

                            // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                            // Tag the images for deployment based on the image's hash
                            NOTIFICATION_IMAGE_HASH = getImageTagHash("${BUILDS[4]}")
                            echo "NOTIFICATION_IMAGE_HASH: ${NOTIFICATION_IMAGE_HASH}"
                            openshift.tag("${BUILDS[4]}@${NOTIFICATION_IMAGE_HASH}", "${BUILDS[4]}:${TAG_NAMES[0]}")
                        }
                    }
                }
            }
        }, Depoy_feedback_api_Dev: {
            stage("Deploy feedback api pod") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Tagging ${BUILDS[5]} for deployment to ${TAG_NAMES[0]} ..."

                            // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                            // Tag the images for deployment based on the image's hash
                            FEEDBACK_IMAGE_HASH = getImageTagHash("${BUILDS[5]}")
                            echo "NOTIFICATION_IMAGE_HASH: ${FEEDBACK_IMAGE_HASH}"
                            openshift.tag("${BUILDS[5]}@${FEEDBACK_IMAGE_HASH}", "${BUILDS[5]}:${TAG_NAMES[0]}")
                        }
                    }
                }
            }
        }, Deploy_Staff_FE_Dev: {
            stage("Deploy Frontend to Dev") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Tagging ${BUILDS[1]} for deployment to ${TAG_NAMES[0]} ..."

                            // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                            // Tag the images for deployment based on the image's hash
                            FRONTEND_IMAGE_HASH = getImageTagHash("${BUILDS[1]}")
                            echo "FRONTEND_IMAGE_HASH: ${FRONTEND_IMAGE_HASH}"
                            openshift.tag("${BUILDS[1]}@${FRONTEND_IMAGE_HASH}", "${BUILDS[1]}:${TAG_NAMES[0]}")
                        }

                        def NAME_SPACE = getNameSpace()
                        openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[0]}") {
                            dc = openshift.selector('dc', "${BUILDS[1]}")
                            // Wait for the deployment to complete.
                            // This will wait until the desired replicas are all available
                            dc.rollout().status()
                        }
                        echo "Front End Deployment Complete."
                    }
                }
            }
        }, Deploy_Appointment_Dev: {
            stage("Deploy Appointment to Dev") {
                script: {
                    openshift.withCluster() {
                        openshift.withProject() {
                            echo "Tagging ${BUILDS[2]} for deployment to ${TAG_NAMES[0]} ..."

                            // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                            // Tag the images for deployment based on the image's hash
                            APPOINTMENT_IMAGE_HASH = getImageTagHash("${BUILDS[2]}")
                            echo "APPOINTMENT_IMAGE_HASH: ${APPOINTMENT_IMAGE_HASH}"
                            openshift.tag("${BUILDS[2]}@${APPOINTMENT_IMAGE_HASH}", "${BUILDS[2]}:${TAG_NAMES[0]}")
                        }

                        def NAME_SPACE = getNameSpace()
                        openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[0]}") {
                            dc = openshift.selector('dc', "${BUILDS[2]}")
                            // Wait for the deployment to complete.
                            // This will wait until the desired replicas are all available
                            dc.rollout().status()
                        }
                        echo "Appointment Online Complete."
                    }
                }
            }
        }
        stage('Newman Tests') {
            dir('api/postman') {
                sh (
                    returnStdout: true,
                    script: "npm init -y"
                )

                sh (
                    returnStdout: true,
                    script: "npm install newman"
                )

                USERID = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^userid_qtxn/{print $2}\'',
                    returnStdout: true
                ).trim()

                PASSWORD = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^password_qtxn/{print $2}\'',
                    returnStdout: true
                ).trim()

                USERID_NONQTXN = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^userid_nonqtxn/{print $2}\'',
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

                PUBLIC_USERID = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^public_user_id/{print $2}\'',
                    returnStdout: true
                ).trim()

                PASSWORD_PUBLIC_USER = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^public_user_password/{print $2}\'',
                    returnStdout: true
                ).trim()

                PUBLIC_API_URL = sh (
                    script: 'oc describe configmap jenkin-config | awk  -F  "=" \'/^public_url/{print $2}\'',
                    returnStdout: true
                ).trim()

                NODE_OPTIONS='--max_old_space_size=2048'
                sleep(time:10,unit:"SECONDS")
                sh (
                    returnStdout: true,
                    script: "./node_modules/newman/bin/newman.js run API_Test_TheQ_Booking.json --delay-request 250 -e postman_env.json --global-var 'userid=${USERID}' --global-var 'password=${PASSWORD}' --global-var 'userid_nonqtxn=${USERID_NONQTXN}' --global-var 'password_nonqtxn=${PASSWORD_NONQTXN}' --global-var 'client_secret=${CLIENT_SECRET}' --global-var 'url=${API_URL}' --global-var 'auth_url=${AUTH_URL}' --global-var 'clientid=${CLIENTID}' --global-var 'realm=${REALM}' --global-var public_url=${PUBLIC_API_URL} --global-var public_user_id=${PUBLIC_USERID} --global-var public_user_password=${PASSWORD_PUBLIC_USER}"
                )
            }
        }
    }
}
node {
    stage("Deploy to test") {
        input "Deploy to test?"
    }
}
node {

    parallel Depoy_API_Test: {
        stage("Deploy API - test") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[0]} for deployment to ${TAG_NAMES[1]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "API_IMAGE_HASH: ${API_IMAGE_HASH}"
                        openshift.tag("${BUILDS[0]}@${API_IMAGE_HASH}", "${BUILDS[0]}:${TAG_NAMES[1]}")
                    }

                    def NAME_SPACE = getNameSpace()
                    openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[1]}") {
                        def dc = openshift.selector('dc', "${BUILDS[0]}")
                        // Wait for the deployment to complete.
                        // This will wait until the desired replicas are all available
                        dc.rollout().status()
                    }
                    echo "API Deployment Complete."
                }
            }
        }
    }, Deploy_Staff_FE_Test: {
        stage("Deploy Frontend - Test") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[1]} for deployment to ${TAG_NAMES[1]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "FRONTEND_IMAGE_HASH: ${FRONTEND_IMAGE_HASH}"
                        openshift.tag("${BUILDS[1]}@${FRONTEND_IMAGE_HASH}", "${BUILDS[1]}:${TAG_NAMES[1]}")
                    }

                    def NAME_SPACE = getNameSpace()
                    openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[1]}") {
                        dc = openshift.selector('dc', "${BUILDS[1]}")
                        // Wait for the deployment to complete.
                        // This will wait until the desired replicas are all available
                        dc.rollout().status()
                    }
                    echo "Front End Deployment Complete."
                }
            }
        } 
    }, Deploy_Appointment_Test: {
        stage("Deploy Appointment - Test") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[2]} for deployment to ${TAG_NAMES[1]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "APPOINTMENT_IMAGE_HASH: ${APPOINTMENT_IMAGE_HASH}"
                        openshift.tag("${BUILDS[2]}@${APPOINTMENT_IMAGE_HASH}", "${BUILDS[2]}:${TAG_NAMES[1]}")
                    }

                    def NAME_SPACE = getNameSpace()
                    openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[1]}") {
                        dc = openshift.selector('dc', "${BUILDS[2]}")
                        // Wait for the deployment to complete.
                        // This will wait until the desired replicas are all available
                        dc.rollout().status()
                    }
                    echo "Front End Deployment Complete."
                }
            }
        }
    }, Depoy_notifications_api_Test: {
        stage("Deploy notifications api pod") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[4]} for deployment to ${TAG_NAMES[1]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "NOTIFICATION_IMAGE_HASH: ${NOTIFICATION_IMAGE_HASH}"
                        openshift.tag("${BUILDS[4]}@${NOTIFICATION_IMAGE_HASH}", "${BUILDS[4]}:${TAG_NAMES[1]}")
                    }
                }
            }
        }
    }, Depoy_feedback_api_Test: {
        stage("Deploy feedback api pod") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[5]} for deployment to ${TAG_NAMES[1]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "NOTIFICATION_IMAGE_HASH: ${FEEDBACK_IMAGE_HASH}"
                        openshift.tag("${BUILDS[5]}@${FEEDBACK_IMAGE_HASH}", "${BUILDS[5]}:${TAG_NAMES[1]}")
                    }
                }
            }
        }        
    }, Deploy_Cron_Email_Test: {
        stage("Deploy Appt Reminder - test") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[3]} for deployment to ${TAG_NAMES[1]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "REMINDER_IMAGE_HASH: ${REMINDER_IMAGE_HASH}"
                        openshift.tag("${BUILDS[3]}@${REMINDER_IMAGE_HASH}", "${BUILDS[3]}:${TAG_NAMES[1]}")
                    }
                    echo "Appt Reminder Deployment Complete."
                }
            }
        }
    }
}
node {
    stage("Deploy to prod") {
        input "Deploy to Prod?"
    }
}
node {
    stage("Update Production") {
        script: {
            openshift.withCluster() {
                openshift.withProject() {
                    echo "Tagging Production to Stable"
                    openshift.tag("${BUILDS[0]}:prod", "${BUILDS[0]}:stable")
                    openshift.tag("${BUILDS[1]}:prod", "${BUILDS[1]}:stable")
                    openshift.tag("${BUILDS[2]}:prod", "${BUILDS[2]}:stable")
                    openshift.tag("${BUILDS[3]}:prod", "${BUILDS[3]}:stable")
                    openshift.tag("${BUILDS[4]}:prod", "${BUILDS[4]}:stable")
                    openshift.tag("${BUILDS[5]}:prod", "${BUILDS[5]}:stable")
                }
            }
        }
    }
}
node {
    parallel Depoy_API_Prod: {
        stage("Deploy API - Prod") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[0]} for deployment to ${TAG_NAMES[2]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "API_IMAGE_HASH: ${API_IMAGE_HASH}"
                        openshift.tag("${BUILDS[0]}@${API_IMAGE_HASH}", "${BUILDS[0]}:${TAG_NAMES[2]}")
                    }

                    def NAME_SPACE = getNameSpace()
                    openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[2]}") {
                        def dc = openshift.selector('dc', "${BUILDS[0]}")
                        // Wait for the deployment to complete.
                        // This will wait until the desired replicas are all available
                        dc.rollout().status()
                    }
                    echo "API Deployment Complete."
                }
            }
        }
    }, Deploy_Staff_FE_Prod: {
        stage("Deploy Frontend - Prod") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[1]} for deployment to ${TAG_NAMES[2]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "FRONTEND_IMAGE_HASH: ${FRONTEND_IMAGE_HASH}"
                        openshift.tag("${BUILDS[1]}@${FRONTEND_IMAGE_HASH}", "${BUILDS[1]}:${TAG_NAMES[2]}")
                    }

                    def NAME_SPACE = getNameSpace()
                    openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[2]}") {
                        dc = openshift.selector('dc', "${BUILDS[1]}")
                        // Wait for the deployment to complete.
                        // This will wait until the desired replicas are all available
                        dc.rollout().status()
                    }
                    echo "Front End Deployment Complete."
                }
            }
        }
    }, Deploy_Appointment_Prod: {
        stage("Deploy Appointment - Prod") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[2]} for deployment to ${TAG_NAMES[2]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "APPOINTMENT_IMAGE_HASH: ${APPOINTMENT_IMAGE_HASH}"
                        openshift.tag("${BUILDS[2]}@${APPOINTMENT_IMAGE_HASH}", "${BUILDS[2]}:${TAG_NAMES[2]}")
                    }

                    def NAME_SPACE = getNameSpace()
                    openshift.withProject("${NAME_SPACE}-${DEP_ENV_NAMES[2]}") {
                        dc = openshift.selector('dc', "${BUILDS[2]}")
                        // Wait for the deployment to complete.
                        // This will wait until the desired replicas are all available
                        dc.rollout().status()
                    }
                    echo "Front End Deployment Complete."
                }
            }
        }
    }, Depoy_notifications_api_Prod: {
        stage("Deploy notifications api pod - PROD") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[4]} for deployment to ${TAG_NAMES[2]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "NOTIFICATION_IMAGE_HASH: ${NOTIFICATION_IMAGE_HASH}"
                        openshift.tag("${BUILDS[4]}@${NOTIFICATION_IMAGE_HASH}", "${BUILDS[4]}:${TAG_NAMES[2]}")
                    }
                }
            }
        }
    }, Depoy_feedback_api_Prod: {
        stage("Deploy feedback api pod - PROD") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[5]} for deployment to ${TAG_NAMES[2]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "NOTIFICATION_IMAGE_HASH: ${FEEDBACK_IMAGE_HASH}"
                        openshift.tag("${BUILDS[5]}@${FEEDBACK_IMAGE_HASH}", "${BUILDS[5]}:${TAG_NAMES[2]}")
                    }
                }
            }
        }        
    }, Deploy_Cron_Email_Prod: {
        stage("Deploy Appt Reminders - Prod") {
            script: {
                openshift.withCluster() {
                    openshift.withProject() {
                        echo "Tagging ${BUILDS[3]} for deployment to ${TAG_NAMES[2]} ..."

                        // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                        // Tag the images for deployment based on the image's hash
                        echo "REMINDER_IMAGE_HASH: ${REMINDER_IMAGE_HASH}"
                        openshift.tag("${BUILDS[3]}@${REMINDER_IMAGE_HASH}", "${BUILDS[3]}:${TAG_NAMES[2]}")
                    }
                    echo "Appt Reminders Deployment Complete."
                }
            }
        }
    }
}