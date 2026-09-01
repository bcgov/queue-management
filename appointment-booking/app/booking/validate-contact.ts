// Email/phone validation for the review step contact fields.

import { isValidPhoneNumber } from 'libphonenumber-js'

const DEFAULT_COUNTRY = 'CA'

export function isValidEmail(email: string): boolean {
  const trimmed = email.trim()
  return trimmed.length > 0 && /^[^@]+@[^@]+\.[^@]+$/.test(trimmed)
}

export function isValidPhone(phone: string): boolean {
  const trimmed = phone.trim()
  if (!trimmed) {
    return false
  }
  return isValidPhoneNumber(trimmed, DEFAULT_COUNTRY)
}

export type ContactValidation = {
  emailError: string | null
  phoneError: string | null
  sectionError: string | null
  /** At least one valid email or phone; for the confirm button on a later step. */
  hasValidContact: boolean
}

export function getContactValidation(email: string, phone: string): ContactValidation {
  const emailValue = email.trim()
  const phoneValue = phone.trim()
  const emailOk = isValidEmail(emailValue)
  const phoneOk = isValidPhone(phoneValue)

  return {
    // Empty field is fine when the other contact method is valid.
    emailError: emailValue && !emailOk ? 'Enter a valid email address.' : null,
    phoneError: phoneValue && !phoneOk ? 'Enter a valid phone number.' : null,
    sectionError:
      emailOk || phoneOk
        ? null
        : !emailValue && !phoneValue
          ? 'Enter an email address or phone number.'
          : 'Enter a valid email address or phone number.',
    hasValidContact: emailOk || phoneOk,
  }
}
