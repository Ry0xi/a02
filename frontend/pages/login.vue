<template>
  <div>
    <v-card class="px-6 py-12 login-card" outlined>
      <!-- タブボタン -->
      <Tab
        v-model="isActive"
        leftName="Login"
        rightName="Signup"
        width="200px"
        class="mb-8"
      />

      <!--ログインフォーム  -->
      <div v-show="isActive === 1">
        <v-form ref="SignInForm">
          <UserFormEmail v-model="user.email" noValidation />
          <UserFormPassword v-model="user.password" noValidation />
        </v-form>
      </div>

      <!-- サインアップフォーム -->
      <div v-show="isActive === 2">
        <v-form ref="SignUpForm">
          <UserFormName v-model="user.name" />
          <UserFormEmail v-model="user.email" />
          <UserFormPassword v-model="user.password" />
        </v-form>
      </div>

      <!-- エラーメッセージ -->
      <div v-show="message" class="error-message">{{ message }}</div>

      <!-- ボタン -->
      <Btn @click="submit">{{ btnName }}</Btn>

      <div class="link-reset-password">パスワードを忘れた方はこちら</div>
    </v-card>
  </div>
</template>

<script>
export default {
  layout: 'login',
  data() {
    return {
      isActive: 1,
      user: {
        email: '',
        password: '',
        name: '',
      },
      message: 'パスワードまたはメールアドレスが間違っています。',
    }
  },
  computed: {
    // ボタン名の切り替え
    btnName() {
      return this.isActive == 1 ? 'ログイン' : '登録'
    },
  },
  watch: {
    // タブの切替時にバリデーションをリセット
    isActive() {
      this.resetValidate()
    },
  },
  methods: {
    // バリデーションのリセット
    resetValidate() {
      this.$refs.SignInForm.reset()
      this.$refs.SignUpForm.reset()
    },
    submit() {
      if (this.isActive == 1) {
        this.signIn()
      } else {
        this.signUp()
      }
    },
    // ログイン処理
    signIn() {
      if (this.$refs.SignInForm.validate()) {
        console.log('signin')
      }
    },
    // 登録処理
    signUp() {
      if (this.$refs.SignUpForm.validate()) {
        console.log('signup')
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.login-card {
  max-width: 500px;
  margin: 0 auto;
}
.error-message {
  margin-bottom: 28px;
  padding: 20px;
  font-size: 14px;
  border-radius: 20px;
  color: #fff;
  background-color: #f8535b;
}
.link-reset-password {
  margin: 50px 0 10px;
  font-size: 14px;
  text-align: center;
}
</style>
