import { ActionIF } from '@/interfaces/action-interface'

export const setName: ActionIF = ({ commit }, name): void => {
  commit('mutateName', name)
}

export const setResource: ActionIF = ({ commit }, resource): void => {
  commit('mutateResource', resource)
}
