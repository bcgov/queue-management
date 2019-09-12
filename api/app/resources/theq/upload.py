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
from qsystem import api, oidc, application
from flask import request
import os
from os.path import isfile, join
from shutil import copy2


@api.route("/upload/", methods=["POST"])
class Categories(Resource):

    @oidc.accept_token(require_token=True)
    def post(self):

        #  Get the file name where to put the file.
        fullpath = os.path.dirname(os.path.abspath(__file__))
        end = fullpath.find("/app/")
        uploadpath = fullpath[:end] + "/videos" # /api/static/videos/

        #  Make the directory if it doesn't already exist.
        if not os.path.isdir(uploadpath):
            os.mkdir(uploadpath)

        #   Save uploaded video file
        for file in request.files.getlist("file"):
            filename = file.filename
            destination = "/".join([uploadpath, filename])
            dest_save = destination + ".bak"
            if isfile(destination):
                copy2(destination, dest_save)
            file.save(destination)

        #  Get and save the updated manifest.
        form = request.form.to_dict()
        data = form.get("manifest")
        video_path = application.config['VIDEO_PATH']
        save_file = join(video_path, 'manifest.json.bak')
        output_file = join(video_path, 'manifest.json')
        copy2(output_file, save_file)
        with open(output_file, "w") as myfile:
          myfile.write(data)
