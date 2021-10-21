<template>
  <div>
    <v-card class="px-6 py-12 login-card" outlined>
      <div>認証情報が正しくありません。</div>
      <div>再度ログインしてください。</div>
      <Btn class="mt-6" @click="toLogin"> ログイン画面へ </Btn>
    </v-card>
  </div>
</template>

<script>
export default {
  layout: 'login',
  auth: false,
  methods: {
    toLogin() {
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
.login-card {
  max-width: 500px;
  margin: 0 auto;
}
</style>
