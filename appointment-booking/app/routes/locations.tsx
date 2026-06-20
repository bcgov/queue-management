import { Link } from '@bcgov/design-system-react-components'

const PAGE_DESCRIPTION =
  'Find Service BC office locations in British Columbia. View addresses, contact details, hours of operation and book an appointment.'

const OFFICES = [
  {
    name: 'Victoria',
    physicalAddress: '847 Fort Street, Victoria',
    mailingAddress: 'PO Box 9422, Victoria, BC V8W 9V1',
    phone: '250-387-6121',
    fax: '250-387-6040',
    email: 'ServiceBC.Victoria@gov.bc.ca',
    hours: [
      ['Monday to Friday', '9 am to 4:30 pm'],
      ['Closed from', '12 pm to 1 pm'],
    ],
    availableServices: [{ label: 'Popular services', href: '#' }],
    unavailableServices: [{ label: 'ICBC Driver Licensing', href: '#' }],
  },
  {
    name: 'Vancouver',
    physicalAddress: '1181 Melville Street, Vancouver',
    mailingAddress: 'PO Box 9439, Vancouver, BC V6Z 2H7',
    phone: '604-660-2421',
    fax: '604-660-2411',
    email: 'ServiceBC.Vancouver@gov.bc.ca',
    hours: [['Monday to Friday', '9 am to 4:30 pm']],
    availableServices: [{ label: 'Popular services', href: '#' }],
  },
  {
    name: 'Duncan',
    physicalAddress: '1040 Duncan Street, Duncan',
    mailingAddress: 'PO Box 1000, Duncan, BC V9L 3W4',
    phone: '250-746-1316',
    fax: '250-746-1317',
    email: 'ServiceBC.Duncan@gov.bc.ca',
    hours: [
      ['Monday to Friday', '9 am to 4:30 pm'],
      ['Closed from', '12 pm to 1 pm'],
    ],
    availableServices: [{ label: 'Popular services', href: '#' }],
    unavailableServices: [{ label: 'ICBC Driver Licensing', href: '#' }],
  },
]

export function meta() {
  return [{ title: 'Service BC Locations' }, { name: 'description', content: PAGE_DESCRIPTION }]
}

export default function Locations() {
  return (
    <>
      <h1>Service BC Locations Directory</h1>

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
            {OFFICES.map((office) => (
              <tr key={office.name}>
                <th scope="row">{office.name}</th>
                <td>
                  <p>
                    <strong>Physical address</strong>
                    <br />
                    <Link href="#">{office.physicalAddress}</Link>
                  </p>
                  <p>
                    <strong>Mailing address</strong>
                    <br />
                    {office.mailingAddress}
                  </p>
                  <p>
                    <strong>Phone:</strong> {office.phone}
                    <br />
                    <strong>Fax:</strong> {office.fax}
                    <br />
                    <Link href={`mailto:${office.email}`}>{office.email}</Link>
                  </p>
                </td>
                <td>
                  {office.hours.map((lines) => (
                    <p key={lines.join('-')}>
                      {lines.map((line, index) => (
                        <span key={line}>
                          {index > 0 ? <br /> : null}
                          {line}
                        </span>
                      ))}
                    </p>
                  ))}
                </td>
                <td>
                  <p>This office offers the following services:</p>
                  <ul>
                    {office.availableServices.map((service) => (
                      <li key={service.label}>
                        <Link href={service.href}>{service.label}</Link>
                      </li>
                    ))}
                  </ul>
                  {office.unavailableServices ? (
                    <>
                      <p>Not available at this location:</p>
                      <ul>
                        {office.unavailableServices.map((service) => (
                          <li key={service.label}>
                            <Link href={service.href}>{service.label}</Link>
                          </li>
                        ))}
                      </ul>
                    </>
                  ) : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
