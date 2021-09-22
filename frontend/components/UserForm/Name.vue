<template>
  <div>
    <v-text-field
      v-model="setName"
      prepend-inner-icon="mdi-account-circle"
      single-line
      outlined
      :rules="rules"
      :counter="max"
      label="ユーザー名"
    >
    </v-text-field>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'name',
    event: 'input',
  },
  props: {
    name: String,
  },
  data() {
    const max = 30
    return {
      max,
      rules: [
        (v) => !!v || 'ユーザー名を入力してください',
        (v) => (!!v && max >= v.length) || `${max}文字以内で入力してください`,
      ],
    }
  },
  computed: {
    setName: {
      get() {
        return this.name
      },
      set(value) {
        return this.$emit('input', value)
      },
    },
  },
}
</script>
