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
import os
from os.path import isfile
from pprint import pprint
from datetime import datetime

@api.route("/videofiles/", methods=["GET"])
class VideoFiles(Resource):

    @oidc.accept_token(require_token=True)
    def get(self):

        video_path = application.config['VIDEO_PATH']
        print("==> In VideoFiles, path is " + video_path)
        newfiles = []

        with os.scandir(video_path) as dir_entries:
            for entry in dir_entries:
                if isfile(entry):
                    file_name, file_extension = os.path.splitext(entry.name)
                    if file_extension.lower() == '.mp4':
                        info = entry.stat()
                        new_info = {}
                        new_info['name'] = entry.name
                        new_info['date'] = datetime.utcfromtimestamp(info.st_mtime).strftime('%Y-%m-%d %I:%H:%M %p')
                        new_info['size'] = info.st_size
                        newfiles.append(new_info)

                    if entry.name.lower() == 'manifest.json':
                        with open (entry, "r") as myfile:
                            # manifest_data = myfile.readlines()
                            manifest_data = myfile.read()
                            print("==> Manifest data")
                            print(">>" + manifest_data + "<<")

        return {'videofiles': newfiles,
                'manifest' : manifest_data,
                'errors': ''}
