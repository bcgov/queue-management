import { Component, Vue } from 'vue-property-decorator'

/**
 * Mixin that provides some useful common utilities.
 */
@Component
export default class CommonMixin extends Vue {
  /**
   * This is an example mixin that will return a msg.
   *
   * @param msg The msg to return.
   */
  sendMsg (msg: string): string {
    return msg ? `${msg} - msg created by sendMsg mixin` : 'Error, no Message'
  }
}
