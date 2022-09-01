export interface TimeSlots {
  dayOfWeek: string[]
  endTime: string
  startTime: string
  noOfSlots: number
  dayStr?: string
  endTimeStr?: string
  startTimeStr?: string
}

export interface TimeZone {
  timezoneId: number
  timezoneName: string
}

export interface Office {
  appointmentDuration: number
  appointmentsDaysLimit: number
  appointmentsEnabledInd: boolean
  civicAddress: string
  disableOnlineAppointment: boolean
  examsEnabledInd: boolean
  latitude: number
  longitude: number
  maxPersonAppointmentPerDay: number
  officeAppointmentMessage: string
  officeId: number
  officeName: string
  officeNumber: number
  sbId: number
  telephone: string
  timeslots: TimeSlots[]
  timezone: TimeZone
  onlineStatus: string
  externalMapLink: string,
  checkInNotification: number,
  checkInReminderMsg: Text,
  automaticReminderAt: number,
  currentlyWaiting: number,
  digitalSignageMessage: number,
  digitalSignageMessage1: Text,
  digitalSignageMessage2: Text,
  digitalSignageMessage3: Text,
  showCurrentlyWaitingBottom: number,
}

export interface Offices {
  offices: Office[]
}
