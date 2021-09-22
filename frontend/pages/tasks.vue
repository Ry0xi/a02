<template>
  <p>tasks</p>
</template>

<script>
export default {
  data() {
    return {
      header: {
        title: 'タスク一覧'
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