<template>
  <div>
    <Loading :loading="loading" />
    <v-form ref="EmailForm">
      <UserFormPassword
        v-model="user.password"
        noIcon
        noValidation
        label="パスワード"
      />

      <UserFormEmail v-model="user.email" noIcon label="新しいメールアドレス" />

      <ErrorMessage :message="message" />

      <Btn @click="updatePassword">メールアドレスを変更する</Btn>
    </v-form>
  </div>
</template>

<script>
export default {
  layout: 'setting',
  data() {
    return {
      header: {
        title: 'メールアドレスの設定',
        backUrl: '/setting',
      },
      loading: false,
      user: {
        password: '',
        email: '',
      },
      message: null,
    }
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header)
    },
    // メールアドレスの更新
    updatePassword() {
      this.messages = []
      if (this.$refs.EmailForm.validate()) {
        this.$axios
          .put('/api/setting/reset_email', this.user)
          .then(() => {
            this.$router.push('/setting')
          })
          .catch((error) => {
            this.message = '更新できませんでした'
          })
      }
    },
  },
}
</script>
