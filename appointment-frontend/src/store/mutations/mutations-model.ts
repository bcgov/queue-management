export const mutateName = (state: any, name: string) => {
  state.stateModel.stateText = name
}

export const mutateResource = (state: any, resource: object) => {
  state.resourceModel = resource
}
