export interface User {
  displayName: string
  email: string
  lastName: string
  telephone: string
  userId: number
  username: string
  sendEmailReminders: boolean
  sendSmsReminders: boolean
}

export interface UserUpdateBody {
  email: string
  telephone: string
  sendEmailReminders: boolean
  sendSmsReminders: boolean
}
