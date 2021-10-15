<!--
パスワードフォーム
v-model:      入力値
noValidation: バリデーションメッセージを表示しない
-->
<template>
  <div>
    <v-text-field
      v-model="setPassword"
      :type="toggle.type"
      :prepend-inner-icon="noIcon ? '' : 'mdi-lock'"
      :append-icon="toggle.icon"
      outlined
      :label="label"
      :rules="form.rules"
      :hint="form.hint"
      @click:append="show = !show"
    >
    </v-text-field>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'password',
    event: 'input',
  },
  props: {
    password: String,
    label: {
      type: String,
      default: 'パスワード',
    },
    noValidation: {
      type: Boolean,
      default: false,
    },
    noIcon: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      show: false,
    }
  },
  computed: {
    setPassword: {
      get() {
        return this.password
      },
      set(value) {
        return this.$emit('input', value)
      },
    },
    toggle() {
      const icon = this.show ? 'mdi-eye' : 'mdi-eye-off'
      const type = this.show ? 'text' : 'password'
      return { icon, type }
    },
    form() {
      const msg = '8文字以上の半角英数字'
      const required = (v) => !!v || ''
      const format = (v) =>
        /^([a-zA-Z0-9]{8,})$/.test(v) || '半角英数字8文字以上で入力してください'

      const rules = this.noValidation ? [required] : [format]
      const hint = this.noValidation ? undefined : msg
      return { rules, hint }
    },
  },
}
</script>
