const puppeteer = require('puppeteer')

let page;
let browser;
const width = 1200;
const height = 800;
const maxTestCaseTime = 30000;

beforeAll(async () => {
  browser = await puppeteer.launch({
    headless: false,
    slowMo: 100,
    args: [`--window-size=${width},${height}`]
  });
  page = await browser.newPage();
  await page.setViewport({ width, height });
});

afterAll(() => {
  browser.close();
});

describe("Serve Citizens", () => {
  test('Login', async () => {
    await page.goto(process.env.CFMS_DEV_URL)
    await page.waitForSelector('#login-button')

    const navigationPromise = page.waitForNavigation();
    await page.click('#login-button');
    await navigationPromise;

    await page.waitForSelector('#username')
    await page.type('#username', 'cfms-postman-operator')
    await page.type('#password', process.env.POSTMAN_OPERATOR_PASSWORD)

    await page.click('#kc-login');
    await navigationPromise;

    await page.waitForSelector('label.navbar-user')
  }, maxTestCaseTime)

  test('Invite and serve citizen from queue', async () => {
    await addCitizenToQueue();
    await inviteFromQueue();
    await beginServiceFromServeCitizenModal();
    await finishService();
  }, maxTestCaseTime);

  test('Invite and serve citizen using button', async () => {
    await addCitizenToQueue();
    await inviteCitizenFromDash();
    await beginServiceFromServeCitizenModal();
    await finishService();
  }, maxTestCaseTime);

  test('Return citizen to queue then complete service', async () => {
    await addCitizenToQueue();
    await inviteFromQueue();
    await returnToQueue();
    await inviteCitizenFromDash();
    await beginServiceFromServeCitizenModal();
    await finishService();
  }, maxTestCaseTime);

  test('Citizen left', async () => {
    await addCitizenToQueue();
    await inviteFromQueue();
    await citizenLeft();
  }, maxTestCaseTime);

  test('Serve citizen through the queue', async () => {
    await addCitizenToQueue();
    await inviteCitizenFromDash();
    await beginServiceFromServeCitizenModal();
    await placeOnHold();
    await beginServiceFromHoldTable();
    await finishService();
  }, maxTestCaseTime);
/*
  test('Begin service from add citizen modal', async () => {
    await addCitizenFromDash();
    await populateAddCitizen();
    await beginServiceFromAddCitizenModal();
    await finishService();
  }, maxTestCaseTime);
*/
  test('Cancel service from add citizen modal', async () => {
    await addCitizenFromDash();
    await populateAddCitizen();
    await cancelFromAddCitizenModal();
  }, maxTestCaseTime);
})

function delay(time) {
   return new Promise(function(resolve) {
       setTimeout(resolve, time)
   });
}

async function addCitizenToQueue() {
  await addCitizenFromDash();
  await populateAddCitizen();
  await addToQueue();
}

async function populateAddCitizen() {
  await page.waitForSelector('#add_citizen_channels_select')
  await page.select('#add_citizen_channels_select', "1")
  await page.click('.add_citizen_categories_table > tbody > tr > td')
}

async function inviteFromQueue() {
  await page.click('#client-waiting-table > tbody > tr > td')
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

async function beginServiceFromHoldTable() {
  await page.click('#client-hold-table > table > tbody > tr > td')
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

/**
 * Main Dashboard button functions
 */

async function inviteCitizenFromDash() {
  await page.click('#invite-citizen-button');
  await delay(1000)
  await page.waitForSelector('.serve-modal-content')
}

async function addCitizenFromDash() {
  await page.click('#add-citizen-button');
  await delay(1000)
  await page.waitForSelector('.add_citizen_template')
}

/**
 * Add Citizen Modal button functions
 */

async function addToQueue() {
  await page.click('#add-citizen-add-to-queue')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

async function beginServiceFromAddCitizenModal() {
  await page.click('#add-citizen-begin-service')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template')
}

async function cancelFromAddCitizenModal() {
  await page.click('#add-citizen-cancel')
  await delay(1000)
  await page.waitForSelector('.add_citizen_template', { hidden: true })
}

/**
 * Serve Citizen Modal button functions
 */

async function beginServiceFromServeCitizenModal() {
  await page.waitForSelector('#serve-citizen-begin-service-button', { disabled: false })
  await page.click('#serve-citizen-begin-service-button')
}

async function returnToQueue() {
  await page.waitForSelector('#serve-citizen-return-to-queue-button', { disabled: false })
  await page.click('#serve-citizen-return-to-queue-button')
}

async function citizenLeft() {
  await page.waitForSelector('#serve-citizen-citizen-left-button', { disabled: false })
  await page.click('#serve-citizen-citizen-left-button')
}

async function placeOnHold() {
  await page.waitForSelector('#serve-citizen-place-on-hold-button', { disabled: false })
  await page.click('#serve-citizen-place-on-hold-button')
}

async function finishService() {
  await page.waitForSelector('#serve-citizen-finish-button', { disabled: false })
  await page.click('#serve-citizen-finish-button')
}
