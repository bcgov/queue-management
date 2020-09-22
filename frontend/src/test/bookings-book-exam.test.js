const puppeteer = require('puppeteer')

let page
let browser
const width = 1200
const height = 800
const maxTestCaseTime = 100000

beforeAll(async () => {
  browser = await puppeteer.launch({
    headless: false,
    slowMo: 100,
    args: [`--window-size=${width},${height}`]
  })
  page = await browser.newPage()
  await page.setViewport({ width, height })
})

afterAll(() => {
  browser.close()
})

describe('Serve Citizens', () => {
  test(
    'Login',
    async () => {
      await page.goto(process.env.CFMS_DEV_URL)
      await page.waitForSelector('#keycloak-login')

      const navigationPromise = page.waitForNavigation()
      await page.click('#keycloak-login')
      await navigationPromise

      await page.waitForSelector('#username')
      await page.type('#username', 'cfms-postman-operator')
      await page.type('#password', process.env.POSTMAN_OPERATOR_PASSWORD)

      await page.click('#kc-login')
      await navigationPromise

      await page.waitForSelector('label.navbar-user')
    },
    maxTestCaseTime
  )

  test(
    'Creating an Individual Exam',
    async () => {
      await closeNotification()
      await clickNavMenu()
      await clickNavExamInventory()
      await closeTimeTracking()
      await clickAddITA()
      await clickDropDown()
      await clickAddExamNext()
      await fillInEventID()
      await fillInExamName()
      await fillInCandidateName()
      await clickAddExamNext()
      await clickFillInNotes()
      await clickAddExamNext()
      await clickAddExamSubmit()
      await clickAddExamSubmitClose()
    },
    maxTestCaseTime
  )

  test(
    'Booking an Individual Exam',
    async () => {
      await closeNotification()
      await clickNavMenu()
      await clickNavExamInventory()
      await closeTimeTracking()
      await clickRowActionsDropDown()
      await clickScheduleExam()
      await clickSchedulerButton()
      await selectSchedulerOption()
      await clickNextDayButton()
      await clickCalendar()
      await clickSubmit()
    },
    maxTestCaseTime
  )
})

function delay (time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time)
  })
}

async function clickNavMenu () {
  await page.waitForSelector('#nav-dropdown__BV_toggle_')
  await page.click('#nav-dropdown__BV_toggle_')
}

async function clickNavExamInventory () {
  await page.waitForSelector('#exam_inventory')
  await page.click('#exam_inventory')
}

async function closeTimeTracking () {
  await page.waitForSelector('#add-citizen-cancel')
  await page.click('#add-citizen-cancel')
}

async function closeNotification () {
  try {
    await page.waitForSelector('.close')
    await page.click('.close')
  } catch (error) {
    console.log('Notification div not present')
  }
}

async function clickAddITA () {
  await page.waitForSelector("#add-ita button[id='add-ita__BV_button_']")
  await page.click("#add-ita button[id='add-ita__BV_button_']")
}

async function clickDropDown () {
  await page.waitForSelector('#exam_type_dropdown')
  await page.click('#exam_type_dropdown')
  const linkHandlers = await page.$x("//a[contains(text(), 'COFQ - 3HR Single Exam')]")

  if (linkHandlers.length > 0) {
    await linkHandlers[0].click()
  } else {
    throw new Error('Link not found')
  }
}

async function clickAddExamNext () {
  await page.waitFor('#add_exam_next')
  await page.click('#add_exam_next')
}

async function clickAddExamSubmit () {
  await page.waitFor('#add_exam_submit')
  await page.click('#add_exam_submit')
}

async function clickAddExamSubmitClose () {
  await page.waitFor('#add_exam_submit_close')
  await page.click('#add_exam_submit_close')
}

async function fillInEventID () {
  await page.waitForSelector('#event_id')
  await page.type('#event_id', '12345')
}

async function fillInExamName () {
  await page.waitForSelector('#exam_name')
  await page.type('#exam_name', 'ITA Individual Exam Test')
}

async function fillInCandidateName () {
  await page.waitForSelector('#examinee_name')
  await page.type('#examinee_name', 'Ringo Starr')
}

async function clickFillInNotes () {
  await page.waitForSelector('#notes')
  await page.click('#notes')
  await page.type('#notes', 'Testing notes input field.')
}

async function clickRowActionsDropDown () {
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown']")
  await page.click("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown']")
}

async function clickScheduleExam () {
  await page.waitForSelector("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown'] a[class='dropdown-item']:nth-child(1) ")
  await page.click("#exam_inventory_table tbody tr:first-child td:last-child div[id='nav-dropdown'] a[class='dropdown-item']:nth-child(1) ")
}

async function clickSchedulerButton () {
  await page.waitForSelector("button[id='view_select__BV_toggle_']")
  await page.click("button[id='view_select__BV_toggle_']")
}

async function selectSchedulerOption () {
  await page.waitForSelector("a[class='dropdown-item']:nth-child(3)")
  await page.click("a[class='dropdown-item']:nth-child(3)")
}

async function clickNextDayButton () {
  await page.waitForSelector("button[id='next']")
  await page.click("button[id='next']")
}

async function clickCalendar () {
  await page.waitForSelector("div[id='bookingcal'] div[class='fc-view-container'] " +
    "div[class='fc-view fc-agendaDay-view fc-agenda-view'] table tbody[class='fc-body'] tr td[class='fc-widget-content'] " +
    "div[class='fc-scroller fc-time-grid-container'] div[class='fc-time-grid fc-unselectable'] div[class='fc-slats'] " +
    "table tbody tr[data-time='08:00:00'] td[class='fc-widget-content']")
  await page.click("div[id='bookingcal'] div[class='fc-view-container'] " +
    "div[class='fc-view fc-agendaDay-view fc-agenda-view'] table tbody[class='fc-body'] tr td[class='fc-widget-content'] " +
    "div[class='fc-scroller fc-time-grid-container'] div[class='fc-time-grid fc-unselectable'] div[class='fc-slats'] " +
    "table tbody tr[data-time='08:00:00'] td[class='fc-widget-content']")
}

async function clickSubmit () {
  await page.waitForSelector('#booking_modal___BV_modal_footer_ button.btn-primary')
  await page.click('#booking_modal___BV_modal_footer_ button.btn-primary')
}
