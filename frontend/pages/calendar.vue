<template>
  <p>calendar</p>
</template>

<script>
export default {
  data() {
    return {
      header: {
        title: 'カレンダー'
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