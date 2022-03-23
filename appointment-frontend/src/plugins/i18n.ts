import VueI18n, { LocaleMessages } from 'vue-i18n'
import Vue from 'vue'

Vue.use(VueI18n)

function loadLocaleMessages (): LocaleMessages {
  // the "i" on the end of the regex indicates case insensitivity, so the "A-Z" is redundant. Just use "a-z".
  const locales = require.context('../locales', true, /[a-z0-9-_,\s]+\.json$/i)
  const messages: LocaleMessages = {}
  locales.keys().forEach((key) => {
    // the "i" on the end of the regex indicates case insensitivity, so the "A-Z" is redundant. Just use "a-z".
    const matched = key.match(/([a-z0-9-_]+)\./i)
    if (matched && matched.length > 1) {
      const locale = matched[1]
      messages[locale] = locales(key)
    }
  })
  return messages
}

const i18n = new VueI18n({
  locale: process.env.VUE_APP_I18N_LOCALE || 'en',
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages: loadLocaleMessages()
})

export default i18n
