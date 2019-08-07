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
    
    page.on('error', err => {
        console.log("==> Error happened at the page: ", err);
    });

    page.on('pageerror', pageerr => {
        console.log("==> Page Error happened: ", pageerr);
    });
});

afterAll(() => {
    browser.close();
});

describe("Test Google", () => {

    var allOK = false;

    test(
        "Arrived at Google?",
        async () => {
            await page.goto("https://go3ogle.com");
            await expect(page.title()).resolves.toMatch('Google');
            if (page.title() === "Google") { allOK = true };
        },
        maxTestCaseTime
    );
    
    if (allOK) { console.log("All is OK") }
    else ("All is NOT OK");
});
