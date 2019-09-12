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
# from os import listdir
# from os.path import isfile, join
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

        # print("==> print files in directory")
        # for file in listdir(video_path):
        #     full_name = join(video_path, file)
        #     if isfile(full_name):
        #         print("    --> File: " + full_name)
        #     else:
        #         print("    --> Dir:  " + full_name)

        with os.scandir(video_path) as dir_entries:
            for entry in dir_entries:
                # print("==> Next entry")
                if isfile(entry):
                    file_name, file_extension = os.path.splitext(entry.name)
                    # print("    --> File name: " + file_name + "; File Extension: " + file_extension)
                    if file_extension.lower() == '.mp4':
                        print("        --> This is a video file")
                        info = entry.stat()
                        new_info = {}
                        new_info['name'] = entry.name
                        new_info['date'] = datetime.utcfromtimestamp(info.st_mtime).strftime('%Y-%m-%d %I:%H:%M %p')
                        new_info['size'] = info.st_size
                        print("        --> Name: " + entry.name + "; Date: " + str(info.st_mtime) + "; Size: " + str(info.st_size))
                        newfiles.append(new_info)

                    if entry.name.lower() == 'manifest.json':
                        with open (entry, "r") as myfile:
                            manifest_data = myfile.readlines()
                            # print("==> manifest.json data")
                            # print(manifest_data)


        print("==> Newfiles")
        pprint(newfiles)

                #     pprint(entry)
                #     info = entry.stat()
                #     pprint(info)
                #     print("----Dir Entry-------------------------")
                #     for attr in dir(entry):
                #         print("    --> entry." + attr + " = " + str(getattr(entry, attr)))
                #     print("----Dir Info-------------------------")
                #     for attr in dir(info):
                #         print("    --> info." + attr + " = " + str(getattr(info, attr)))
                #
                # else:
                #     print("    --> Directory")
                #     pprint(entry)

        files =  {
            "files": [
                {
                    "name" : "File 1",
                    "date" : "Now",
                    "size" : "Really big"
                },
                {
                    "name": "File 2",
                    "date": "Then",
                    "size": "Really small"
                },
                {
                    "name": "File 3",
                    "date": "Sometime",
                    "size": "Medium"
                },
            ]
        }

        return {'videofiles': newfiles,
                'manifest' : manifest_data,
                'errors': ''}
