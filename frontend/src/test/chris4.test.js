const puppeteer = require("puppeteer");
const rimraf = require('rimraf');

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
});

afterAll(() => {
    browser.close();
});

describe("Test Google", () => {

    test(
        "Login",
        async () => {
            await page.goto("https://google.com");
            // console.log(page);
            await expect(page.title()).resolves.toMatch('Goo33gle');
            await page.waitForSelector('title');
            var mytitle = await page.title();
            console.log("==> Title: " + mytitle);
        }
    );
});
