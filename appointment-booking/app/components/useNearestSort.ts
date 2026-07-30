import { useState } from 'react'

export type NearestLocationStatus = 'idle' | 'loading' | 'active' | 'error'
export type Coordinates = { latitude: number; longitude: number }

// Shared geolocation + nearest-sort state for the directory and booking locations step.
export function useNearestSort() {
  const [nearestSort, setNearestSort] = useState(false)
  const [status, setStatus] = useState<NearestLocationStatus>('idle')
  const [userLocation, setUserLocation] = useState<Coordinates | null>(null)
  const [error, setError] = useState<string | null>(null)

  function clearNearestSort() {
    setNearestSort(false)
    setStatus('idle')
    setUserLocation(null)
    setError(null)
  }

  function toggleNearestSort() {
    if (nearestSort) {
      clearNearestSort()
      return
    }

    // Guard for SSR / browsers without geolocation — pin must not throw.
    if (typeof navigator === 'undefined' || !navigator.geolocation) {
      setStatus('error')
      setError('Your browser does not support location services.')
      return
    }

    setStatus('loading')
    setError(null)

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        })
        setNearestSort(true)
        setStatus('active')
      },
      (geoError) => {
        setStatus('error')
        setNearestSort(false)
        setUserLocation(null)
        setError(
          geoError.code === geoError.PERMISSION_DENIED
            ? 'Location access was denied. Allow location in your browser to sort by nearest office.'
            : 'Unable to determine your location. Please try again.',
        )
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 },
    )
  }

  return {
    nearestSort,
    status,
    userLocation,
    error,
    clearNearestSort,
    toggleNearestSort,
  }
}
