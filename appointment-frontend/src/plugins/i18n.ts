import VueI18n, { LocaleMessages } from 'vue-i18n'
import Vue from 'vue'

Vue.use(VueI18n)

function loadLocaleMessages (): LocaleMessages {
  const locales = import.meta.glob('../locales/**/*.json', {
    eager: true,
    import: 'default'
  })

  const messages: LocaleMessages = {}

  Object.entries(locales).forEach(([path, content]) => {
    const matched = path.match(/\/([^/]+)\.json$/)

    if (matched) {
      messages[matched[1]] = content as LocaleMessages[string]
    }
  })

  return messages
}

const i18n = new VueI18n({
  locale: import.meta.env.VITE_I18N_LOCALE || 'en',
  fallbackLocale: import.meta.env.VITE_I18N_FALLBACK_LOCALE || 'en',
  messages: loadLocaleMessages()
})

export default i18n