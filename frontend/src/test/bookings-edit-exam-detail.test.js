const puppeteer = require("puppeteer");

let page;
let browser;
const width = 1200;
const height = 800;
const maxTestCaseTime = 41000;

beforeAll(async () => {
    browser = await puppeteer.launch({
        headless: false,
        slowMo: 50,
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
    "Update Exam Details",
    async () => {
      await closeNotification();
      await clickNavMenu();
      await clickNavExamInventory();
      await closeTimeTracking();
      await clickRowActionsDropDown();
    },
    maxTestCaseTime
  );

});

async function clickNavMenu() {
  await page.waitForSelector("#nav-dropdown__BV_toggle_");
  console.log("Found it")
  await page.click("#nav-dropdown__BV_toggle_");
  await delay(100);
}

async function clickNavExamInventory() {
  await page.waitForSelector("#exam_inventory");
  await page.click("#exam_inventory");
  await delay(100);
}

async function closeTimeTracking() {
  await page.waitForSelector("#add-citizen-cancel");
  await page.click("#add-citizen-cancel");
  await delay(100);
}

async function closeNotification() {
  try {
    await page.waitForSelector(".close");
    await page.click(".close");
    await delay(100);
  }catch (error){
    console.log("Notification div not present")
  }
}

function delay(time) {
  return new Promise(function(resolve) {
    setTimeout(resolve, time);
  });
}

async function clickRowActionsDropDown() {
  console.log("Testing table row");
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:nth-child(9)");
  console.log("Found it")
}
