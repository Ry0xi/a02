<template>
  <div>
    <v-text-field
      v-model="setEmail"
      prepend-inner-icon="mdi-email"
      single-line
      outlined
      :rules="form.rules"
      label="メールアドレス"
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
    noValidation: {
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
