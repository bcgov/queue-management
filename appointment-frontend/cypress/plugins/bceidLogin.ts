/* eslint-disable no-console */

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

import puppeteer from 'puppeteer'

class BceidLogin {
  private static readonly SELECTOR_BCEID_BUTTON_SUBMIT = 'input[name=btnSubmit]'
  private static readonly SELECTOR_BCEID_INPUT_PASSWORD = '#password'
  private static readonly SELECTOR_BCEID_INPUT_USER_ID = '#user'

  browser: puppeteer.Browser | null
  page: puppeteer.Page | null

  async init () {
    this.browser = await puppeteer.launch({
      args: ['--disable-setuid-sandbox', '--no-sandbox'],
      headless: true
    })

    this.page = await this.browser.newPage()
  }

  private async open (url: string) {
    if (this.browser === null) {
      // TODO: this doesn't work. Change index.ts to remove the init call, and
      // then sort out why setDefaultNavigationTimeout on undefined is failing.
      // Once that's done move init code into this clause.
      this.init()
    }

    this.page.setDefaultNavigationTimeout(0)

    return this.page.goto(url)
  }

  async login (url: string, username: string, password: string) {
    await this.open(url)

    try {
      await this.page.waitForSelector(BceidLogin.SELECTOR_BCEID_INPUT_USER_ID,
        { timeout: 10000, visible: true })
    } catch (exception) {
      console.debug('bceidLogin page load timeout, will retry (' + exception +
        ')')
      throw exception
    }

    await this.page.type(BceidLogin.SELECTOR_BCEID_INPUT_USER_ID, username)
    await this.page.type(BceidLogin.SELECTOR_BCEID_INPUT_PASSWORD, password)
    await this.page.click(BceidLogin.SELECTOR_BCEID_BUTTON_SUBMIT)

    await this.page.waitForNavigation({ waitUntil: 'networkidle2' })
  }

  async getSessionItems () {
    return this.page.evaluate(() => {
      let items = {}
      Object.keys(sessionStorage).forEach(key => {
        items[key] = sessionStorage.getItem(key)
      })

      return items
    })
  }

  async close () {
    await this.browser.close()
  }
}

export default BceidLogin
