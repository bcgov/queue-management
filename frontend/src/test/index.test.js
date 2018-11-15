const puppeteer = require("puppeteer");

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
      test(
        "Login",
        async () => {
          await page.goto(process.env.CFMS_DEV_URL);
          await page.waitForSelector("#keycloak-login");

          const navigationPromise = page.waitForNavigation();
          await page.click("#keycloak-login");
          await navigationPromise;

          await page.waitForSelector("#username");
          await page.type("#username", "cfms-postman-operator");
          await page.type("#password", process.env.POSTMAN_OPERATOR_PASSWORD);

          await page.click("#kc-login");
          await navigationPromise;

          await page.waitForSelector("label.navbar-user");
        },
        maxTestCaseTime
      );

  test(
    "Invite and serve citizen from queue",
    async () => {
      await addCitizenToQueue();
      await inviteFromQueue();
      await beginServiceFromServeCitizenModal();
      await finishService();
    },
    maxTestCaseTime
  );

  test(
    "Invite and serve citizen using button",
    async () => {
      await addCitizenToQueue();
      await inviteCitizenFromDash();
      await beginServiceFromServeCitizenModal();
      await finishService();
    },
    maxTestCaseTime
  );

  test(
    "Return citizen to queue then complete service",
    async () => {
      await addCitizenToQueue();
      await inviteFromQueue();
      await returnToQueue();
      await inviteCitizenFromDash();
      await beginServiceFromServeCitizenModal();
      await finishService();
    },
    maxTestCaseTime
  );

  test(
    "Citizen left",
    async () => {
      await addCitizenToQueue();
      await inviteFromQueue();
      await citizenLeft();
    },
    maxTestCaseTime
  );

  test(
    "Serve citizen through the queue",
    async () => {
      await addCitizenToQueue();
      await inviteCitizenFromDash();
      await beginServiceFromServeCitizenModal();
      await placeOnHold();
      await beginServiceFromHoldTable();
      await finishService();
    },
    maxTestCaseTime
  );

  test('Begin service from add citizen modal', async () => {
    await addCitizenFromDash();
    await populateAddCitizen();
    await beginServiceFromAddCitizenModal();
    await finishService();
  }, maxTestCaseTime);

  test(
    "Cancel service from add citizen modal",
    async () => {
      await addCitizenFromDash();
      await populateAddCitizen();
      await cancelFromAddCitizenModal();
    },
    maxTestCaseTime
  );

  test(
    "Invite as quick transaction counter",
    async () => {
      await addCitizenToQueue(); //Add regular first
      await addQuickCitizenToQueue(); //Add quick second
      await page.select("#counter-selection", "quick"); //Select quick transaction counter

      await inviteCitizenFromDash();
      await page.waitForSelector(".quick-span"); //Invite should bring up the quick first
      await beginServiceFromServeCitizenModal();
      await finishService();

      await inviteCitizenFromDash(); //Second invite bring up remaining regular
      await beginServiceFromServeCitizenModal();
      await finishService();
    },
    maxTestCaseTime
  );

  test(
    "Edit to quick transaction in serve citizen counter",
    async () => {
      await addCitizenToQueue();
      await inviteCitizenFromDash();
      await editQuickTransFromServeCitizenModal() //Edit to quick transaction
      await returnToQueue();
      await inviteCitizenFromDash();
      await page.waitForSelector(".quick-span"); //Should be quick transaction now
      await beginServiceFromServeCitizenModal();
      await finishService();
    },
    maxTestCaseTime
  );

  test(
    "Invite low, normal, high priority citizens",
    async () => {
      let priorityValue;
      // Add low, then normal, and then high priority citizen
      await addCitizenLowPriorityToQueue();
      await addCitizenToQueue();
      await addCitizenHighPriorityToQueue();

      await inviteCitizenFromDash();
      priorityValue = await page.$eval("#priority-selection", el => el.value);
      if(priorityValue != '1') throw('Not high priority') // First should be high
      await beginServiceFromServeCitizenModal();
      await finishService();

      await inviteCitizenFromDash();
      priorityValue = await page.$eval("#priority-selection", el => el.value);
      if (priorityValue != '2') throw ('Not normal priority') // Second should be normal
      await beginServiceFromServeCitizenModal();
      await finishService();

      await inviteCitizenFromDash();
      priorityValue = await page.$eval("#priority-selection", el => el.value);
      if(priorityValue != '3') throw('Not low priority') // Third should be low
      await beginServiceFromServeCitizenModal();
      await finishService();
    },
    maxTestCaseTime
  );
});

function delay(time) {
  return new Promise(function(resolve) {
    setTimeout(resolve, time);
  });
}

async function addCitizenToQueue() {
  await page.waitForSelector("#add-citizen-button");
  await addCitizenFromDash();
  await populateAddCitizen();
  await addToQueue();
}

async function addQuickCitizenToQueue() {
  await page.waitForSelector("#add-citizen-button");
  await addCitizenFromDash();
  await populateAddCitizen();
  await addToQuickQueue();
}

async function addCitizenHighPriorityToQueue() {
  await page.waitForSelector("#add-citizen-button");
  await addCitizenFromDash();
  await populateAddCitizen();
  await addToHighPriorityQueue();
}

async function addCitizenLowPriorityToQueue() {
  await page.waitForSelector("#add-citizen-button");
  await addCitizenFromDash();
  await populateAddCitizen();
  await addToLowPriorityQueue();
}

async function populateAddCitizen() {
  await page.waitForSelector("#add_citizen_channels_select");
  await page.select("#add_citizen_channels_select", "1");
  await page.click(".add_citizen_categories_table > tbody > tr > td");
}

async function inviteFromQueue() {
  await page.waitForSelector("#client-waiting-table");
  await page.click("#client-waiting-table > tbody > tr > td");
  await delay(1000);
  await page.waitForSelector(".serve-modal-content");
}

async function beginServiceFromHoldTable() {
  await page.waitForSelector("#client-hold-table");
  await page.click("#client-hold-table > table > tbody > tr > td");
  await delay(1000);
  await page.waitForSelector(".serve-modal-content");
}

/**
 * Main Dashboard button functions
 */

async function inviteCitizenFromDash() {
  await page.waitForSelector("#invite-citizen-button");
  await page.click("#invite-citizen-button");
  await delay(1000);
  await page.waitForSelector(".serve-modal-content");
}

async function addCitizenFromDash() {
  await page.waitForSelector("#add-citizen-button");
  await page.click("#add-citizen-button");
  await delay(1000);
  await page.waitForSelector(".add_citizen_template");
}

/**
 * Add Citizen Modal button functions
 */

async function addToQueue() {
  await page.click("#add-citizen-add-to-queue");
  await delay(1000);
  await page.waitForSelector(".add_citizen_template", { hidden: true });
}

async function addToQuickQueue() {
  await page.click(".quick");
  await page.click("#add-citizen-add-to-queue");
  await delay(1000);
  await page.waitForSelector(".add_citizen_template", { hidden: true });
}

async function addToHighPriorityQueue() {
  await page.select("#priority-selection", "1"); //Select high priority
  await page.click("#add-citizen-add-to-queue");
  await delay(1000);
  await page.waitForSelector(".add_citizen_template", { hidden: true });
}

async function addToLowPriorityQueue() {
  await page.select("#priority-selection", "3"); //Select low priority
  await page.click("#add-citizen-add-to-queue");
  await delay(1000);
  await page.waitForSelector(".add_citizen_template", { hidden: true });
}

async function beginServiceFromAddCitizenModal() {
  await page.click("#add-citizen-begin-service");
  await delay(1000);
  await page.waitForSelector(".serve-modal-content");
}

async function cancelFromAddCitizenModal() {
  await page.waitForSelector("#add-citizen-cancel");
  await page.click("#add-citizen-cancel");
  await delay(1000);
  await page.waitForSelector(".add_citizen_template", { hidden: true });
}

/**
 * Serve Citizen Modal button functions
 */

async function beginServiceFromServeCitizenModal() {
  await page.waitForSelector("#serve-citizen-begin-service-button", {
    disabled: false
  });
  await page.click("#serve-citizen-begin-service-button");
}

async function editQuickTransFromServeCitizenModal() {
  await page.waitForSelector(".quick-checkbox");
  await page.click(".quick-checkbox");
}

async function returnToQueue() {
  await page.waitForSelector("#serve-citizen-return-to-queue-button", {
    disabled: false
  });
  await page.click("#serve-citizen-return-to-queue-button");
}

async function citizenLeft() {
  await page.waitForSelector("#serve-citizen-citizen-left-button", {
    disabled: false
  });
  await page.click("#serve-citizen-citizen-left-button");
}

async function placeOnHold() {
  await page.waitForSelector("#serve-citizen-place-on-hold-button", {
    disabled: false
  });
  await page.click("#serve-citizen-place-on-hold-button");
}

async function finishService() {
  await page.waitForSelector("#serve-citizen-finish-button", {
    disabled: false
  });
  await page.click("#serve-citizen-finish-button");
}
