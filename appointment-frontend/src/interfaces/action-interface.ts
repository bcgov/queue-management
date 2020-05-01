import { ActionContext } from 'vuex'

// Interface to define a Vuex Action
export interface ActionIF {
  (x: ActionContext<string, any>, y: any): void
}

export interface ActionBindingIF {
  (x: any): void
}
