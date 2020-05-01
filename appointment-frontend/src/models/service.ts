/* eslint-disable camelcase */
export interface Service {
  actual_service_ind: number
  deleted: string
  display_dashboard_ind: number
  external_service_name: string
  online_availability: string
  online_link: string
  prefix: string
  service_code: string
  service_desc: string
  service_id: number
  service_name: string
  parent_id: number,
  parent?: ServiceParent
}

export interface Services {
  services: Service[]
}

export interface ServiceParent {
  service_name: string
}

export interface Categories {
  categories: Service[]
}
