const puppeteer = require("puppeteer");

let page;
let browser;
const width = 1200;
const height = 800;
const maxTestCaseTime = 41000;

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
    "Testing Return Exam",
    async () => {
      await closeNotification();
      await clickNavMenu();
      await clickNavExamInventory();
      await closeTimeTracking();
      await clickRowActionsDropDown();
      await clickReturnExam();
      await selectReturnExam();
      await addActionTaken();
      await changeNotes();
      await clickSubmit();
    },
    maxTestCaseTime
  );

});

async function clickNavMenu() {
  await page.waitForSelector("#nav-dropdown__BV_toggle_");
  await page.click("#nav-dropdown__BV_toggle_");
}

async function clickNavExamInventory() {
  await page.waitForSelector("#exam_inventory");
  await page.click("#exam_inventory");
}

async function closeTimeTracking() {
  await page.waitForSelector("#add-citizen-cancel");
  await page.click("#add-citizen-cancel");
}

async function closeNotification() {
  try {
    await page.waitForSelector(".close");
    await page.click(".close");
  }catch (error){
    console.log("Notification div not present")
  }
}

async function clickRowActionsDropDown() {
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown']");
  await page.click("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown']");
}

async function clickReturnExam() {
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown'] " +
    "a[class='dropdown-item']:last-child ");
  await page.click("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown'] " +
    "a[class='dropdown-item']:last-child ");
}

async function selectReturnExam() {
  await page.waitForSelector("select[id='exam-returned-select']")
  await page.select("select[id='exam-returned-select']", "true")
}

async function addActionTaken() {
  await page.waitForSelector("input[id='action_taken']")
  await page.type("input[id='action_taken']", "Sample Tracking Number")
}

async function changeNotes() {
  await page.waitForSelector("input[id='notes']")
  await page.type("input[id='notes']", " This exam was returned.")
}

async function clickSubmit() {
  await page.waitForSelector("#return_exam_modal___BV_modal_footer_ button.btn-primary");
  await page.click("#return_exam_modal___BV_modal_footer_ button.btn-primary");
}
