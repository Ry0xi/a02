<template>
  <v-app class="app-container">
    <!-- <CommonHeader :title="title" /> -->

    <v-main>
      <v-container class="mt-4">
        <Nuxt />
      </v-container>
    </v-main>

    <GlobalNavBottom />
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      title: '',
    }
  },
  created() {
    this.setListener()
  },
  methods: {
    // ページによってタイトルを変える
    setListener() {
      this.$nuxt.$on('updateHeader', this.setHeader)
    },
    setHeader(title) {
      this.title = title || ''
    },
  },
}
</script>
