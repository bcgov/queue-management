import React from 'react'
import { Button as DSButton } from '@bcgov/design-system-react-components'

export function Button(props: React.ComponentPropsWithoutRef<typeof DSButton>) {
  return <DSButton {...props} />
}
