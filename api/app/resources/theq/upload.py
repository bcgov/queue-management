'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''


from flask_restplus import Resource
from qsystem import api, oidc
from app.models.theq import Service
from sqlalchemy import exc
from app.schemas.theq import ServiceSchema
from requests_toolbelt.multipart import decoder
from flask import request
import os


@api.route("/upload/", methods=["POST"])
class Categories(Resource):

    def post(self):
        print("==> In the /upload/ python method")

        #  Get the file name where to put the file.
        fullpath = os.path.dirname(os.path.abspath(__file__))
        print("    --> Full path is: " + fullpath)
        end = fullpath.find("/api/")
        uploadpath = fullpath[:end+4] + "/videos" # /api/static/videos/
        print("    --> Upload path part 1 is: " + uploadpath)

        #  NOTE:  Openshift path is /opt/app-root/src/videos  Need to fix this tomorrow
        #  xxxxxx  Start here.

        #  Make first part of the directory if it doesn't already exist.
        if not os.path.isdir(uploadpath):
            os.mkdir(uploadpath)

        for file in request.files.getlist("file"):
            print(file.filename)
            filename = file.filename
            destination = "/".join([uploadpath, filename])
            print(destination)
            file.save(destination)
