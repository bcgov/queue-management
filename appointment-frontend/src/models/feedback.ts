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
  citizenComments:FeedbackRequestKV,
  serviceChannel:FeedbackRequestKV,
  response: FeedbackRequestKV,
  citizenName: FeedbackRequestKV,
  citizenContact: FeedbackRequestKV,
  citizenEmail: FeedbackRequestKV,
  entityKey: FeedbackRequestKV,
  serviceDate:FeedbackRequestKV,
  submitDateTime:FeedbackRequestKV,
  enteredBy: FeedbackRequestKV
}

export interface FeedbackResponseObject{
  responseCode: number
}

export interface FeedbackRequestKV{
  value?: string,
  type?:string
}

   