import Axios, { AxiosResponse } from 'axios'
import { FeedbackRequestObject, FeedbackResponseObject } from '@/models/feedback'
import ConfigHelper from '@/utils/config-helper'
import { addAxiosInterceptors } from '@/utils/interceptors'
const axios = addAxiosInterceptors(Axios.create())

export default class FeedbackService {
  public static async submitFeedback (feedbackBody: FeedbackRequestObject): Promise<AxiosResponse<any>> {
    return axios.post('http://localhost:5001/api/v1/feedback', feedbackBody)
  }
}
