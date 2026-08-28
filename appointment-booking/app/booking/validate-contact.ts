// Email/phone validation for the review step contact fields.

export function isValidEmail(email: string): boolean {
  const trimmed = email.trim()
  return trimmed.length > 0 && /^[^@]+@[^@]+\.[^@]+$/.test(trimmed)
}

export function isValidPhone(phone: string): boolean {
  const normalized = phone.trim().replace(/[ ()]/g, '')
  return normalized.length > 0 && /^\+?1?[-.]?\d{3}[-.]?\d{3}[-.]?\d{4}$/.test(normalized)
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
