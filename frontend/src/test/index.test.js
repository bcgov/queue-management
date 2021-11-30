const puppeteer = require('puppeteer')

let page
let browser
const width = 1200
const height = 800
const maxTestCaseTime = 30000
const USER_DATA_DIR = 'c:\\temp\\jest'
const USER_DATA_DIR_WSL = '/mnt/c/temp/jest'

beforeAll(async () => {
  browser = await puppeteer.launch({
    executablePath: 'chrome.exe',
    userDataDir: USER_DATA_DIR,
    headless: false,
    slowMo: 30,
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
    'Invite and serve citizen from queue',
    async () => {
      await addCitizenToQueue()
      await inviteFromQueue()
      await beginServiceFromServeCitizenModal()
      await finishService()
    },
    maxTestCaseTime
  )

  test(
    'Invite and serve citizen using button',
    async () => {
      await addCitizenToQueue()
      await inviteCitizenFromDash()
      await beginServiceFromServeCitizenModal()
      await finishService()
    },
    maxTestCaseTime
  )

  test(
    'Return citizen to queue then complete service',
    async () => {
      await addCitizenToQueue()
      await inviteFromQueue()
      await returnToQueue()
      await inviteCitizenFromDash()
      await beginServiceFromServeCitizenModal()
      await finishService()
    },
    maxTestCaseTime
  )

  test(
    'Citizen left',
    async () => {
      await addCitizenToQueue()
      await inviteFromQueue()
      await citizenLeft()
    },
    maxTestCaseTime
  )

  test(
    'Serve citizen through the queue',
    async () => {
      await addCitizenToQueue()
      await inviteCitizenFromDash()
      await beginServiceFromServeCitizenModal()
      await placeOnHold()
      await beginServiceFromHoldTable()
      await finishService()
    },
    maxTestCaseTime
  )

  test('Begin service from add citizen modal',
    async () => {
      await addCitizenFromDash()
      await populateAddCitizen()
      await beginServiceFromAddCitizenModal()
      await finishService()
    },
    maxTestCaseTime
  )

  test(
    'Cancel service from add citizen modal',
    async () => {
      await addCitizenFromDash()
      await populateAddCitizen()
      await cancelFromAddCitizenModal()
    },
    maxTestCaseTime
  )

  test(
    'Invite as quick transaction counter',
    async () => {
      await addCitizenToQueue() // Add regular first
      await addQuickCitizenToQueue() // Add quick second
      await setCsrToQuickTxn() //  Ensure the CSR is a Quick Txn CSR
      await inviteCitizenFromDash()
      const value_qtxn = await getServeQTxnValue()
      const value_first = await getServeSelectedValue()
      await beginServiceFromServeCitizenModal()
      await finishService()

      await inviteCitizenFromDash() // Second invite bring up remaining regular
      const value_counter = await getServeCounterValue()
      const value_second = await getServeSelectedValue()
      await beginServiceFromServeCitizenModal()
      await finishService()
      await setCsrToCounter() //  Set CSR back to Counter

      //  Make sure 1st citizen from invite was QTxn, 2nd was Counter.
      const OK1 = 'First citizen was Quick Transaction'
      const OK2 = 'Second citizen was Counter Transaction'
      let message1 = ''
      let message2 = ''
      if (value_qtxn == value_first) { message1 = OK1 } else { message1 = 'First citizen was not Quick Transaction' }
      if (value_counter == value_second) { message2 = OK2 } else { message2 = 'Second citizen was not Counter Transaction' }
      expect(message1).toBe(OK1)
      expect(message2).toBe(OK2)
    },
    maxTestCaseTime
  )

  test(
    'Edit to quick transaction in serve citizen counter',
    async () => {
      await addCitizenToQueue()
      await inviteCitizenFromDash()
      await editQuickTransFromServeCitizenModal() // Edit to quick transaction
      await returnToQueue()
      await inviteCitizenFromDash()
      const value_qtxn = await getServeQTxnValue()
      const value_citizen = await getServeSelectedValue()
      await beginServiceFromServeCitizenModal()
      await finishService()

      //  Make sure 1st citizen from invite was QTxn, 2nd was Counter.
      const OK = 'Citizen was Quick Transaction'
      let message = ''
      if (value_qtxn == value_citizen) { message = OK } else { message = 'Citizen was not Quick Transaction' }
      expect(message).toBe(OK)
    },
    maxTestCaseTime
  )

  test(
    'Invite low, normal, high priority citizens',
    async () => {
      // Add low, then normal, and then high priority citizen
      await addCitizenLowPriorityToQueue()
      await addCitizenToQueue()
      await addCitizenHighPriorityToQueue()

      await inviteCitizenFromDash()
      const priorityValueHigh = await page.$eval('#priority-selection', el => el.value)
      await beginServiceFromServeCitizenModal()
      await finishService()

      await inviteCitizenFromDash()
      const priorityValueNormal = await page.$eval('#priority-selection', el => el.value)
      await beginServiceFromServeCitizenModal()
      await finishService()

      await inviteCitizenFromDash()
      const priorityValueLow = await page.$eval('#priority-selection', el => el.value)
      await beginServiceFromServeCitizenModal()
      await finishService()

      //  Make sure priority values were OK.
      const OkHigh = 'First citizen was High Priority'
      const OkNormal = 'Second citizen was Normal Priority'
      const OkLow = 'Third citizen was Low Priority'
      let MsgHigh = ''
      let MsgNormal = ''
      let MsgLow = ''
      if (priorityValueHigh == 1) { MsgHigh = OkHigh } else { MsgHigh = 'First citizen was not High Priority' }
      if (priorityValueNormal == 2) { MsgNormal = OkNormal } else { MsgNormal = 'Second citizen was not Normal Priority' }
      if (priorityValueLow == 3) { MsgLow = OkLow } else { MsgLow = 'Third citizen was not Low Priority' }
      expect(MsgHigh).toBe(OkHigh)
      expect(MsgNormal).toBe(OkNormal)
      expect(MsgLow).toBe(OkLow)
    },
    maxTestCaseTime
  )
})

function delay (time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time)
  })
}

const getCSRQTxnValue = async () => {
  const option = (await page.$x('//*[@id = "counter-selection-csr"]/option[contains(text(), "Quick")]'))[0]
  return await (await option.getProperty('value')).jsonValue()
}

const getCSRCounterValue = async () => {
  const option = (await page.$x('//*[@id = "counter-selection-csr"]/option[contains(text(), "Counter")]'))[0]
  return await (await option.getProperty('value')).jsonValue()
}

const getServeQTxnValue = async () => {
  const option = (await page.$x('//*[@id = "counter-selection-serve"]/option[contains(text(), "Quick")]'))[0]
  return await (await option.getProperty('value')).jsonValue()
}

const getServeCounterValue = async () => {
  const option = (await page.$x('//*[@id = "counter-selection-serve"]/option[contains(text(), "Counter")]'))[0]
  return await (await option.getProperty('value')).jsonValue()
}

const getServeSelectedValue = async () => {
  return await page.$eval('#counter-selection-serve', selectedValue => selectedValue.value)
}

const getAddQTxnValue = async () => {
  const option = (await page.$x('//*[@id = "counter-selection-add"]/option[contains(text(), "Quick")]'))[0]
  return await (await option.getProperty('value')).jsonValue()
}

async function addCitizenToQueue () {
  await page.waitForSelector('#add-citizen-button')
  await addCitizenFromDash()
  await populateAddCitizen()
  await addToQueue()
}

async function addQuickCitizenToQueue () {
  await page.waitForSelector('#add-citizen-button')
  await addCitizenFromDash()
  await populateAddCitizen()
  await addToQuickQueue()
}

async function addCitizenHighPriorityToQueue () {
  await page.waitForSelector('#add-citizen-button')
  await addCitizenFromDash()
  await populateAddCitizen()
  await addToHighPriorityQueue()
}

async function addCitizenLowPriorityToQueue () {
  await page.waitForSelector('#add-citizen-button')
  await addCitizenFromDash()
  await populateAddCitizen()
  await addToLowPriorityQueue()
}

async function populateAddCitizen () {
  await page.waitForSelector('#add_citizen_channels_select')
  const option = (await page.$x('//*[@id = "add_citizen_channels_select"]/option[text() = "In Person"]'))[0]
  const value = await (await option.getProperty('value')).jsonValue()
  await page.select('#add_citizen_channels_select', value)
  await page.click('.add_citizen_categories_table > tbody > tr > td')
}

async function setCsrToQuickTxn () {
  const value = await getCSRQTxnValue()
  await page.select('#counter-selection-csr', value) // Select quick transaction counter
}

async function setCsrToCounter () {
  const value = await getCSRCounterValue()
  await page.select('#counter-selection-csr', value) // Select quick transaction counter
}

async function getValueQTxnCsr () {
  const option = (await page.$x('//*[@id = "counter-selection-csr"]/option[contains(text(), "Quick")]'))[0]
  await (await option.getProperty('value')).jsonValue()
}

async function inviteFromQueue () {
  await page.waitForSelector('#client-waiting-table')
  await page.click('#client-waiting-table > table > tbody > tr > td')
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

async function beginServiceFromHoldTable () {
  await page.waitForSelector('#client-hold-table')
  await page.click('#client-hold-table > table > tbody > tr > td')
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

/**
 * Main Dashboard button functions
 */

async function inviteCitizenFromDash () {
  await page.waitForSelector('#invite-citizen-button')
  await page.click('#invite-citizen-button')
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

async function addCitizenFromDash () {
  await page.waitForSelector('#add-citizen-button')
  await page.click('#add-citizen-button')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template')
}

/**
 * Add Citizen Modal button functions
 */

async function addToQueue () {
  await page.click('#add-citizen-add-to-queue')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

async function addToQuickQueue () {
  const quick_value = await getAddQTxnValue()
  await page.select('#counter-selection-add', quick_value) // Select Quick Transaction
  await page.click('#add-citizen-add-to-queue')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

async function addToHighPriorityQueue () {
  await page.select('#priority-selection', '1') // Select high priority
  await page.click('#add-citizen-add-to-queue')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

async function addToLowPriorityQueue () {
  await page.select('#priority-selection', '3') // Select low priority
  await page.click('#add-citizen-add-to-queue')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

async function beginServiceFromAddCitizenModal () {
  await page.click('#add-citizen-begin-service')
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

async function cancelFromAddCitizenModal () {
  await page.waitForSelector('#add-citizen-cancel')
  await page.click('#add-citizen-cancel')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

/**
 * Serve Citizen Modal button functions
 */

async function beginServiceFromServeCitizenModal () {
  await page.waitForSelector('#serve-citizen-begin-service-button', {
    disabled: false
  })
  await page.click('#serve-citizen-begin-service-button')
}

async function editQuickTransFromServeCitizenModal () {
  const quick_value = await getServeQTxnValue()
  await page.select('#counter-selection-serve', quick_value) // Select Quick Transaction
}

async function returnToQueue () {
  await page.waitForSelector('#serve-citizen-return-to-queue-button', {
    disabled: false
  })
  await page.click('#serve-citizen-return-to-queue-button')
}

async function citizenLeft () {
  await page.waitForSelector('#serve-citizen-citizen-left-button', {
    disabled: false
  })
  await page.click('#serve-citizen-citizen-left-button')
}

async function placeOnHold () {
  await page.waitForSelector('#serve-citizen-place-on-hold-button', {
    disabled: false
  })
  await page.click('#serve-citizen-place-on-hold-button')
}

async function finishService () {
  await page.waitForSelector('#serve-citizen-finish-button', {
    disabled: false
  })
  await page.click('#serve-citizen-finish-button')
}
