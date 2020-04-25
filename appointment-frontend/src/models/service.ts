/* eslint-disable camelcase */
export interface Service {
  actual_service_ind: number
  deleted: string
  display_dashboard_ind: number
  external_service_name: string
  online_availability: number
  online_link: string
  parent_id: number
  prefix: string
  service_code: string
  service_desc: string
  service_id: number
  service_name: string
}

export interface Services {
  services: Service[]
}
