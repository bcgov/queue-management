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


from flask_restx import Resource
from qsystem import api, oidc, application
from flask import request
import os
from os.path import isfile, join
from shutil import copy2


@api.route("/upload/", methods=["POST"])
class Categories(Resource):

    @oidc.accept_token(require_token=True)
    def post(self):

        #  Get the path name where to put the file, form where manifest, new file name are
        fullpath = os.path.dirname(os.path.abspath(__file__))
        end = fullpath.find("/app/")
        uploadpath = fullpath[:end] + "/videos" # /api/static/videos/
        form = request.form.to_dict()

        #  Make the directory if it doesn't already exist.
        try:
            if not os.path.isdir(uploadpath):
                os.mkdir(uploadpath)
        except Exception as error:
            print("==> Error trying to create directory: " + uploadpath)
            print("    --> Message: " + str(error))

        #   Save uploaded video file
        for file in request.files.getlist("file"):
            filename = file.filename
            if "newname" in form:
                filename = form.get("newname")

                #  If the filename doesn't end in .mp4, then add .mp4 as an extension
                file_name, file_extension = os.path.splitext(filename)
                if file_extension.lower() != '.mp4':
                    filename = filename + ".mp4"

            destination = "/".join([uploadpath, filename])
            try:
                file.save(destination)
            except Exception as error:
                print("==> Error trying to save file: " + filename)
                print("    --> Message: " + str(error))

        #  Get and save the updated manifest.
        data = form.get("manifest")
        video_path = application.config['VIDEO_PATH']
        output_file = join(video_path, 'manifest.json')
        try:
            with open(output_file, "w") as myfile:
                myfile.write(data)
        except Exception as error:
            print("==> Error trying to update file: " + output_file)
            print("    --> Message: " + str(error))
