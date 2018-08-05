/**
 * @jest-environment jest-environment-webdriver
 */

const url = process.env['jest_url'];
const maxTestCaseTime = 30000;

/**
 * Begin test cases
 */

describe(process.env['jest_url'], () => {
  test('Login', async () => {
    await browser.get(url);
    await browser.findElement(by.id('login-button')).click();

    //At Keycloak page
    await browser.wait(until.titleIs('Log in to Service BC'), 10000);
    await browser.findElement(by.id('username')).sendKeys(process.env['jest_username']);
    await browser.findElement(by.id('password')).sendKeys(process.env['jest_password']);
    await browser.findElement(by.id('kc-login')).click();

    //Back at main page
    await browser.wait(until.titleIs('Queue Management'), 10000);

    //Wait for login to finish
    await browser.wait(until.elementIsVisible(browser.findElement(by.className('navbar-user'))), 10000);
    await browser.sleep(1000);
  }, maxTestCaseTime);

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

  test('Begin service from add citizen modal', async () => {
    await addCitizenFromDash();
    await populateAddCitizen();
    await beginServiceFromAddCitizenModal();
    await finishService();
  }, maxTestCaseTime);

  test('Cancel service from add citizen modal', async () => {
    await addCitizenFromDash();
    await populateAddCitizen();
    await cancelFromAddCitizenModal();
  }, maxTestCaseTime);
});

async function addCitizenToQueue() {
  await addCitizenFromDash();
  await populateAddCitizen();
  await addToQueue();
}

async function populateAddCitizen() {
  //Open the dropdown
  const channelDropdown = await browser.findElement(by.id('add_citizen_channels_select'));
  await channelDropdown.click();

  //Find and click the first one
  const options = await channelDropdown.findElements(by.tagName("option"));
  options[0].click();

  //Select the service
  const serviceTable = await browser.findElement(by.className('add_citizen_categories_table'));
  const service = await serviceTable.findElements(by.tagName('td'));
  service[0].click();

  await browser.sleep(1000);
}

async function inviteFromQueue() {
  const waitingCitizensTable = await browser.findElement(by.id('client-table'));
  const waitingCitizensData = await waitingCitizensTable.findElements(by.tagName('td'));

  //Open the modal
  waitingCitizensData[0].click();
  await browser.sleep(1000);
}

async function beginServiceFromHoldTable() {
  const holdCitizensTable = await browser.findElement(by.id('client-hold-table'));
  const holdCitizensRows = await holdCitizensTable.findElements(by.tagName('td'));

  //Open the modal
  holdCitizensRows[0].click();
  await browser.sleep(1000);
}

/**
 * Main Dashboard button functions
 */

async function inviteCitizenFromDash() {
  await browser.findElement(by.id('invite-citizen-button')).click();
  await browser.sleep(1000);
}

async function addCitizenFromDash() {
  await browser.findElement(by.id('add-citizen-button')).click();
  await browser.sleep(1000);
}

/**
 * Add Citizen Modal button functions
 */

async function addToQueue() {
  await browser.wait(until.elementIsVisible(browser.findElement(by.id('add-citizen-add-to-queue'))), 10000);
  await browser.findElement(by.id('add-citizen-add-to-queue')).click();
  await browser.sleep(1000);
}

async function beginServiceFromAddCitizenModal() {
  await browser.wait(until.elementIsVisible(browser.findElement(by.id('add-citizen-begin-service'))), 10000);
  await browser.findElement(by.id('add-citizen-begin-service')).click();
  await browser.sleep(1000);
}

async function cancelFromAddCitizenModal() {
  await browser.wait(until.elementIsVisible(browser.findElement(by.id('add-citizen-cancel'))), 10000);
  await browser.findElement(by.id('add-citizen-cancel')).click();
  await browser.sleep(1000);
}

/**
 * Serve Citizen Modal button functions
 */

async function beginServiceFromServeCitizenModal() {
  await browser.wait(until.elementIsVisible(browser.findElement(by.id('serve-citizen-begin-service-button'))), 10000);
  await browser.findElement(by.id('serve-citizen-begin-service-button')).click();
  await browser.sleep(1000);
}

async function returnToQueue() {
  await browser.wait(until.elementIsVisible(browser.findElement(by.id('serve-citizen-return-to-queue-button'))), 10000);
  await browser.findElement(by.id('serve-citizen-return-to-queue-button')).click();
  await browser.sleep(1000);
}

async function citizenLeft() {
  await browser.wait(until.elementIsVisible(browser.findElement(by.id('serve-citizen-citizen-left-button'))), 10000);
  await browser.findElement(by.id('serve-citizen-citizen-left-button')).click();
  await browser.sleep(1000);
}

async function placeOnHold() {
  await browser.wait(until.elementIsEnabled(browser.findElement(by.id('serve-citizen-place-on-hold-button'))), 10000);
  await browser.findElement(by.id('serve-citizen-place-on-hold-button')).click();
  await browser.sleep(1000);
}

async function finishService() {
  await browser.wait(until.elementIsEnabled(browser.findElement(by.id('serve-citizen-finish-button'))), 10000);
  await browser.findElement(by.id('serve-citizen-finish-button')).click();
  await browser.sleep(1000);
}
