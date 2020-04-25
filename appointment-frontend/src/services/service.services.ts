import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { EmptyResponse } from '@/models/global'
import { addAxiosInterceptors } from '@/utils/interceptors'

const axios = addAxiosInterceptors(Axios.create())

export default class InvitationService {
  /**
  public static async createInvitation (invitation: CreateRequestBody): Promise<AxiosResponse<Invitation>> {
    return axios.post(`${ConfigHelper.getAppAPIUrl()}/invitations`, invitation)
  }

  public static async resendInvitation (invitation: Invitation): Promise<AxiosResponse<Invitation>> {
    return axios.patch(`${ConfigHelper.getAppAPIUrl()}/invitations/${invitation.id}`, invitation)
  }

  public static async deleteInvitation (invitationId: number): Promise<AxiosResponse<Invitation>> {
    return axios.delete(`${ConfigHelper.getAppAPIUrl()}/invitations/${invitationId}`)
  }

  public static async validateToken (token: string): Promise<AxiosResponse<EmptyResponse>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/invitations/tokens/${token}`)
  }

  public static async acceptInvitation (token: string): Promise<AxiosResponse<Invitation>> {
    return axios.put(`${ConfigHelper.getAppAPIUrl()}/invitations/tokens/${token}`, {})
  }
  **/

  public static async validateToken (token: string): Promise<AxiosResponse<EmptyResponse>> {
    return axios.get(`${ConfigHelper.getAppAPIUrl()}/invitations/tokens/${token}`)
  }
}
