# Copyright © 2019 Province of British Columbia
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
"""Job to add internal_user role to staff users."""

import argparse

import requests
import json


def run(env: str, kc_client_id: str, kc_client_secret: str, kc_realm: str):
    if not kc_client_secret:
        print('\n*********** ERROR ***********')
        print('Please provide client secret')
        print('*****************************\n')
        return

    env = env.lower()

    env_prefix = '' if env == 'prod' else f'-{env}'
    kc_base_url = f'https://sso{env_prefix}.pathfinder.gov.bc.ca/auth/'

    kc_token_url = f'{kc_base_url}realms/{kc_realm}/protocol/openid-connect/token'

    token_response = requests.post(kc_token_url,
                                   data=f'client_id={kc_client_id}&client_secret={kc_client_secret}&grant_type=client_credentials',
                                   headers={'Content-Type': 'application/x-www-form-urlencoded'})
    kc_admin_token = token_response.json().get('access_token')

    get_users_url = f'{kc_base_url}admin/realms/{kc_realm}/users?max=999999999'
    users_response = requests.get(get_users_url, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {kc_admin_token}'
    })
    print('\n****************************************')
    print('Found {} users in realm {}'.format(len(users_response.json()), kc_realm))
    print('****************************************')

    get_role_url = f'{kc_base_url}admin/realms/{kc_realm}/roles/internal_user'
    role_response = requests.get(get_role_url, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {kc_admin_token}'
    })
    print(get_role_url)
    print(kc_admin_token)

    role_response.raise_for_status()

    print(role_response.json())

    user_count: int = 0
    idir_possible_user_names_ext = ('@idir', 'idir@', 'idir/', '/idir')

    for user in users_response.json():
        user_id = user.get('id')
        user_name = user.get('username')
        if any(ext in user_name for ext in idir_possible_user_names_ext):
            print(f'adding role to user {user_name}')
            add_role_url = f'{kc_base_url}admin/realms/{kc_realm}/users/{user_id}/role-mappings/realm'
            add_role_response = requests.post(add_role_url, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {kc_admin_token}'
            }, data=json.dumps([{
                'id': role_response.json().get('id'),
                'name': role_response.json().get('name')
            }]))
            add_role_response.raise_for_status()

            user_count += 1

    print('\n****************************************')
    print(f'* Added roles to {user_count} Users *')
    print('****************************************')


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Add role to staff users.")

    parser.add_argument("-env", "--env", dest="env", help="Environment [test, prod]", metavar="ENV", default="test")

    parser.add_argument("-kc_client", "--kc_client", dest="kc_client",
                        help="Service account client ID in Keycloak. Must have roles : manage-realm, manage-users",
                        metavar="CLIENT",
                        default="add-roles-client")
    parser.add_argument("-kc_secret", "--kc_secret", dest="kc_secret", help="Service account client secret in Keycloak",
                        metavar="SECRET")
    parser.add_argument("-kc_realm", "--kc_realm", dest="kc_realm", help="Keycloak realm", metavar="REALM",
                        default="vtkayq4c")

    args = parser.parse_args()

    print(args)

    run(args.env, args.kc_client, args.kc_secret, args.kc_realm)
