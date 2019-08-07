const puppeteer = require("puppeteer");
const rimraf = require('rimraf');

let page;
let browser;
const width = 1200;
const height = 800;
const maxTestCaseTime = 10000;
const USER_DATA_DIR = 'c:\\temp\\jest';
const USER_DATA_DIR_WSL = '/mnt/c/temp/jest';

afterAll(() => {
    browser.close();
});

describe("Test Google", () => {
    beforeAll(async () => {
        browser = await puppeteer.launch({
            executablePath: 'chrome.exe',
            userDataDir: USER_DATA_DIR,
            headless: false,
            slowMo: 30,
            args: [`--window-size=${width},${height}`]
        });

        page = await browser.newPage();
        await page.goto("https://google.com");
    });

    it('should be titled "Google"', async () => {
        await expect(page.title()).resolves.toMatch('Google');
    });
});

