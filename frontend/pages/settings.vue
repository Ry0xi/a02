<template>
  <p>settings</p>
</template>

<script>
export default {
  data() {
    return {
      header: {
        title: '設定'
      }
    }
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    }
  }
}
</script>