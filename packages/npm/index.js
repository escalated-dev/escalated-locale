const fs = require('fs')
const path = require('path')

const cache = new Map()

function readLocale(locale) {
  const normalized = locale || 'en'
  if (!cache.has(normalized)) {
    const filePath = path.join(__dirname, 'locales', `${normalized}.json`)
    cache.set(normalized, JSON.parse(fs.readFileSync(filePath, 'utf8')))
  }
  return cache.get(normalized)
}

function resolvePath(data, key) {
  return key.split('.').reduce((current, part) => {
    if (!current || typeof current !== 'object') {
      return undefined
    }
    return current[part]
  }, data)
}

function applyParams(value, params) {
  return Object.entries(params || {}).reduce(
    (current, [key, replacement]) => current.replaceAll(`{${key}}`, String(replacement)),
    value
  )
}

function getLocaleData(locale = 'en') {
  return readLocale(locale)
}

function t(key, locale = 'en', params = {}) {
  const localeData = getLocaleData(locale)
  const fallbackData = locale === 'en' ? localeData : getLocaleData('en')
  const value = resolvePath(localeData, key) ?? resolvePath(fallbackData, key)
  if (typeof value !== 'string') {
    return key
  }
  return applyParams(value, params)
}

module.exports = {
  getLocaleData,
  t,
}
