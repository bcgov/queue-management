import axios from 'axios'

export function Axios(context) {
  let bearer = typeof context === 'object' ? context.state.bearer : context

  return(
    axios.create({
      baseURL: process.env.API_URL,
      withCredentials: true,
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${bearer}`
      }
    })
  )
}

export function adjustColor(col, amt) {
  col = col.split('#')[1]
  let num = parseInt(col,16)
  let r = (num >> 16) + amt
  if (r > 255) r = 255
  else if  (r < 0) r = 0
  let b = ((num >> 8) & 0x00FF) + amt
  if (b > 255) b = 255
  else if  (b < 0) b = 0
  let g = (num & 0x0000FF) + amt
  if (g > 255) g = 255
  else if (g < 0) g = 0
  return '#' + (g | (b << 8) | (r << 16)).toString(16)
}

export function searchNestedObject(searchObj, search) {
  let searchTerm = search.toLowerCase()
  let keys = Object.keys(searchObj)
  let l = keys.length
  for (let i = 0; i < l; i++) {
    let key = keys[i]
    let val = searchObj[key]
    if (typeof val === 'string') {
      if (val.toLowerCase().includes(searchTerm)) {
        return true
      }
    }
    if (typeof val === 'object' && val !== null) {
      let keys2 = Object.keys(val)
      let l2 = keys2.length
      for (let i2 = 0; i2 < l2; i2++) {
        let key2 = keys2[i2]
        let val2 = val[key2]
        if (typeof val2 === 'string') {
          if (val2.toLowerCase().includes(searchTerm)) {
            return true
          }
        }
      }
    }
  }
  return false
}
