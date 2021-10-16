<template>
  <div>
    <Loading :loading="loading" />
    <v-form ref="passwordForm">
      <UserFormPassword
        v-model="user.password"
        noIcon
        noValidation
        label="現在のパスワード"
      />

      <UserFormPassword
        v-model="user.newPassword"
        noIcon
        label="新しいパスワード"
      />

      <ErrorMessage :message="message" />

      <Btn @click="updatePassword">パスワードを変更する</Btn>
    </v-form>
  </div>
</template>

<script>
export default {
  layout: 'setting',
  data() {
    return {
      header: {
        title: 'パスワードの設定',
        backUrl: '/setting',
      },
      loading: false,
      user: {
        password: '',
        newPassword: '',
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
    // パスワードの更新
    updatePassword() {
      this.message = null
      if (this.$refs.passwordForm.validate()) {
        this.loading = true
        this.$axios
          .put('/api/setting/reset_password', this.user)
          .then(() => {
            this.$router.push('/setting')
          })
          .catch((error) => {
            this.loading = false
            this.message = '更新できませんでした'
          })
      }
    },
  },
}
</script>
