import Axios, { AxiosResponse } from 'axios'
import ConfigHelper from '@/utils/config-helper'
import { FeedbackRequestObject } from '@/models/feedback'
import { addAxiosInterceptors } from '@/utils/interceptors'
const axios = addAxiosInterceptors(Axios.create())

export default class FeedbackService {
  public static async submitFeedback (feedbackBody: FeedbackRequestObject): Promise<AxiosResponse<any>> {
    return axios.post(`${ConfigHelper.getFeedbackURL()}/feedback`, feedbackBody)
  }
}
