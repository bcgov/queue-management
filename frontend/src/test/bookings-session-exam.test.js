const puppeteer = require("puppeteer");

let page;
let browser;
const width = 1200;
const height = 800;
const maxTestCaseTime = 45000;

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
    "Add Session Exam",
    async () => {
      await closeNotification();
      await clickNavMenu();
      await clickNavExamInventory();
      await closeTimeTracking();
      await clickNavDropDown();
      await fillInExamName();
      await fillInEventID();
      await fillInNumberOfStudents();
      await clickAddExamNext();
      await fillInExamDate();
      await fillInExamTime();
      await fillInLocation();
      await clickFillInNotes();
      await clickAddExamNext();
      await clickAddExamSubmit();
      await clickAddExamSubmitClose();

    },
    maxTestCaseTime
  );
});

async function closeNotification() {
  try {
    await page.waitForSelector(".close");
    await page.click(".close");
  }catch (error){
    console.log("Notification div not present")
  }
}

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

async function clickNavDropDown() {
  await page.waitForSelector("#add-ita button[id='add-ita__BV_toggle_']");
  await page.click("#add-ita button[id='add-ita__BV_toggle_']");
  const linkHandlers = await page.$x("//a[contains(text(), 'Add Monthly Session Exam')]");

  if (linkHandlers.length > 0) {
    await linkHandlers[0].click();
  } else {
    throw new Error("Link not found");
  }
}

async function fillInExamName() {
  await page.waitForSelector("#exam_name");
  await page.type("#exam_name", "Monthly Sessional Exam Test");
}

async function fillInEventID() {
  await page.waitForSelector("#event_id");
  await page.type("#event_id", "12345");
}


async function fillInNumberOfStudents() {
  await page.waitForSelector("#number_of_students");
  await page.type("#number_of_students", "25");
}

async function clickAddExamNext(){
  await page.waitFor("#add_exam_next");
  await page.click("#add_exam_next");
}

async function fillInExamDate() {
  await page.waitForSelector('#expiry_date input[name="date"]');
  await page.type('#expiry_date input[name="date"]', '2019-04-29');
  await page.type('#expiry_date input[name="date"]', String.fromCharCode(13));
}

async function fillInExamTime() {
  await page.waitForSelector('#exam_time input[name="date"]');
  await page.click('#exam_time input[name="date"]');
  await page.click('#exam_time ul.mx-time-list li:first-child');
}

async function fillInLocation() {
  await page.waitForSelector('#offsite_location');
  await page.type('#offsite_location', 'Test Offsite Location');
}

async function clickFillInNotes() {
  await page.waitForSelector("#notes");
  await page.click("#notes");
  await page.type("#notes", "Testing notes input field.")
}

async function clickAddExamSubmit(){
  await page.waitFor("#add_exam_submit");
  await page.click("#add_exam_submit");
}

async function clickAddExamSubmitClose(){
  await page.waitFor("#add_exam_submit_close");
  await page.click("#add_exam_submit_close");
}
