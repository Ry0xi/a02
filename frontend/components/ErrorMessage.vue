<template>
  <div class="error-message" v-if="message">
    {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      default: null,
    },
  },
}
</script>

<style lang="scss" scoped>
.error-message {
  margin-bottom: 28px;
  padding: 20px;
  font-size: 14px;
  border-radius: 20px;
  color: #fff;
  background-color: #f8535b;
}
</style>
