// Libraries
import { Component, Vue } from 'vue-property-decorator'
// Interfaces
import { ResourceExampleIF } from '@/interfaces'
import { State } from 'vuex-class'
/**
 * Mixin for components to retrieve text/settings from json resource.
 */
@Component
export default class ResourceLookupMixin extends Vue {
  @State resourceModel!: Array<ResourceExampleIF>

  /**
   * Method to return the specified message
   *
   * @param id ID a number indicating the id of the resource to look up.
   */
  getName (id: number): string {
    const user: ResourceExampleIF | undefined = this.resourceModel && this.resourceModel.find(user => user.id === id)
    return user ? user.displayName : ''
  }

  /**
   * Method to return the specified display Name
   *
   * @param id ID a number indicating the id of the resource to look up.
   */
  getMessage (id: number): string {
    const user: ResourceExampleIF | undefined = this.resourceModel && this.resourceModel.find(user => user.id === id)
    return user ? user.message : ''
  }
}
