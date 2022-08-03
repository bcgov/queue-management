export interface ServiceParent {
  serviceName: string
}

export interface Service {
  actualServiceInd: number
  deleted: string
  displayDashboardInd: number
  externalServiceName: string
  isDlkt: boolean
  onlineAvailability: string
  onlineLink: string
  parentId: number
  parent?: ServiceParent
  prefix: string
  serviceCode: string
  serviceDesc: string
  serviceId: number
  serviceName: string
}

export interface Services {
  services: Service[]
}

export interface Categories {
  categories: Service[]
}
