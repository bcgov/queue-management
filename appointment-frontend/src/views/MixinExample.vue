<template>
  <div class="mixinExample">
    <h1>This is an about page that contains an example for a Mixin</h1>
    <h2>Testing Mixins: {{ sendMsg('My First Message')}}</h2>
  </div>
</template>
<script>
import { Component, Mixins } from 'vue-property-decorator'
import { CommonMixin } from '@/mixins'

@Component
export default class MixinExample extends Mixins(CommonMixin) {}
</script>
