<template>
  <v-app class="app-container">
    <CommonHeader :title="title" />

    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>

    <GlobalNavBottom />
  </v-app>
</template>

<script>
import Header from '@/components/CommonHeader'

export default {
  components: {
    Header
  },
  data() {
    return {
      title: ''
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
    }
  }
}
</script>

<style scoped>
.v-application {
  background-color: var(--v-background-base, #777);
}
.app-container {
  background-image: url("/img/bg-sp-transparent.png");
  background-size: cover;
  background-position: top center;
}
</style>