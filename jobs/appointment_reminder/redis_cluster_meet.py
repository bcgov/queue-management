# Copyright © 2021 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Designed to be called by cron on a regular basis to heal the Redis cluster in
# the event of restart of all pods. To keep the code as simple as possible, it
# does a CLUSTER MEET every time it is called, even if the cluster is complete.
#
# Arguments are:
#
#  - Name of the statefulset, such as "redis-theq". This script relies on pods
#    being named "redis-theq-0" through "redis-theq-5"
#  - Hostname of the Redis service, such as "$REDIS_THEQ_SERVICE_HOST"
#  - Port number of the Redis service, such as "$REDIS_THEQ_SERVICE_PORT"
#  - Password for authenticating to the Redis nodes, such as the "password"
#    value in the "redis-theq-secret" secret.

import json
import requests
import socket
import sys

redis_statefulset = sys.argv[1]
redis_host = sys.argv[2]
redis_port = sys.argv[3]
redis_password = sys.argv[4]

# The location of the authorization token needed to make Kubernetes API calls,
# particularly pod get.
auth_token_file = "/var/run/secrets/kubernetes.io/serviceaccount/token"
auth_token = open(auth_token_file).read()

# The location of the file that tells us what namespace we're running in. Used
# for Kubernetes API calls.
namespace_file = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
namespace = open(namespace_file).read()

# The Kubernetes API endpoint that will be used to get the information for the
# Redis pods.
api_endpoint = "https://kubernetes.default.svc/api/v1/namespaces/" + \
               namespace + "/pods/"

# The self-signed certificate that is used by the Kubernetes API.
api_certificate_file = "/run/secrets/kubernetes.io/serviceaccount/" + \
                       "service-ca.crt"

# Open a socket to whatever Redis pod is on the load balancer.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((redis_host, int(redis_port)))
s.send(("HELLO 3 AUTH default " + redis_password + "\n").encode())
# print(s.recv(1024).decode())

# CLUSTER MEET with every IP, including itself (for code simplicity).
for i in range(0, 6):
    response = requests.get(api_endpoint + redis_statefulset + "-" + str(i),
                            headers={"Authorization": "Bearer " + auth_token},
                            verify=api_certificate_file)
    ip = json.loads(response.content)["status"]["podIP"]
    s.send(("CLUSTER MEET " + format(ip) + " " + redis_port + "\n").encode())
    # print(s.recv(1024).decode())

s.close()
