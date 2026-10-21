// Booking step 5: review details, contact, and confirm the appointment.
import { useEffect, useState } from 'react'
import { Button, InlineAlert, Text, TextField } from '@bcgov/design-system-react-components'
import { useNavigate } from 'react-router'

import { createAppointment, updateAppointment } from '~/api/appointments'
import { getCurrentUser, updateUser, type PublicUser } from '~/api/users'
import { useAuth } from '~/auth/auth-context'
import { addJsonToSession } from '~/auth/session'
import { SessionKeys } from '~/auth/session-keys'
import { useBooking } from '~/booking/booking-context'
import type { BookingConfirmation } from '~/booking/booking-store'
import { getContactValidation, isValidEmail, isValidPhone } from '~/booking/validate-contact'
import { BookingBackRow } from '~/components/BookingBackRow'
import { BookingContinueRow } from '~/components/BookingContinueRow'
import { BookingDetailCallout } from '~/components/BookingDetailCallout'
import { BookingStepProgress } from '~/components/BookingStepProgress'

const BOOKING_STEP = 5
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING = 'Review your appointment details before confirming.'

export function meta() {
  return [{ title: 'Review Appointment' }]
}

export default function ReviewPage() {
  const navigate = useNavigate()
  const { isReady: isAuthReady, isAuthenticated, session } = useAuth()
  const {
    isReady: isBookingReady,
    selectedService,
    selectedLocation,
    selectedSlot,
    modifyingAppointmentId,
    clearBookingAfterConfirm,
  } = useBooking()
  const isModifying = modifyingAppointmentId != null
  const [profile, setProfile] = useState<PublicUser | null>(null)
  // null = use profile/session default; string = user edited (including cleared).
  const [contactEmail, setContactEmail] = useState<string | null>(null)
  const [contactPhone, setContactPhone] = useState<string | null>(null)
  // null = use profile opt-in defaults until the user toggles a checkbox.
  const [sendEmailConfirmation, setSendEmailConfirmation] = useState<boolean | null>(null)
  const [sendSmsConfirmation, setSendSmsConfirmation] = useState<boolean | null>(null)
  const [contactTouched, setContactTouched] = useState(false)
  const [isConfirming, setIsConfirming] = useState(false)
  const [confirmError, setConfirmError] = useState<string | null>(null)

  useEffect(() => {
    if (!isAuthReady || !isAuthenticated) return

    let cancelled = false
    getCurrentUser()
      .then((user) => {
        if (!cancelled) setProfile(user)
      })
      .catch(() => {
        // Profile load failed; session email is still used when available.
      })

    return () => {
      cancelled = true
    }
  }, [isAuthReady, isAuthenticated])

  const email = (contactEmail ?? (profile?.email?.trim() || session?.email?.trim() || '')).trim()
  const phone = (contactPhone ?? (profile?.telephone?.trim() || '')).trim()
  const emailOk = isValidEmail(email)
  const phoneOk = isValidPhone(phone)
  const wantEmail = sendEmailConfirmation ?? Boolean(profile?.send_email_reminders)
  const wantSms = sendSmsConfirmation ?? Boolean(profile?.send_sms_reminders)
  const validation = getContactValidation(email, phone)

  async function handleConfirm() {
    setContactTouched(true)
    if (!validation.hasValidContact || !selectedService || !selectedLocation || !selectedSlot) {
      return
    }
    if (wantEmail && !emailOk) {
      setConfirmError('Enter a valid email address to receive email confirmation.')
      return
    }
    if (wantSms && !phoneOk) {
      setConfirmError('Enter a valid phone number to receive SMS confirmation.')
      return
    }
    if (!profile?.user_id) {
      setConfirmError('Unable to save your contact details. Please refresh and try again.')
      return
    }

    setConfirmError(null)
    setIsConfirming(true)

    try {
      // Save contact + opt-in flags first so the API can send confirmation after book.
      const userUpdate = {
        email,
        telephone: phone,
        send_email_reminders: wantEmail && emailOk,
        send_sms_reminders: wantSms && phoneOk,
      }
      // Local debug: confirm opt-in reached the API before book.
      console.info('[booking] saving confirmation preferences', userUpdate)
      await updateUser(profile.user_id, userUpdate)

      const payload = {
        office_id: selectedLocation.id,
        service_id: selectedService.id,
        // Office wall clock; API converts to UTC using the office timezone.
        start_time: `${selectedSlot.date}T${selectedSlot.startTime}:00`,
        end_time: `${selectedSlot.date}T${selectedSlot.endTime}:00`,
        appointment_draft_id: selectedSlot.draftAppointmentId,
      }

      if (modifyingAppointmentId != null) {
        await updateAppointment(modifyingAppointmentId, payload)
      } else {
        await createAppointment(payload)
      }

      const confirmation: BookingConfirmation = {
        kind: 'booked',
        bookedByName: session?.userFullName?.trim() || 'Appointment User',
        serviceName: selectedService.name,
        locationName: selectedLocation.name,
        locationAddress: selectedLocation.address || null,
        date: selectedSlot.date,
        startTime: selectedSlot.startTime,
        endTime: selectedSlot.endTime,
        sentEmail: wantEmail && emailOk,
        sentSms: wantSms && phoneOk,
      }
      addJsonToSession(SessionKeys.BookingConfirmation, confirmation)
      clearBookingAfterConfirm()
      navigate('/confirmation')
    } catch (err) {
      const expired = err instanceof Error && err.message === 'Session expired'
      setConfirmError(
        expired
          ? 'Your session has expired. Please sign in again to continue.'
          : err instanceof Error
            ? err.message
            : 'Unable to book this appointment. Please try again.',
      )
    } finally {
      setIsConfirming(false)
    }
  }

  const stepProgress = (
    <BookingStepProgress
      step={BOOKING_STEP}
      stepCount={BOOKING_STEP_COUNT}
      heading={BOOKING_STEP_HEADING}
    />
  )

  // Wait until sessionStorage restore finishes so we do not flash the wrong screen.
  if (!isAuthReady || !isBookingReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading booking…</Text>
      </div>
    )
  }

  if (!selectedService || !selectedLocation || !selectedSlot) {
    return (
      <>
        {stepProgress}
        <InlineAlert variant="warning" title="Start your booking">
          Please go back to the services page and start by selecting a service, then a location.
        </InlineAlert>
        <div className="booking-nav-row">
          <Button
            type="button"
            onPress={() => navigate(isModifying ? '/appointments' : '/services')}
          >
            {isModifying ? 'My appointments' : 'Go to services'}
          </Button>
        </div>
      </>
    )
  }

  if (!isAuthenticated) {
    return (
      <>
        {stepProgress}
        <InlineAlert variant="warning" title="Sign in to continue">
          Please sign in before reviewing your appointment.
        </InlineAlert>
        <div className="booking-nav-row">
          <Button type="button" onPress={() => navigate('/login')}>
            Go to login
          </Button>
        </div>
      </>
    )
  }

  return (
    <>
      <h1 className="sr-only">Review Appointment</h1>
      {stepProgress}

      <BookingDetailCallout
        selectedService={selectedService}
        selectedLocation={selectedLocation}
        selectedSlot={selectedSlot}
      />

      <section className="review-contact" aria-labelledby="review-contact-heading">
        <h2 id="review-contact-heading">Contact details</h2>
        <p className="review-contact-intro">
          Provide your contact information and choose how you want to receive confirmation.
        </p>

        <TextField
          label="Email"
          type="email"
          name="email"
          value={email}
          onChange={(value) => {
            setContactEmail(value)
            setContactTouched(true)
          }}
          isInvalid={contactTouched && !!validation.emailError}
          errorMessage={contactTouched ? (validation.emailError ?? undefined) : undefined}
          // BC DS TextField only shows errorMessage when isInvalid is also set.
        />
        <label className="review-contact-opt-in">
          <input
            type="checkbox"
            name="send_email_confirmation"
            checked={wantEmail && emailOk}
            disabled={!emailOk}
            onChange={(event) => {
              setSendEmailConfirmation(event.target.checked)
              setContactTouched(true)
            }}
          />
          <span>Send confirmation and reminders by email</span>
        </label>

        <TextField
          label="Phone number"
          type="tel"
          name="phone"
          value={phone}
          onChange={(value) => {
            setContactPhone(value)
            setContactTouched(true)
          }}
          isInvalid={contactTouched && !!validation.phoneError}
          errorMessage={contactTouched ? (validation.phoneError ?? undefined) : undefined}
        />
        <label className="review-contact-opt-in">
          <input
            type="checkbox"
            name="send_sms_confirmation"
            checked={wantSms && phoneOk}
            disabled={!phoneOk}
            onChange={(event) => {
              setSendSmsConfirmation(event.target.checked)
              setContactTouched(true)
            }}
          />
          <span>Send confirmation and reminders by SMS text</span>
        </label>

        <InlineAlert
          variant="warning"
          title="By providing your phone number above, you consent to receiving informational text messages from the Government of British Columbia. Text STOP to cancel."
        />

        {contactTouched && validation.sectionError ? (
          // Shown when both fields are empty; individual field errors do not cover that case.
          <p className="review-contact-section-error" role="alert">
            {validation.sectionError}
          </p>
        ) : null}
      </section>

      {confirmError ? (
        <div className="review-confirm-error" role="alert">
          <InlineAlert variant="danger" title="Unable to book this appointment">
            {confirmError}
          </InlineAlert>
          {confirmError.includes('sign in again') ? (
            <div className="booking-nav-row">
              <Button type="button" onPress={() => navigate('/login')}>
                Sign in again
              </Button>
            </div>
          ) : null}
        </div>
      ) : null}

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/datetime')} />
        <BookingContinueRow
          label={isConfirming ? 'Confirming…' : 'Confirm appointment'}
          isDisabled={isConfirming}
          onContinue={() => void handleConfirm()}
        />
      </div>
    </>
  )
}
