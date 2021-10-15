<template>
  <div>
    <v-overlay :value="setLoading">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'loading',
    event: 'update',
  },
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    setLoading: {
      get() {
        return this.loading
      },
    },
  },
}
</script>
