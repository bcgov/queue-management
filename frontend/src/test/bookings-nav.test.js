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
    "Closing notifications if present",
    async () => {
      await closeNotification()
    },
    maxTestCaseTime
  );

  test(
    "Testing closing time tracking, return to /queue",
    async () => {
      await clickNavMenu();
      await clickNavRoomBooking();
      await closeTimeTracking();
      await clickNavMenu();
      await clickTheQ();
    },
    maxTestCaseTime
  );

  test(
    "Testing setting time tracking for exam management",
    async () => {
      await clickNavMenu();
      await clickNavRoomBooking();
      await setTimeTracking();
      await clickNavMenu();
      await clickTheQ();
      await returnToTheQueue();
    },
    maxTestCaseTime
  );

  test(
    "Testing Nav Menu Buttons",
    async() => {
      await clickNavMenu();
      await clickNavRoomBooking();
      await closeTimeTracking();
      await clickNavMenu();
      await clickNavExamInventory();
      await clickNavMenu();
      await clickNavOfficeAgenda();
      await clickNavMenu();
      await clickTheQ();
    },
    maxTestCaseTime
  );

});

function delay(time) {
  return new Promise(function(resolve) {
    setTimeout(resolve, time);
  });
}

async function clickNavMenu() {
  await page.waitForSelector("#nav-dropdown__BV_toggle_");
  await page.click("#nav-dropdown__BV_toggle_");
  await delay(500);
}

async function clickNavRoomBooking() {
  await page.waitForSelector("#room_bookings");
  await page.click("#room_bookings");
  await delay(500);
}

async function clickNavExamInventory() {
  await page.waitForSelector("#exam_inventory");
  await page.click("#exam_inventory");
  await delay(500);
}

async function clickNavOfficeAgenda() {
  try{
    await page.waitForSelector("#office_agenda");
    await page.click("#office_agenda");
    await delay(500);
  }catch (error){
    console.log("Is your CSR role set to GA? If so, this test has failed.")
  }
}

async function clickTheQ() {
  await page.waitForSelector("#the_q");
  await page.click("#the_q");
  await delay(500);
}

async function closeTimeTracking() {
  await page.waitForSelector("#add-citizen-cancel");
  await page.click("#add-citizen-cancel");
  await delay(500);
}

async function setTimeTracking() {
  await page.waitForSelector("#innertable");
  await page.click("#innertable > table > tbody > tr > td");
  await page.waitForSelector("#add-citizen-begin-service");
  await page.click("#add-citizen-begin-service");
  await delay(500);
}

async function returnToTheQueue() {
  await page.waitForSelector("#serve-citizen-return-to-queue-button");
  await page.click("#serve-citizen-return-to-queue-button");
  await delay(500);
}

async function closeNotification() {
  try {
    await page.waitForSelector(".close");
    await page.click(".close");
    await delay(500);
  }catch (error){
    console.log("Notification div not present")
  }
}
