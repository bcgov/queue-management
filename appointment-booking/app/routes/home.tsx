import { redirect } from 'react-router'

// Send visitors from / to the locations directory.
export function loader() {
  return redirect('/locations')
}
