export interface ServiceParent {
  serviceName: string
}

export interface Service {
  actualServiceInd: number
  deleted: string
  displayDashboardInd: number
  externalServiceName: string
  onlineAvailability: string
  onlineLink: string
  prefix: string
  serviceCode: string
  serviceDesc: string
  serviceId: number
  serviceName: string
  parentId: number,
  parent?: ServiceParent
}

export interface Services {
  services: Service[]
}

export interface Categories {
  categories: Service[]
}
