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
      <ErrorMessage :message="message" />

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
      message: null,
    }
  },
  computed: {
    // ボタン名の切り替え
    btnName() {
      return this.isActive == 1 ? 'ログイン' : '登録'
    },
  },
  watch: {
    // タブの切替時にバリデーション、メッセージをリセット
    isActive() {
      this.reset()
    },
  },
  methods: {
    // バリデーション、メッセージのリセット
    reset() {
      this.$refs.SignInForm.reset()
      this.$refs.SignUpForm.reset()
      this.message = null
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
        this.auth()
      }
    },
    // 登録処理
    signUp() {
      if (this.$refs.SignUpForm.validate()) {
        this.$axios
          .post('/api/auth/register/', {
            email: this.user.email,
            password: this.user.password,
          })
          .then((response) => {
            this.auth('signup')
          })
          .catch((error) => {
            console.log(error)
            this.message = error.response.data
          })
      }
    },
    // 認証処理
    auth(type) {
      this.$auth
        .loginWith('local', {
          data: {
            email: this.user.email,
            password: this.user.password,
          },
        })
        .then(() => {
          if (type === 'signup') {
            // アカウント作成にユーザー名を登録
            this.$axios.post('/api/profile/', {
              username: this.user.name,
            })
          }
        })
        .catch((error) => {
          this.message = error.response.data
        })
    },
  },
}
</script>

<style lang="scss" scoped>
.login-card {
  max-width: 500px;
  margin: 0 auto;
}
.link-reset-password {
  margin: 50px 0 10px;
  font-size: 14px;
  text-align: center;
}
</style>
