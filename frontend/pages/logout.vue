<template></template>
<script>
export default {
  mounted() {
    this.logout()
  },
  methods: {
    logout() {
      this.$auth.logout()
      this.$axios.post('/api/auth/logout/')
      this.$store.commit('revertCompletePreload')
      this.$router.push('/')
    },
  },
}
</script>
