const puppeteer = require('puppeteer')

let page
let browser
const width = 1200
const height = 800
const maxTestCaseTime = 41000

beforeAll(async () => {
  browser = await puppeteer.launch({
    headless: false,
    slowMo: 100,
    args: [`--window-size=${width},${height}`]
  })
  page = await browser.newPage()
  await page.setViewport({ width, height })
})

afterAll(() => {
  browser.close()
})

describe('Serve Citizens', () => {
  test(
    'Login',
    async () => {
      await page.goto(process.env.CFMS_DEV_URL)
      await page.waitForSelector('#keycloak-login')

      const navigationPromise = page.waitForNavigation()
      await page.click('#keycloak-login')
      await navigationPromise

      await page.waitForSelector('#username')
      await page.type('#username', 'cfms-postman-operator')
      await page.type('#password', process.env.POSTMAN_OPERATOR_PASSWORD)

      await page.click('#kc-login')
      await navigationPromise

      await page.waitForSelector('label.navbar-user')
    },
    maxTestCaseTime
  )

  test(
    'Update Exam Details',
    async () => {
      await closeNotification()
      await clickNavMenu()
      await clickNavExamInventory()
      await closeTimeTracking()
      await clickRowActionsDropDown()
      await clickEditExamDetails()
      await changeExamName()
      await changeExamReceived()
      await changeEventID()
      await changeMethod()
      await changeExamineeName()
      // Not sure how this was working before without the ()
      await changeNotes()
      await clickSubmit()
    },
    maxTestCaseTime
  )
})

async function clickNavMenu () {
  await page.waitForSelector('#nav-dropdown__BV_toggle_')
  await page.click('#nav-dropdown__BV_toggle_')
}

async function clickNavExamInventory () {
  await page.waitForSelector('#exam_inventory')
  await page.click('#exam_inventory')
}

async function closeTimeTracking () {
  await page.waitForSelector('#add-citizen-cancel')
  await page.click('#add-citizen-cancel')
}

async function closeNotification () {
  try {
    await page.waitForSelector('.close')
    await page.click('.close')
  } catch (error) {
    console.log('Notification div not present')
  }
}

async function clickRowActionsDropDown () {
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:nth-child(10) div[id='nav-dropdown']")
  await page.click("#exam_inventory_table tbody tr:first-child td:nth-child(10) div[id='nav-dropdown']")
}

async function clickEditExamDetails () {
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:nth-child(10) div[id='nav-dropdown'] a[class='dropdown-item']:nth-child(2) ")
  await page.click("#exam_inventory_table tbody tr:first-child td:nth-child(10) div[id='nav-dropdown'] a[class='dropdown-item']:nth-child(2) ")
}

async function changeExamName () {
  await page.waitForSelector("input[id='exam_name']")
  await page.type("input[id='exam_name']", ' was just edited')
}

async function changeExamReceived () {
  await page.select('#exam_received', 'true')
}

async function changeEventID () {
  await page.waitForSelector("input[id='event_id']")
  await page.type("input[id='event_id']", '6')
}

async function changeMethod () {
  await page.waitForSelector("select[id='exam_method']")
  await page.select("select[id='exam_method']", 'online')
}

async function changeExamineeName () {
  await page.waitForSelector("input[id='examinee_name']")
  await page.type("input[id='examinee_name']", ': Former Beatles Member')
}

async function changeNotes () {
  await page.waitForSelector("textarea[id='notes']")
  await page.type("textarea[id='notes']", ' This was edited.')
}

async function clickSubmit () {
  await page.waitForSelector("button[id='edit_submit_allow']")
  await page.click("button[id='edit_submit_allow']")
}
