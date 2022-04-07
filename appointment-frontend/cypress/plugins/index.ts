// Copyright 2022 Province of British Columbia
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

/// <reference types='cypress' />

import BceidLogin from './bceidLogin'
import { addMatchImageSnapshotPlugin } from 'cypress-image-snapshot/plugin'

export default (on: any, config: any) => {
  addMatchImageSnapshotPlugin(on, config)

  on('task', {
    bceidLogin ({ url, username, password }) {
      return (async () => {
        let bceidLogin: BceidLogin
        while (true) {
          try {
            bceidLogin = new BceidLogin()
            await bceidLogin.init()
            await bceidLogin.login(url, username, password)

            const sessionItems = await bceidLogin.getSessionItems()
            await bceidLogin.close()

            return sessionItems
          } catch (exception) {
            if (bceidLogin) {
              try {
                bceidLogin.close()
              } catch (exception) {
              }
            }
          }
        }
      })()
    }
  })
}
