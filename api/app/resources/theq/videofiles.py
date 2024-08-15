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
from qsystem import api, application
from flask import request, g
import shutil

import os
import re
from os.path import isfile, join
from datetime import datetime, timezone
from pathlib import Path
from datetime import datetime
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


def read_file(entry):
    try:
        with open(entry, "r") as myfile:
            manifest_data = myfile.read()
            return {
                'data': manifest_data,
                'errors' : '',
                'code' : 200
            }
    except Exception as err:
        return {
            'data' : '',
            'errors' : str(err),
            'code' : 501
        }

def get_url(office_number, manifest_data):

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
                 'errors' : error,
                 'code' : 501 }

    #  Found the right office.  Now look for it's URL.
    left = manifest_data[index:]
    index = left.find('"url"')
    left = left[index+6:]
    index = left.find('"')
    left = left[index+1:]
    index = left.find('"')
    url = left[:index]

    return {'videourl': url,
            'errors': '',
            'code': 200}

@api.route("/videofiles/", methods=["GET"])
class VideoFiles(Resource):

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):

        video_path = application.config['VIDEO_PATH']
        newfiles = []
        manifest_data = ''
        errors = ''
        space = {}
        space['total'] = 0
        space['used'] = 0
        space['freespace'] = 0
        code = 201

        try:
            with os.scandir(video_path) as dir_entries:
                for entry in dir_entries:
                    if isfile(entry):
                        file_name, file_extension = os.path.splitext(entry.name)
                        if file_extension.lower() == '.mp4':
                            info = entry.stat()
                            new_info = {}
                            new_info['name'] = entry.name
                            new_info['date'] = datetime.fromtimestamp(info.st_mtime, tz=timezone.utc).strftime('%Y-%m-%d %I:%H:%M %p')
                            new_info['size'] = "{:10.3f}".format(info.st_size / 2**20) + "Mb"
                            newfiles.append(new_info)

                        if entry.name.lower() == 'manifest.json':
                            result = read_file(entry)
                            manifest_data = result['data']
                            errors = result['errors']
                            code = result['code']

        except Exception as error:
            manifest_data = ''
            newfiles = []
            errors = str(error)
            code = 501

        try:
            total, used, free = shutil.disk_usage(video_path)
            space['total'] = total // 2**20
            space['used'] = used // 2**20
            space['freespace'] = free // 2**20

        except Exception as error:
            errors = str(error)

        return {'videofiles': newfiles,
                'manifest' : manifest_data,
                'errors': errors,
                'code': code,
                'space': space}

@api.route("/videofiles/<int:office_number>", methods=["GET"])
class VideoFileSelf(Resource):

    # @oidc.accept_token(require_token=True)
    def get(self, office_number):

        code = 0
        errors = ''
        manifest_data = ''

        try:

            office = office_number
            manifest_data = ""

            video_path = application.config['VIDEO_PATH']
            with os.scandir(video_path) as dir_entries:
                for entry in dir_entries:
                    if isfile(entry) and entry.name.lower() == 'manifest.json':
                        result = read_file(entry)
                        manifest_data = result['data']
                        errors = result['errors']
                        code = result['code']

            if code == 200:
                result = get_url(office, manifest_data)
                return result
            else:
                return {
                    'videourl': '',
                    'errors': errors,
                    'code': code
                }

        except Exception as error:
            return {'videourl': '',
                    'errors': str(error),
                    'code': 501}

@api.route("/videofiles/", methods=["DELETE"])
class VideoFiles(Resource):

    # Sanitize the filename by removing path components, restricting allowed characters, and enforcing .mp4 extension.
    @staticmethod
    def sanitize_filename(filename):    
        filename = os.path.basename(filename)
        if not re.match(r'^[\w\-.]+$', filename):
            return None, {'message': 'Invalid filename format.'}, 400
        
        if not filename.endswith('.mp4'):
            return None, {'message': 'Only .mp4 files are allowed.'}, 400
        
        return filename, None, 200
    
    @jwt.has_one_of_roles([Role.internal_user.value])
    def delete(self):

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input filename received in DELETE /videofiles/'}, 400
        if 'name' not in json_data:
            return {'message': 'No name key received in DELETE /videofiles/'}, 400

        # sanitation
        sanitized_name, error, status = self.sanitize_filename(json_data['name'])
        if error:
            return error, status
        
        #  Try to delete the file.
        video_path = application.config['VIDEO_PATH']
        constructed_path = os.path.join(video_path, sanitized_name)


        try:
            delete_name = os.path.realpath(constructed_path)
        except FileNotFoundError:
            return {'message': 'File not found.'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

        if not os.path.commonpath([delete_name, video_path]) == video_path:
            return {'message': 'Invalid filename received in DELETE /videofiles/'}, 400

        try:
            os.remove(delete_name)
            return {}, 204
        except Exception as e:
            return {'message': str(e)}, 500
