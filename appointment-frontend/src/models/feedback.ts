export interface FeedbackModel{
    feedbackType: string,
    feedbackHeader:string,
    feedbackMessage:string,
    name: string,
    email: string,
    phone: string,
    responseRequired: boolean
  }

export interface FeedbackRequestObject{
  variables: FeedbackRequestItem
}

export interface FeedbackRequestItem {
  engagement: FeedbackRequestKV,
  citizen_comments:FeedbackRequestKV,
  service_channel:FeedbackRequestKV,
  response: FeedbackRequestKV,
  citizen_name: FeedbackRequestKV,
  citizen_contact: FeedbackRequestKV,
  citizen_email: FeedbackRequestKV,
  entity_key: FeedbackRequestKV,
  service_date:FeedbackRequestKV,
  submit_date_time:FeedbackRequestKV,
  entered_by: FeedbackRequestKV
}

export interface FeedbackResponseObject{
  response_code: number
}

export interface FeedbackRequestKV{
  value?: string,
  type?:string
}
