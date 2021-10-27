<template>
  <div>
    <v-card class="px-6 py-12 short-card" outlined>
      <h1 v-if="error.statusCode === 404">
        {{ pageNotFound }}
      </h1>
      <h1 v-else>{{ otherError }}</h1>
      <Btn class="mt-6" @click="homeUrl"> ホーム画面へ </Btn>
    </v-card>
  </div>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      pageNotFound: '404 Not Found',
      otherError: 'An error occurred',
    }
  },
  head() {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title,
    }
  },
  methods: {
    homeUrl() {
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
