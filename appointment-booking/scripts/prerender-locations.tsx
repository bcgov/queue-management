import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { Link } from '@bcgov/design-system-react-components'
import { Layout, Page } from '../src/components/common'
import { renderToStaticMarkup } from 'react-dom/server'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const publicCssDir = path.join(root, 'public/css')
const publicFontsDir = path.join(root, 'public/fonts')
const outputPath = path.join(root, 'public/locations/index.html')

const PAGE_DESCRIPTION =
  'Find Service BC office locations in British Columbia. View addresses, contact details,hours of operation and book an appointment.'

function decodeCssString(value: string) {
  return value.replace(/\\n/g, '\n').replace(/\\"/g, '"').replace(/\\\\/g, '\\')
}

function syncPublicStyles() {
  fs.mkdirSync(publicCssDir, { recursive: true })
  fs.mkdirSync(publicFontsDir, { recursive: true })

  fs.copyFileSync(
    path.join(root, 'node_modules/@bcgov/design-tokens/css/variables.css'),
    path.join(publicCssDir, 'design-tokens.css'),
  )

  const bcSansCss = fs
    .readFileSync(path.join(root, 'node_modules/@bcgov/bc-sans/css/BC_Sans.css'), 'utf8')
    .replace(/\.\.\/fonts\//g, '/fonts/')

  fs.writeFileSync(path.join(publicCssDir, 'bc-sans.css'), bcSansCss)

  for (const file of fs.readdirSync(path.join(root, 'node_modules/@bcgov/bc-sans/fonts'))) {
    fs.copyFileSync(
      path.join(root, 'node_modules/@bcgov/bc-sans/fonts', file),
      path.join(publicFontsDir, file),
    )
  }

  const designSystemBundle = fs.readFileSync(
    path.join(root, 'node_modules/@bcgov/design-system-react-components/dist/esm/index.js'),
    'utf8',
  )

  const shellCss = [...designSystemBundle.matchAll(/var css_[^=]+ = "((?:\\.|[^"\\])*)"/g)]
    .map((match) => decodeCssString(match[1]))
    .filter(
      (css) =>
        css.includes('.bcds-header') ||
        css.includes('.bcds-footer') ||
        css.includes('.bcds-bc-logo') ||
        css.includes('.bcds-react-aria-TextField') ||
        css.includes('.bcds-react-aria-Link'),
    )
    .join('\n\n')

  fs.writeFileSync(path.join(publicCssDir, 'bcds-shell.css'), `${shellCss}\n`)
  fs.copyFileSync(path.join(root, 'src/index.css'), path.join(publicCssDir, 'app.css'))
}

function formatPrerenderedHtml(html: string) {
  const blockTags =
    'header|footer|main|div|p|ul|table|thead|tbody|tr|th|td|figure|figcaption|hr'

  return html
    .replace(/></g, '>\n<')
    .replace(new RegExp(`\\n(<\\/?(?:${blockTags})[^>]*>)`, 'g'), '\n  $1')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

function buildHtmlDocument(body: string) {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="${PAGE_DESCRIPTION}" />
    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="stylesheet" href="/css/design-tokens.css" />
    <link rel="stylesheet" href="/css/bc-sans.css" />
    <link rel="stylesheet" href="/css/bcds-shell.css" />
    <link rel="stylesheet" href="/css/app.css" />
    <title>Service BC Locations</title>
  </head>
  <body>
    <div id="root">
${formatPrerenderedHtml(body)
  .split('\n')
  .map((line) => `      ${line}`)
  .join('\n')}
    </div>
  </body>
</html>
`
}

const LOGO_STYLES = `<style>
.bcds-bc-logo--whiteFill { fill: #ffffff; stroke-width: 0; }
.bcds-bc-logo--blueFill { fill: #234075; stroke-width: 0; }
.bcds-bc-logo--goldFill { fill: #e3a82b; stroke-width: 0; }
.bcds-bc-logo--noFill { fill: none; stroke-width: 0; }
</style>`

const LOGO_IMG =
  '<img src="/bc-gov-logo.svg" alt="Government of British Columbia" class="bc-gov-logo" />'

function externalizeLogos(body: string) {
  const logoMatch = body.match(/<svg id="bcgov-logo-header"[\s\S]*?<\/svg>/)
  if (!logoMatch) {
    return body
  }

  const logoPath = path.join(root, 'public/bc-gov-logo.svg')
  const styledSvg = logoMatch[0].replace(/(<svg[^>]*>)/, `$1${LOGO_STYLES}`)

  fs.writeFileSync(logoPath, styledSvg)

  return body
    .replace(/<svg id="bcgov-logo-header"[\s\S]*?<\/svg>/g, LOGO_IMG)
    .replace(/<svg id="bcgov-logo-footer"[\s\S]*?<\/svg>/g, LOGO_IMG)
}

function OfficeSearchField() {
  return (
    <div className="bcds-react-aria-TextField locations-search">
      <label className="bcds-react-aria-TextField--Label" htmlFor="office-search">
        Search for an office
      </label>
      <div className="bcds-react-aria-TextField--container medium">
        <input
          id="office-search"
          name="office-search"
          type="search"
          className="bcds-react-aria-TextField--Input"
          placeholder="Search by city or office name"
          autoComplete="off"
        />
      </div>
    </div>
  )
}

function LocationsContent() {
  return (
    <>
      <p>
        Find the nearest Service BC location. Before you go, please check to see if the location
        allows you to book an appointment and provides the service you need. Service availability
        can vary by office.
      </p>

      <p>
        <strong>Before you visit:</strong>
      </p>
      <ul>
        <li>Consider accessing your service online</li>
        <li>Consider booking an appointment if available</li>
        <li>Make sure the location is open and offers the service you need</li>
        <li>Confirm details such as eligibility, what to bring and cost</li>
      </ul>

      <p>Use the search bar below to find an office in your area.</p>

      <OfficeSearchField />

      <div className="locations-table-wrapper">
        <table className="locations-table">
          <thead>
            <tr>
              <th scope="col">Location</th>
              <th scope="col">Address and contact details</th>
              <th scope="col">Hours</th>
              <th scope="col">More information</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Victoria</th>
              <td>
                <p>
                  <strong>Physical address</strong>
                  <br />
                  <Link href="#">847 Fort Street, Victoria</Link>
                </p>
                <p>
                  <strong>Mailing address</strong>
                  <br />
                  PO Box 9422, Victoria, BC V8W 9V1
                </p>
                <p>
                  <strong>Phone:</strong> 250-387-6121
                  <br />
                  <strong>Fax:</strong> 250-387-6040
                  <br />
                  <Link href="mailto:ServiceBC.Victoria@gov.bc.ca">
                    ServiceBC.Victoria@gov.bc.ca
                  </Link>
                </p>
              </td>
              <td>
                <p>
                  Monday to Friday
                  <br />9 am to 4:30 pm
                </p>
                <p>
                  Closed from
                  <br />
                  12 pm to 1 pm
                </p>
              </td>
              <td>
                <p>This office offers the following services:</p>
                <ul>
                  <li>
                    <Link href="#">Popular services</Link>
                  </li>
                </ul>
                <p>Not available at this location:</p>
                <ul>
                  <li>
                    <Link href="#">ICBC Driver Licensing</Link>
                  </li>
                </ul>
              </td>
            </tr>
            <tr>
              <th scope="row">Vancouver</th>
              <td>
                <p>
                  <strong>Physical address</strong>
                  <br />
                  <Link href="#">1181 Melville Street, Vancouver</Link>
                </p>
                <p>
                  <strong>Mailing address</strong>
                  <br />
                  PO Box 9439, Vancouver, BC V6Z 2H7
                </p>
                <p>
                  <strong>Phone:</strong> 604-660-2421
                  <br />
                  <strong>Fax:</strong> 604-660-2411
                  <br />
                  <Link href="mailto:ServiceBC.Vancouver@gov.bc.ca">
                    ServiceBC.Vancouver@gov.bc.ca
                  </Link>
                </p>
              </td>
              <td>
                <p>
                  Monday to Friday
                  <br />9 am to 4:30 pm
                </p>
              </td>
              <td>
                <p>This office offers the following services:</p>
                <ul>
                  <li>
                    <Link href="#">Popular services</Link>
                  </li>
                </ul>
              </td>
            </tr>
            <tr>
              <th scope="row">Duncan</th>
              <td>
                <p>
                  <strong>Physical address</strong>
                  <br />
                  <Link href="#">1040 Duncan Street, Duncan</Link>
                </p>
                <p>
                  <strong>Mailing address</strong>
                  <br />
                  PO Box 1000, Duncan, BC V9L 3W4
                </p>
                <p>
                  <strong>Phone:</strong> 250-746-1316
                  <br />
                  <strong>Fax:</strong> 250-746-1317
                  <br />
                  <Link href="mailto:ServiceBC.Duncan@gov.bc.ca">
                    ServiceBC.Duncan@gov.bc.ca
                  </Link>
                </p>
              </td>
              <td>
                <p>
                  Monday to Friday
                  <br />9 am to 4:30 pm
                </p>
                <p>
                  Closed from
                  <br />
                  12 pm to 1 pm
                </p>
              </td>
              <td>
                <p>This office offers the following services:</p>
                <ul>
                  <li>
                    <Link href="#">Popular services</Link>
                  </li>
                </ul>
                <p>Not available at this location:</p>
                <ul>
                  <li>
                    <Link href="#">ICBC Driver Licensing</Link>
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </>
  )
}

function renderLocationsPageBody() {
  return renderToStaticMarkup(
    <Layout>
      <Page title="Service BC Locations Directory">
        <LocationsContent />
      </Page>
    </Layout>,
  )
}

function prerenderLocationsPage() {
  syncPublicStyles()
  const body = externalizeLogos(renderLocationsPageBody())
  fs.mkdirSync(path.dirname(outputPath), { recursive: true })
  fs.writeFileSync(outputPath, buildHtmlDocument(body))
}

prerenderLocationsPage()
