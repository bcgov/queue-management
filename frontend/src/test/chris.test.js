const puppeteer = require("puppeteer");

let page;
let browser;
const width = 1200;
const height = 800;
const maxTestCaseTime = 10000;
const USER_DATA_DIR = 'c:\\temp\\jest';
const USER_DATA_DIR_WSL = '/mnt/c/temp/jest';



beforeAll(async () => {
    browser = await puppeteer.launch({
        executablePath: 'chrome.exe',
        userDataDir: USER_DATA_DIR,
        headless: false,
        slowMo: 30,
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
          await page.goto("http://go.here.com")
            .then(() => {
                console.log("Got to the right page");
            })
            .catch((err) => {
                console.log("Could not find the page.")
            });
          await page.waitForSelector("#keycloak-login23")
            .then(() => {
                console.log("Login button is there");
            })
            .catch((err) => {
                console.log("Could not find the login button.")
            });
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
});

