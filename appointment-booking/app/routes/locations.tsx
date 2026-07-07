import { useMemo, useState } from 'react'
import {
  Button,
  Link,
  SvgChevronDownIcon,
  SvgChevronUpIcon,
  TextField,
} from '@bcgov/design-system-react-components'

const PAGE_DESCRIPTION =
  'Find Service BC office locations in British Columbia. View addresses, contact details, hours of operation and book an appointment.'

// From https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/servicebc
const OFFICES = [
  {
    name: '100 Mile House',
    physicalAddress: '300 Highway 97 S, 100 Mile House',
    mapUrl:
      'https://maps.google.com/maps?cid=9775726617242896094&%5Fga=2.32943421.206649786.1601838179-1419286085.1538141480',
    mailingAddress: 'PO Box 1600, 100 Mile House, BC V0K 2E0',
    phone: '250-395-7832',
    fax: '250-395-7837',
    email: 'ServiceBC.100MileHouse@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Ashcroft',
    physicalAddress: '318 Railway Avenue, Ashcroft',
    mapUrl:
      'https://maps.google.com/maps?cid=4165483750157607312&%5Fga=2.27167038.206649786.1601838179-1419286085.1538141480',
    mailingAddress: 'PO Box 189, Ashcroft, BC V0K 1A0',
    phone: '250-453-2412',
    fax: '250-453-9622',
    email: 'ServiceBC.Ashcroft@gov.bc.ca',
    hours: ['Monday, Wednesday, Thursday and Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Atlin',
    physicalAddress: '170-3rd Street, Atlin',
    mapUrl:
      'https://maps.google.com/maps?cid=10864636481657123462&%5Fga=2.267756685.206649786.1601838179-1419286085.1538141480',
    mailingAddress: 'Box 100, Atlin, BC V0W 1A0',
    phone: '250-651-7595',
    fax: '250-651-7707',
    email: 'ServiceBC.Atlin@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Bella Coola',
    physicalAddress: '636 Cliff Street, Bella Coola',
    mapUrl:
      'https://maps.google.com/maps?cid=1232687360222844880&%5Fga=2.99967517.206649786.1601838179-1419286085.1538141480',
    mailingAddress: 'Box 185, Bella Coola, BC V0T 1C0',
    phone: '250-799-5361',
    fax: '250-799-5450',
    email: 'ServiceBC.BellaCoola@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Burnaby',
    physicalAddress: '400 - 5021 Kingsway, Burnaby, BC V5H 4A5',
    mapUrl: 'https://goo.gl/maps/oeRKfGmcTmZP7kGo7',
    phone: '1-800-663-7867',
    email: 'ServiceBC.MVA@gov.bc.ca',
    hours: [
      'Monday to Friday 9 am to 4 pm',
      'Opens at 11 am on the last Wednesday of the month * Appointments are not available at this location',
    ],
    servicesIntro: 'This office only offers the following services:',
    availableServices: [
      {
        label: 'BC Services Card account setup',
        href: '#verifyid',
      },
      {
        label: 'BCeID registration',
        href: '#verifyid',
      },
      {
        label: 'Hazardous waste licence to transport applications',
        href: '#waste',
      },
      {
        label: 'Pesticide licence application',
        href: '#pesticide',
      },
    ],
  },
  {
    name: 'Burns Lake',
    physicalAddress: '161 Hwy 16, Burns Lake',
    mapUrl:
      'https://maps.google.com/maps?cid=5281657596853907883&%5Fga=2.94284318.206649786.1601838179-1419286085.1538141480',
    mailingAddress: 'Box 3500, Burns Lake, BC V0J 1E0',
    phone: '250-692-2528',
    fax: '250-692-2530',
    email: 'ServiceBC.BurnsLake@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Campbell River',
    physicalAddress: '115 - 1180 Ironwood Street, Campbell River, BC V9W 5P7',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Campbell+River/@50.0263673,-125.2575787,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0xa052213ba4a4224f!8m2!3d50.0263673!4d-125.25539',
    phone: '250-286-7555',
    fax: '250-286-7573',
    email: 'ServiceBC.CampbellRiver@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Chetwynd',
    physicalAddress: '4744 52nd Street, Chetwynd',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Chetwynd/@55.6980781,-121.6354742,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0xe684a7e8320f9901!8m2!3d55.6980781!4d-121.6332855',
    mailingAddress: 'PO Box, Chetwynd, BC V0C 1J0',
    phone: '250-788-2239',
    fax: '250-788-3802',
    email: 'ServiceBC.Chetwynd@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Chilliwack',
    physicalAddress: 'Suite 1 - 45467 Yale Rd W, Chilliwack, BC V2R 3Z8',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Chilliwack+%28ICBC+Driver+Licensing+-+no+Road+Tests%29/@49.1481939,-121.9674052,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0xc4294bb57ae5592!8m2!3d49.1481939!4d-121.9652165',
    phone: '604-795-8415',
    fax: '604-795-8408 or 604-795-8627',
    email: 'ServiceBC.Chilliwack@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Clinton',
    physicalAddress: '1423 Cariboo Highway, Clinton',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Clinton/@51.091681,-121.5887537,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x5dbee528b3228f03!8m2!3d51.091681!4d-121.586565',
    mailingAddress: 'Box 70, Clinton, BC V0K 1K0',
    phone: '250-459-2268',
    fax: '250-459-7082',
    email: 'ServiceBC.Clinton@gov.bc.ca',
    hours: ['Tuesday, Wednesday and Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Courtenay',
    physicalAddress: '2500 Cliffe Avenue, Courtenay, BC V9N 5M6',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Courtenay/@49.6763274,-124.984531,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x20d4a6b5577cac35!8m2!3d49.6763274!4d-124.9823423',
    phone: '250-897-7500',
    fax: '250-334-1209',
    email: 'ServiceBC.Courtenay@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Cranbrook',
    physicalAddress: '100 Cranbrook St N, Cranbrook, BC V1C 3P9',
    mapUrl:
      'https://www.google.com/maps?cid=14539569360234964172&%5Fga=2.20425275.206649786.1601838179-1419286085.1538141480',
    phone: '250-417-6100',
    fax: '250-426-1253',
    email: 'ServiceBC.Cranbrook@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Creston',
    physicalAddress: '1404 Canyon Street, Creston',
    mapUrl:
      'https://www.google.com/maps?cid=9536777157137415420&%5Fga=2.254173323.206649786.1601838179-1419286085.1538141480',
    mailingAddress: 'Box 1190, Creston, BC V0B 1G0',
    phone: '250-428-3211',
    fax: '250-428-3212',
    email: 'ServiceBC.Creston@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Daajing Giids (formerly Village of Queen Charlotte)',
    physicalAddress: '216 Oceanview Dr, Daajing Giids',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Daajing+Giids/@53.254532,-132.0850709,17z/data=!3m1!4b1!4m6!3m5!1s0x546cdcc37575f48f:0xb82c182e072a9c06!8m2!3d53.254532!4d-132.082496!16s%2Fg%2F11b5wq57g1?entry=ttu',
    mailingAddress: 'Box 309, Daajing Giids, BC V0T 1S0',
    phone: '250-559-4452',
    fax: '250-559-4798',
    email: 'ServiceBC.DaajingGiids@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Dawson Creek',
    physicalAddress: '1201- 103rd Ave, Dawson Creek, BC V1G 4J2',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Dawson+Creek/@55.7587205,-120.2382799,17z/data=!3m1!4b1!4m6!3m5!1s0x5391994742963d8d:0x8e9dc48d99e36db7!8m2!3d55.7587205!4d-120.235705!16s%2Fg%2F11btyd70yz?entry=ttu',
    phone: '250-784-2224',
    fax: '250-784-2211',
    email: 'ServiceBC.DawsonCreek@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm (MST)'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Dease Lake',
    physicalAddress: 'Block D - Hwy 37, Dease Lake',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Dease+Lake/@58.434635,-129.9886275,17z/data=!3m1!4b1!4m6!3m5!1s0x53f9bebd56aa6811:0xa6909d99520ba68c!8m2!3d58.434635!4d-129.9860526!16s%2Fg%2F1thsfl%5Fd?entry=ttu',
    mailingAddress: 'Box 337, Dease Lake, BC V0C 1L0',
    phone: '250-639-2466',
    fax: '250-771-3702',
    email: 'ServiceBC.DeaseLake@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Duncan',
    physicalAddress: '5785 Duncan St, Duncan, BC V9L 3W6',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Duncan/@48.7807655,-123.7095069,17z/data=!3m1!4b1!4m6!3m5!1s0x548f4f5e9f1380fb:0x21540e1df5bd1543!8m2!3d48.7807655!4d-123.706932!16s%2Fg%2F11b5wm09ww?entry=ttu',
    phone: '250-746-1400',
    fax: '250-746-1401',
    email: 'ServiceBC.Duncan@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Fernie',
    physicalAddress: '341 2nd Avenue, Fernie',
    mapUrl: 'https://maps.app.goo.gl/VdgzmxSzh5sE35JD9',
    mailingAddress: 'Box 1769, Fernie, BC V0B 1M0',
    phone: '250-423-6845',
    fax: '250-423-3123',
    email: 'ServiceBC.Fernie@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Fort Nelson',
    physicalAddress: 'A7 5319 - 50th Ave S, Fort Nelson',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Fort+Nelson/@58.8042998,-122.7090292,17z/data=!3m2!4b1!5s0x53eead92de1933b7:0x1e5086adf81bcd81!4m6!3m5!1s0x53eead92e41099bd:0xc72ffd6125db8a65!8m2!3d58.8042998!4d-122.7064543!16s%2Fg%2F11btx6ct24?entry=ttu',
    mailingAddress: 'Bag 1000, Fort Nelson, BC V0C 1R0',
    phone: '250-774-5555',
    fax: '250-774-3844',
    email: 'ServiceBC.FortNelson@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Fort St. James',
    physicalAddress: '470 Stuart Dr W, Fort St. James',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Fort+St.+James/@54.444893,-124.2605885,17z/data=!3m1!4b1!4m6!3m5!1s0x5389a1a7ec69655d:0x62b224b40a20e415!8m2!3d54.444893!4d-124.2580136!16s%2Fg%2F11b5wm05sq?entry=ttu',
    mailingAddress: 'Box 1328, Fort St. James, BC V0J 1P0',
    phone: '250-996-7585',
    fax: '250-996-7652',
    email: 'ServiceBC.FortStJames@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Fort St. John',
    physicalAddress: '10600 - 100th St, Fort St. John, BC V1J 4L6',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Fort+St.+John/@56.2521868,-120.850814,17z/data=!3m1!4b1!4m6!3m5!1s0x53923686ee501b51:0x51ac74bbb80695b5!8m2!3d56.2521868!4d-120.8482391!16s%2Fg%2F1vpq6kpd?entry=ttu',
    phone: '250-787-3350',
    fax: '250-787-3210',
    email: 'ServiceBC.FortStJohn@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm (MST)'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Ganges',
    physicalAddress: '343 Lower Ganges Rd, Salt Spring Island, BC V8K 2V4',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Ganges/@48.8602017,-123.5116376,17z/data=!3m1!4b1!4m6!3m5!1s0x548f574869e27da9:0x82f3b1cc67b9078!8m2!3d48.8602017!4d-123.5090627!16s%2Fg%2F1tgwmczg?entry=ttu',
    phone: '250-537-5414',
    fax: '250-537-4361',
    email: 'ServiceBC.SaltSpring@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Golden',
    physicalAddress: '1104 9 St. S, Golden',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Golden/@51.2965698,-116.9685325,17z/data=!3m1!4b1!4m6!3m5!1s0x5379bf99f343129b:0xbf4287536be00922!8m2!3d51.2965698!4d-116.9659576!16s%2Fg%2F11b5wqckk2?entry=ttu',
    mailingAddress: 'Box 39, Golden, BC V0A 1H0',
    phone: '250-344-7550',
    fax: '250-344-7553',
    email: 'ServiceBC.Golden@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm (MST)', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Grand Forks',
    physicalAddress: '7290 2nd St., Grand Forks',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Grand+Forks/@49.032616,-118.4393689,17z/data=!3m1!4b1!4m6!3m5!1s0x5362adc7ec7692c3:0x36030ada0874db42!8m2!3d49.032616!4d-118.436794!16s%2Fg%2F11b5wm6wrr?entry=ttu',
    mailingAddress: 'Box 850, Grand Forks, BC V0H 1H0',
    phone: '250-442-4306',
    fax: '250-442-4317',
    email: 'ServiceBC.GrandForks@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Hazelton',
    physicalAddress: '2210 Hwy 62, Hazelton',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Hazelton/@55.2573739,-127.6642379,17z/data=!3m1!4b1!4m6!3m5!1s0x5475498015ecc433:0x52ff3ec2d9a2a5b4!8m2!3d55.257374!4d-127.659367!16s%2Fg%2F11btx6vv7v?entry=ttu',
    mailingAddress: 'PO Box 380, Hazelton, BC V0J 1Y0',
    phone: '250-842-6573',
    fax: '250-842-6275',
    email: 'ServiceBC.Hazelton@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Houston',
    physicalAddress: '3400 - 11th St, Houston',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Houston/@54.398616,-126.6493949,17z/data=!3m1!4b1!4m6!3m5!1s0x5475c686bb39c2a3:0xb315cc4a75e7baa5!8m2!3d54.398616!4d-126.64682!16s%2Fg%2F1vpps6c8?entry=ttu',
    mailingAddress: 'Bag 2000, Houston, BC V0J 1Z0',
    phone: '250-845-5828',
    fax: '250-845-7424',
    email: 'ServiceBC.Houston@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Invermere',
    physicalAddress: '625 - 4th St, Invermere',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Invermere/@50.509419,-116.0311569,17z/data=!3m1!4b1!4m6!3m5!1s0x537a66ca36ab48cf:0x952c4b6afae690ea!8m2!3d50.509419!4d-116.028582!16s%2Fg%2F11bt%5Fhc1yr?entry=ttu',
    mailingAddress: 'Box 265, Invermere, BC V0A 1K0',
    phone: '250-342-4260',
    fax: '250-342-4262',
    email: 'ServiceBC.Invermere@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Kamloops',
    physicalAddress: '250 - 455 Columbia St, Kamloops, BC V2C 6K4',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Kamloops+%28No+Driver+Services%29/@50.6704457,-120.3334504,17z/data=!3m2!4b1!5s0x537e2c52c3946b3f:0x298494bee73e884f!4m6!3m5!1s0x537e2c52c4bd4b3b:0xd4c876c9378bc5c!8m2!3d50.6704457!4d-120.3308755!16s%2Fg%2F11b7fgb6hk?entry=ttu',
    phone: '250-828-4540',
    fax: '250-828-4233',
    email: 'ServiceBC.Kamloops@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Kaslo',
    physicalAddress: '413 4th St, Kaslo',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Kaslo/@49.9106913,-116.9074567,17z/data=!3m1!4b1!4m6!3m5!1s0x537b691eedcafc93:0xaf026678f3cef0af!8m2!3d49.9106913!4d-116.9048818!16s%2Fg%2F11b5wqn8kp?entry=ttu',
    mailingAddress: 'PO BOX 580, Kaslo, BC V0G 1C0',
    phone: '250-353-2219',
    fax: '250-353-2316',
    email: 'ServiceBC.Kaslo@gov.bc.ca',
    hours: ['Monday to Friday 10 am to 3 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Kelowna',
    physicalAddress: '305 - 478 Bernard Ave, Kelowna, BC V1Y 6N7',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Kelowna/@49.8865197,-119.4965438,17z/data=!3m1!4b1!4m6!3m5!1s0x537df4a880b32d3f:0x85387667c7ab560c!8m2!3d49.8865197!4d-119.4939689!16s%2Fg%2F11b5wn3f74?entry=ttu',
    phone: '250-861-7500',
    fax: '250-712-7598',
    email: 'ServiceBC.Kelowna@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Kitimat',
    physicalAddress: '795 S Lahakas Blvd, Kitimat, BC V8C 1G2',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Kitimat/@54.0519485,-128.6585806,17z/data=!3m1!4b1!4m6!3m5!1s0x54739b6454da373d:0x1f4c178897512bd9!8m2!3d54.0519485!4d-128.6560057!16s%2Fg%2F11btxkdwjg?entry=ttu',
    phone: '250-632-6188',
    fax: '250-639-9422',
    email: 'ServiceBC.Kitimat@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Lillooet',
    physicalAddress: 'Suite A - 639 Main St, Lillooet',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Lillooet/@50.6931798,-121.9373254,17z/data=!3m1!4b1!4m6!3m5!1s0x54808a397cf6e279:0x7017ed52e60323fd!8m2!3d50.6931798!4d-121.9347505!16s%2Fg%2F11b5wlrdcp?entry=ttu',
    mailingAddress: 'Box 1629, Lillooet, BC V0K 1V0',
    phone: '250-256-7548',
    fax: '250-256-4546',
    email: 'ServiceBC.Lillooet@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Mackenzie',
    physicalAddress: '64 Centennial Dr, Mackenzie',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Mackenzie/@55.338544,-123.0987829,17z/data=!3m1!4b1!4m6!3m5!1s0x538c219180afcd63:0xe3543890a76e9f3b!8m2!3d55.338544!4d-123.096208!16s%2Fg%2F11b5wrblk7?entry=ttu',
    mailingAddress: 'PO Box 2400, Mackenzie, BC V0J 2C0',
    phone: '250-997-4270',
    fax: '250-997-5617',
    email: 'ServiceBC.Mackenzie@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Maple Ridge',
    physicalAddress: '175 - 22470 Dewdney Trunk Rd, Maple Ridge, BC V2X 5Z6',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Maple+Ridge/@49.2199139,-122.6022748,17z/data=!3m2!4b1!5s0x5485d35fac9f3e3b:0x1c3036ab63234573!4m6!3m5!1s0x5485d35fad28fdf7:0x13740aa378e9aa87!8m2!3d49.2199139!4d-122.5996999!16s%2Fg%2F11b5wct5wg?entry=ttu',
    phone: '604-466-7470',
    fax: '604-467-6131',
    email: 'ServiceBC.MapleRidge@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Masset',
    physicalAddress: '1666 Orr St, Masset',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Masset/@54.0128251,-132.1494609,17z/data=!3m1!4b1!4m6!3m5!1s0x5412958802cfbca7:0x575f9ab216a889f0!8m2!3d54.0128251!4d-132.146886!16s%2Fg%2F11b7xxp8tf?entry=ttu',
    mailingAddress: 'Box 226, Massett, BC V0T 1M0',
    phone: '250-626-5278',
    fax: '250-626-9356',
    email: 'ServiceBC.Masset@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Merritt',
    physicalAddress: '2194 Coutlee Ave, Merritt',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Merritt/@50.108281,-120.7879019,17z/data=!3m2!4b1!5s0x548190ec23ae228d:0x85c8ec32876eaa1!4m6!3m5!1s0x548190ec2f1f15d7:0xcbc1b9ed7d5e4501!8m2!3d50.108281!4d-120.785327!16s%2Fg%2F11b6bdz%5F79?entry=ttu',
    mailingAddress: 'PO Box 729, Stn Main, Merritt, BC V1K 1B8',
    phone: '250-378-9343',
    fax: '250-378-9346',
    email: 'ServiceBC.Merritt@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Mission (temporary location)',
    physicalAddress: '7650 Grand St, Mission, BC (inside the Mission Leisure Centre)',
    mapUrl: 'https://maps.app.goo.gl/Sc4vMwxTtpgQicjz8',
    hours: [
      'Open every other Tuesday 9 am to 4:30 pm',
      'By appointment and walk-in March 10 to May 19, 2026',
    ],
    servicesIntro: 'Limited services available',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
      {
        label: 'Income assistance',
        href: '#income',
      },
      {
        label: 'Cash or cheque payments',
        href: '#',
      },
    ],
  },
  {
    name: 'Nakusp',
    physicalAddress: '204 - 6th Ave NW, Nakusp',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Nakusp/@50.2415686,-117.8077701,17z/data=!3m1!4b1!4m6!3m5!1s0x537c715ffaa507ff:0xb15b93e5f1562610!8m2!3d50.2415686!4d-117.8051952!16s%2Fg%2F11b5wkjpch?entry=ttu',
    mailingAddress: 'PO Box 128, Nakusp, BC V0G 1R0',
    phone: '250-265-4865',
    fax: '250-265-3117',
    email: 'ServiceBC.Nakusp@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Nanaimo',
    physicalAddress: '460 Selby St, Nanaimo, BC V9R 2R7',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Nanaimo/@49.1621643,-123.9422165,17z/data=!3m1!4b1!4m6!3m5!1s0x5488a3fcde758bab:0x84670a25d2f071f4!8m2!3d49.1621643!4d-123.9396416!16s%2Fg%2F1tjl5lv2?entry=ttu',
    phone: '250-741-3636',
    fax: '250-741-3663',
    email: 'ServiceBC.Nanaimo@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Nelson',
    physicalAddress: '310 Ward St, Nelson, BC V1L 5S4',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Nelson/@49.493205,-117.2983557,17z/data=!3m2!4b1!5s0x537cb6a5bd449c8d:0xea91bba29793b3c5!4m6!3m5!1s0x537cb6a59a4f9df3:0xbc13347f8f19ded4!8m2!3d49.493205!4d-117.2957808!16s%2Fg%2F1q6qbmmm0?entry=ttu',
    phone: '250-354-6104',
    fax: '250-354-6102',
    email: 'ServiceBC.Nelson@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Oliver',
    physicalAddress: '5917 Airport Street, Oliver',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Oliver/@49.1779746,-119.5524423,17z/data=!3m1!4b1!4m6!3m5!1s0x5482ea370a4a4d6d:0x7c95d10b3f83571e!8m2!3d49.1779746!4d-119.5498674!16s%2Fg%2F1tj962yk?entry=ttu',
    mailingAddress: 'Box 5000, Oliver, BC V0H 1T0',
    phone: '250-498-3818',
    fax: '250-498-6333',
    email: 'ServiceBC.Oliver@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Penticton',
    physicalAddress: '40 Calgary Ave, Penticton, BC V2A 2T6',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Penticton/@49.4854821,-119.5900153,17z/data=!3m1!4b1!4m6!3m5!1s0x548289dbeec2c1e5:0x43eec24a1ddfc946!8m2!3d49.4854821!4d-119.5874404!16s%2Fg%2F1q6q9srh1?entry=ttu',
    phone: '250-487-4200',
    fax: '250-487-4222',
    email: 'ServiceBC.Penticton@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Port Alberni',
    physicalAddress: '4070 - 8th Ave, Port Alberni ,BC V9Y 4S4',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Port+Alberni/@49.2500353,-124.8035776,17z/data=!3m1!4b1!4m6!3m5!1s0x5488f721d609a34b:0x21154a5dc6148291!8m2!3d49.2500353!4d-124.8010027!16s%2Fg%2F1ptx%5Fc2q7?entry=ttu',
    phone: '250-720-2040',
    fax: '250-724-9298',
    email: 'ServiceBC.Port.Alberni@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Port Hardy',
    physicalAddress: '8785 Gray St, Port Hardy',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Port+Hardy/@50.719702,-127.497001,17z/data=!3m1!4b1!4m6!3m5!1s0x54647c2ccfb336e7:0x8bf97410bb5dc24d!8m2!3d50.719702!4d-127.4944261!16s%2Fg%2F11b7ycj3%5Fm?entry=ttu',
    mailingAddress: 'PO Box 400, Port Hardy, BC V0N 2P0',
    phone: '250-949-6323',
    fax: '250-949-6153',
    email: 'ServiceBC.PortHardy@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Powell River',
    physicalAddress: '6944 Alberni St, Powell River, BC V8A 2C1',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Powell+River/@49.8447831,-124.5255392,17z/data=!3m1!4b1!4m6!3m5!1s0x5487e6c50809142d:0x51555d5dab15dd32!8m2!3d49.8447831!4d-124.5229643!16s%2Fg%2F1tfkkwgl?entry=ttu',
    phone: '604-485-3622',
    fax: '604-485-3627',
    email: 'ServiceBC.PowellRiver@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Prince George',
    physicalAddress: '1044 - 5th Ave, Prince George, BC V2L 5G4',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Prince+George+%28ICBC+Driver+Licensing+-+no+Road+Tests%29/@53.9145488,-122.74755,17z/data=!3m1!4b1!4m6!3m5!1s0x538898e69ca3fea3:0x92bf8bdc460d000a!8m2!3d53.9145489!4d-122.7426791!16s%2Fg%2F11b5wklbkw?entry=ttu',
    phone: '250-565-4488',
    fax: '250-565-6638',
    email: 'ServiceBC.PrinceGeorge@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Prince Rupert',
    physicalAddress: '201 - 3rd Ave W, Prince Rupert, BC V8J 1L2',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Prince+Rupert/@54.3141402,-130.3268918,17z/data=!3m1!4b1!4m6!3m5!1s0x5472d56c93b24abb:0x2ec17cee45760898!8m2!3d54.3141403!4d-130.3220209!16s%2Fg%2F1tdjqv0f?entry=ttu',
    phone: '250-624-7415',
    fax: '250-624-7421',
    email: 'ServiceBC.PrinceRupert@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Princeton',
    physicalAddress: '10 - 136 Tapton Ave, Princeton',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Princeton/@49.4581604,-120.5092888,17z/data=!3m1!4b1!4m6!3m5!1s0x5483b3d3e3ca5557:0xf699daa681e55aff!8m2!3d49.4581604!4d-120.5067139!16s%2Fg%2F1pty%5Fn3f2?entry=ttu',
    mailingAddress: 'Box 9, Princeton, BC V0X 1W0',
    phone: '250-295-4600',
    fax: '250-295-3070',
    email: 'ServiceBC.Princeton@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Quesnel',
    physicalAddress: '102 - 350 Barlow Ave, Quesnel, BC V2J 2C2',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Quesnel/@52.9771858,-122.4992478,17z/data=!3m2!4b1!5s0x53870f5a4d9c0c79:0x65a80067ea0406e!4m6!3m5!1s0x53870f5a503cbcb3:0x55336639073ca388!8m2!3d52.9771859!4d-122.4943769!16s%2Fg%2F11b5wlb15r?entry=ttu',
    phone: '250-992-4315',
    fax: '250-992-4314',
    email: 'ServiceBC.Quesnel@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 12:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Revelstoke',
    physicalAddress: 'Room 104 - 1123 Second Street West,',
    mapUrl: 'https://goo.gl/maps/9jyBWWKdW5Qgprf56',
    mailingAddress: 'Box 380, Revelstoke, BC V0E 2S0',
    phone: '250-837-6981',
    fax: '250-837-4669',
    email: 'ServiceBC.Revelstoke@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Salmon Arm',
    physicalAddress: '850A - 16 St NE, Salmon Arm, BC V1E 2V1',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Salmon+Arm/@50.705534,-119.2709029,17z/data=!3m1!4b1!4m6!3m5!1s0x537ef5073f4e81e9:0x3670c8d4ead3b8d3!8m2!3d50.705534!4d-119.268328!16s%2Fg%2F1hc2w4bhz?entry=ttu',
    phone: '250-832-1611',
    fax: '250-832-1607',
    email: 'ServiceBC.SalmonArm@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Sechelt',
    physicalAddress: '5498 Wharf Avenue, Sechelt',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Sechelt/@49.4717791,-123.7570982,17z/data=!3m1!4b1!4m6!3m5!1s0x54863a6f11aec26d:0xf81e147ddd7c318b!8m2!3d49.4717791!4d-123.7545233!16s%2Fg%2F1tk8btf4?entry=ttu',
    mailingAddress: 'Box 950, Sechelt, BC V0N 3A0',
    phone: '604-885-5187',
    fax: '604-885-3710',
    email: 'ServiceBC.Sechelt@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Smithers',
    physicalAddress: '1020 Murray St, Smithers',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Smithers/@54.7774081,-127.1766511,17z/data=!3m1!4b1!4m6!3m5!1s0x5475097b4c88784d:0x5886a3d615df76fa!8m2!3d54.7774081!4d-127.1740762!16s%2Fg%2F1tt0qtj2?entry=ttu',
    mailingAddress: 'Bag 5000, Smithers, BC V0J 2N0',
    phone: '250-847-7207',
    fax: '250-847-7232',
    email: 'ServiceBC.Smithers@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Sparwood',
    physicalAddress: '96-101 Red Cedar Dr, Sparwood',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Sparwood/@49.7324523,-114.8874602,17z/data=!3m1!4b1!4m6!3m5!1s0x5365592661bd29ff:0x417906d799a4b994!8m2!3d49.7324523!4d-114.8848853!16s%2Fg%2F11b5wp0jn3?entry=ttu',
    mailingAddress: 'Box 1086, Sparwood, BC V0B 2G0',
    phone: '250-425-6890',
    fax: '250-425-7851',
    email: 'ServiceBC.Sparwood@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Squamish',
    physicalAddress: '1360 Pemberton Ave, Squamish',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Squamish/@49.7014889,-123.1548441,17z/data=!3m1!4b1!4m6!3m5!1s0x5486f83e085c11b3:0x6b9e750fc2839318!8m2!3d49.7014889!4d-123.1522692!16s%2Fg%2F1tk%5Fnzmf?entry=ttu',
    mailingAddress: 'Box 1008, Squamish, BC V8B 0A7',
    phone: '604-892-2400',
    fax: '604-892-2342',
    email: 'ServiceBC.Squamish@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Stewart',
    physicalAddress: 'Court House, 703 Brightwell Street, Stewart',
    mapUrl: 'https://goo.gl/maps/yedViFv7nSQcgdQY9',
    mailingAddress: 'Box 127, Stewart, BC V0T 1W0',
    phone: '250-636-2294',
    fax: '250-636-2678',
    email: 'ServiceBC.Stewart@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Surrey',
    physicalAddress: '200 - 10470 152nd Street, Surrey, BC V3R 0Y3',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Surrey+%28Limited+Services%29/@49.1927423,-122.8029109,17z/data=!3m2!4b1!5s0x5485d71273f0ea9b:0xb25b0d0f6a23d7ef!4m6!3m5!1s0x5485d71bca879d3d:0xa8fa69056bcd964!8m2!3d49.1927423!4d-122.800336!16s%2Fg%2F11g1sb2stt?entry=ttu',
    phone: '1-800-663-7867',
    email: 'ServiceBC.MVA@gov.bc.ca',
    hours: [
      'Monday to Friday 9 am to 4:30 pm',
      'Closed from 10 am to 10:15 am, 12 pm to 1 pm, 3 pm to 3:15 pm * Appointments are not available at this location',
    ],
    servicesIntro: 'This office only offers the following services:',
    availableServices: [
      {
        label: 'BC Services Card account setup',
        href: '#verifyid',
      },
      {
        label: 'BCeID registration',
        href: '#verifyid',
      },
      {
        label: 'Hazardous waste licence to transport applications',
        href: '#waste',
      },
      {
        label: 'Pesticide licence application',
        href: '#pesticide',
      },
    ],
  },
  {
    name: 'Terrace',
    physicalAddress: '101 - 3220 Eby St, Terrace, BC V8G 5K8',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Terrace/@54.518105,-128.6005249,17z/data=!3m1!4b1!4m6!3m5!1s0x547499ec82d0cd2b:0x7df821f9444cfdc4!8m2!3d54.518105!4d-128.59795!16s%2Fg%2F1tghp8d7?entry=ttu',
    phone: '250-638-6515',
    fax: '250-638-6519',
    email: 'ServiceBC.Terrace@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Trail',
    physicalAddress: '1520 Bay Ave, Trail, BC V1R 4B3',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Trail/@49.0946429,-117.7090327,17z/data=!3m1!4b1!4m6!3m5!1s0x5362d9f29fecb685:0x9818d7cee41ec0ab!8m2!3d49.0946429!4d-117.7064578!16s%2Fg%2F11b5wp6wsg?entry=ttu',
    phone: '250-364-0591',
    fax: '250-364-0561',
    email: 'ServiceBC.Trail@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
  },
  {
    name: 'Ucluelet',
    physicalAddress: 'Unit 5 - 1620 Peninsula Rd, Ucluelet',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Ucluelet/@48.9417194,-125.5501307,17z/data=!3m1!4b1!4m6!3m5!1s0x548973bd058f7cb1:0x85dc5b7f944ceca3!8m2!3d48.9417194!4d-125.5475558!16s%2Fg%2F11b5wlm4sv?entry=ttu',
    mailingAddress: 'Box 609, Ucluelet, BC V0R 3A0',
    phone: '250-726-7025',
    fax: '250-726-7211',
    email: 'ServiceBC.Ucluelet@gov.bc.ca',
    hours: ['Monday to Friday 10:30 am to 3 pm', 'Closed from 12:30 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Valemount',
    physicalAddress: '1300 4th Ave, Valemount',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Valemount/@52.83305,-119.2700299,17z/data=!3m1!4b1!4m6!3m5!1s0x5383a07ea75a2bcb:0x536b0b240a6367b6!8m2!3d52.83305!4d-119.267455!16s%2Fg%2F1v41%5F41s?entry=ttu',
    mailingAddress: 'Box 657, Valemount, BC V0E 2Z0',
    phone: '250-566-4448',
    fax: '250-566-4620',
    email: 'ServiceBC.Valemount@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Vancouver',
    physicalAddress: '7th Floor - 865 Hornby Street, Vancouver, BC V6Z 2G3',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Vancouver+%28Limited+Services%29/@49.2818669,-123.1258438,17z/data=!3m2!4b1!5s0x5486717ffa4badd1:0xd534c82d60826a10!4m6!3m5!1s0x5486718950b0bd45:0x6e8ea0b2222fd066!8m2!3d49.2818669!4d-123.1232689!16s%2Fg%2F11f6kv5bg9?entry=ttu',
    phone: '1-800-663-7867',
    email: 'ServiceBC.MVA@gov.bc.ca',
    hours: [
      'Monday to Friday 9 am to 4:30 pm',
      'Closed from 10 am to 10:15 am, 12 pm to 1 pm, 3 pm to 3:15 pm * Appointments are not available at this location',
    ],
    servicesIntro: 'This office only offers the following services:',
    availableServices: [
      {
        label: 'BC Services Card account setup',
        href: '#verifyid',
      },
      {
        label: 'BCeID registration',
        href: '#verifyid',
      },
      {
        label: 'Hazardous waste licence to transport applications',
        href: '#waste',
      },
      {
        label: 'Pesticide licence application',
        href: '#pesticide',
      },
    ],
  },
  {
    name: 'Vanderhoof',
    physicalAddress: '189 East Stewart Street,',
    mapUrl: 'https://goo.gl/maps/b2WweN4J3hyBuJy76',
    mailingAddress: 'Box 1459, Vanderhoof, BC V0J 3A0',
    phone: '250-567-6301',
    fax: '250-567-6303',
    email: 'ServiceBC.Vanderhoof@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm', 'Closed from 12 pm to 1 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Vernon',
    physicalAddress: '3201- 30 St, Vernon, BC V1T 9G3',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Vernon/@50.2655979,-119.2730343,17z/data=!3m2!4b1!5s0x537dd8e8462b3f77:0xb2514da76d26136f!4m6!3m5!1s0x537dd8e83902e8b3:0x7c4a7af217276cb0!8m2!3d50.2655979!4d-119.2704594!16s%2Fg%2F1thznkyz?entry=ttu',
    phone: '250-549-5511',
    fax: '250-549-5508',
    email: 'ServiceBC.Vernon@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
  {
    name: 'Victoria',
    physicalAddress: '403-771 Vernon Ave, Victoria',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Victoria/@48.4583433,-123.3794112,17z/data=!3m1!4b1!4m6!3m5!1s0x548f73a396e52105:0xb6e752ce6afe039d!8m2!3d48.4583433!4d-123.3768363!16s%2Fg%2F11b7ybfvjk?entry=ttu',
    mailingAddress: 'Box 9408 Stn Prov Govt, Victoria, BC V8W 9V1',
    phone: '250-387-6121',
    fax: '250-952-4124',
    email: 'ServiceBC.Victoria@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'ICBC Driver Licensing',
        href: '#icbc',
      },
    ],
  },
  {
    name: 'Williams Lake',
    physicalAddress: '104 - 540 Borland St, Williams Lake, BC V2G 1R8',
    mapUrl:
      'https://www.google.com/maps/place/Service+BC+Centre+Williams+Lake/@52.1302168,-122.1405855,17z/data=!3m2!4b1!5s0x5380a3765f9d6e73:0x87c11642b56e6cc9!4m6!3m5!1s0x5380a3765c2a35e1:0x514baa617d7a284c!8m2!3d52.1302168!4d-122.1380106!16s%2Fg%2F1tgtf55s?entry=ttu',
    phone: '250-398-4211',
    fax: '250-398-4208',
    email: 'ServiceBC.WilliamsLake@gov.bc.ca',
    hours: ['Monday to Friday 9 am to 4:30 pm'],
    servicesIntro: 'This office offers the following services:',
    availableServices: [
      {
        label: 'Popular services',
        href: '#services',
      },
    ],
    unavailableServices: [
      {
        label: 'Income assistance',
        href: '#income',
      },
    ],
  },
]

type Office = (typeof OFFICES)[number]
type SortColumn = 'location' | 'address' | 'hours' | 'services'
type SortDirection = 'asc' | 'desc'

function officeSearchText(office: Office) {
  return [
    office.name,
    office.physicalAddress,
    office.mailingAddress,
    office.phone,
    office.fax,
    office.email,
    ...office.hours,
    office.servicesIntro,
    ...office.availableServices.map((service) => service.label),
    ...(office.unavailableServices?.map((service) => service.label) ?? []),
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()
}

function officeAppointmentsAvailable(office: Office) {
  return !office.hours.some((line) =>
    line.includes('Appointments are not available at this location'),
  )
}

function sortValue(office: Office, column: SortColumn) {
  switch (column) {
    case 'location':
      return office.name
    case 'address':
      return [office.physicalAddress, office.mailingAddress, office.phone, office.email]
        .filter(Boolean)
        .join(' ')
    case 'hours':
      return office.hours.join(' ')
    case 'services':
      return [
        office.servicesIntro,
        ...office.availableServices.map((service) => service.label),
        ...(office.unavailableServices?.map((service) => service.label) ?? []),
      ].join(' ')
  }
}

export function meta() {
  // Used in the prerendered HTML for search engines.
  return [{ title: 'Service BC Locations' }, { name: 'description', content: PAGE_DESCRIPTION }]
}

export default function Locations() {
  const [search, setSearch] = useState('')
  const [sortColumn, setSortColumn] = useState<SortColumn>('location')
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc')

  const visibleOffices = useMemo(() => {
    const query = search.trim().toLowerCase()
    const results = query
      ? OFFICES.filter((office) => officeSearchText(office).includes(query))
      : [...OFFICES]

    results.sort((a, b) => {
      const comparison = sortValue(a, sortColumn).localeCompare(
        sortValue(b, sortColumn),
        undefined,
        {
          sensitivity: 'base',
        },
      )
      return sortDirection === 'asc' ? comparison : -comparison
    })

    return results
  }, [search, sortColumn, sortDirection])

  function toggleSort(column: SortColumn) {
    if (sortColumn === column) {
      setSortDirection((direction) => (direction === 'asc' ? 'desc' : 'asc'))
      return
    }

    setSortColumn(column)
    setSortDirection('asc')
  }

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

      <TextField
        className="locations-search"
        name="office-search"
        value={search}
        onChange={setSearch}
      />

      <div className="locations-table-wrapper">
        <table className="locations-table">
          <thead>
            <tr>
              <th scope="col">
                <ColumnSortButton
                  column="location"
                  label="Location"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={toggleSort}
                />
              </th>
              <th scope="col">
                <ColumnSortButton
                  column="address"
                  label="Address and contact details"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={toggleSort}
                />
              </th>
              <th scope="col">
                <ColumnSortButton
                  column="hours"
                  label="Hours"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={toggleSort}
                />
              </th>
              <th scope="col">
                <ColumnSortButton
                  column="services"
                  label="More information"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={toggleSort}
                />
              </th>
            </tr>
          </thead>
          <tbody>
            {visibleOffices.length === 0 ? (
              <tr>
                <td colSpan={4}>No offices match your search.</td>
              </tr>
            ) : (
              visibleOffices.map((office) => (
                <tr key={office.name}>
                  <th scope="row">{office.name}</th>
                  <td>
                    <p>
                      <strong>Physical address</strong>
                      <br />
                      <Link href={office.mapUrl ?? '#'}>{office.physicalAddress}</Link>
                    </p>
                    {office.mailingAddress ? (
                      <p>
                        <strong>Mailing address</strong>
                        <br />
                        {office.mailingAddress}
                      </p>
                    ) : null}
                    <p>
                      {office.phone ? (
                        <>
                          <strong>Phone:</strong> {office.phone}
                          <br />
                        </>
                      ) : null}
                      {office.fax ? (
                        <>
                          <strong>Fax:</strong> {office.fax}
                          <br />
                        </>
                      ) : null}
                      {office.email ? (
                        <Link href={`mailto:${office.email}`}>{office.email}</Link>
                      ) : null}
                    </p>
                  </td>
                  <td className="locations-hours-cell">
                    {office.hours.map((line) => (
                      <p key={line}>{line}</p>
                    ))}
                    <p className="locations-book-appointment">
                      <Button
                        size="small"
                        variant="primary"
                        isDisabled={!officeAppointmentsAvailable(office)}
                      >
                        Book an appointment
                      </Button>
                    </p>
                  </td>
                  <td>
                    <p>{office.servicesIntro}</p>
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
              ))
            )}
          </tbody>
        </table>
      </div>
    </>
  )
}

function ColumnSortButton({
  column,
  label,
  sortColumn,
  sortDirection,
  onSort,
}: {
  column: SortColumn
  label: string
  sortColumn: SortColumn
  sortDirection: SortDirection
  onSort: (column: SortColumn) => void
}) {
  const isActive = sortColumn === column

  return (
    <button
      type="button"
      className="locations-sort-button"
      onClick={() => onSort(column)}
      aria-sort={isActive ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none'}
      aria-label={
        isActive
          ? `Sort by ${label}, currently ${sortDirection === 'asc' ? 'ascending' : 'descending'}`
          : `Sort by ${label}`
      }
    >
      <span>{label}</span>
      <span className="locations-sort-icons" aria-hidden="true">
        <span className={isActive && sortDirection === 'asc' ? 'is-active' : undefined}>
          <SvgChevronUpIcon />
        </span>
        <span className={isActive && sortDirection === 'desc' ? 'is-active' : undefined}>
          <SvgChevronDownIcon />
        </span>
      </span>
    </button>
  )
}
