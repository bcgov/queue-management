import axios from 'axios'
import config from './../../../config'

export function Axios (context) {
  const bearer = typeof context === 'object' ? context.state.bearer : context

  return (
    axios.create({
      baseURL: config.APP_API_URL,
      withCredentials: true,
      headers: {
        Accept: 'application/json',
        Authorization: `Bearer ${bearer}`
      }
    })
  )
}

export function adjustColor (col, amt) {
  col = col.split('#')[1]
  const num = parseInt(col, 16)
  let r = (num >> 16) + amt
  if (r > 255) r = 255
  else if (r < 0) r = 0
  let b = ((num >> 8) & 0x00FF) + amt
  if (b > 255) b = 255
  else if (b < 0) b = 0
  let g = (num & 0x0000FF) + amt
  if (g > 255) g = 255
  else if (g < 0) g = 0
  return '#' + (g | (b << 8) | (r << 16)).toString(16)
}

export function searchNestedObject (searchObj, search) {
  const searchTerm = search.toLowerCase()
  const keys = Object.keys(searchObj)
  const l = keys.length
  for (let i = 0; i < l; i++) {
    const key = keys[i]
    const val = searchObj[key]
    if (checkStringValMatch(val, searchTerm)) {
      return true
    }
    if (typeof val === 'object' && val !== null) {
      const keys2 = Object.keys(val)
      const l2 = keys2.length
      for (let i2 = 0; i2 < l2; i2++) {
        const key2 = keys2[i2]
        const val2 = val[key2]
        if (checkStringValMatch(val2, searchTerm)) {
          return true
        }
      }
    }
  }
  return false
}

function checkStringValMatch (val: any, searchTerm: any): boolean {
  if (typeof val === 'string') {
    if (val.toLowerCase().includes(searchTerm)) {
      return true
    }
  }
  return false
}
