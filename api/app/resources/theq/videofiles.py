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
from app.models.theq import CSR
from flask import g
import os
from os.path import isfile
from pprint import pprint
from datetime import datetime

def ReadFile(entry):
    with open(entry, "r") as myfile:
        manifest_data = myfile.read()
        # print("==> Manifest data")
        # print(">>" + manifest_data + "<<")
        return manifest_data

def GetUrl(office_number, manifest_data):

    error = "Neither office " + str(office_number) + ' "default" found in manifest.json'

    #  Search for office number, if not found, search for defauult.
    search = '"' + str(office_number) + '"'
    index = manifest_data.find(search)
    if (index < 0):
        search = '"default"'
        index = manifest_data.find(search)

    #  If neither office or default found, an error in the manifest.
    if (index < 0):
        return { 'videourl' : '',
                 'errors' : error}

    print("==> In GetURL: Office: " + str(office_number) + "; Search: " + search + "; Index: " + str(index))

    #  Found the right office.  Now look for it's URL.
    left = manifest_data[index:]
    index = left.find('"url"')
    left = left[index+6:]
    index = left.find('"')
    left = left[index+1:]
    index = left.find('"')
    url = left[:index]
    print("    --> URL is: " + url)

    return {'videourl': url,
            'errors': '',
            'test': 'Hi there'}

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
                        manifest_data = ReadFile(entry)
                        # ToDo xxx PUT IN ERROR CHECKING!!!
                        # with open (entry, "r") as myfile:
                        #     manifest_data = myfile.read()
                        #     print("==> Manifest data")
                        #     print(">>" + manifest_data + "<<")

        return {'videofiles': newfiles,
                'manifest' : manifest_data,
                'errors': ''}

@api.route("/videofiles/<int:office_number>", methods=["GET"])
class VideoFileSelf(Resource):

    # @oidc.accept_token(require_token=True)
    def get(self, office_number):

        # try:

            office = office_number
            manifest_data = ""

            print("==> In GET /videofiles/me/: Office number is: " + str(office))

            video_path = application.config['VIDEO_PATH']
            with os.scandir(video_path) as dir_entries:
                for entry in dir_entries:
                    if isfile(entry):
                        if entry.name.lower() == 'manifest.json':
                            manifest_data = ReadFile(entry)

            print("    --> Manifest data is:")
            print(manifest_data)

            result = GetUrl(office, manifest_data)

            return result

    # except:
        #     print("==> Error in VideoFileSelf")
