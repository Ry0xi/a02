<!--
メールフォーム
v-model:      入力値
noValidation: バリデーションメッセージを表示しない
-->
<template>
  <div>
    <v-text-field
      v-model="setEmail"
      :prepend-inner-icon="noIcon ? '' : 'mdi-email'"
      outlined
      :rules="form.rules"
      :label="label"
    >
    </v-text-field>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'email',
    event: 'input',
  },
  props: {
    email: String,
    label: {
      type: String,
      default: 'メールアドレス',
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
  computed: {
    setEmail: {
      get() {
        return this.email
      },
      set(value) {
        return this.$emit('input', value)
      },
    },
    form() {
      const required = (v) => !!v || ''
      const format = (v) =>
        /.+@.+\..+/.test(v) || 'メールアドレスが正しくありません'

      const rules = this.noValidation ? [required] : [format]
      return { rules }
    },
  },
}
</script>
