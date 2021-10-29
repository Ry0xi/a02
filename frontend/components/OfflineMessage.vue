<template>
  <div>
    <v-overlay :value="offline" absolute z-index="2">
      <v-card class="px-6 py-12 login-card" outlined light>
        <div>{{ message }}</div>
      </v-card>
    </v-overlay>
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      offline: !window.navigator.onLine,
    }
  },
}
</script>
