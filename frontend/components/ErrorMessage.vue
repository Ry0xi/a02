<template>
  <div class="error-message" v-if="setMessage.length">
    <div v-for="message in setMessage" :key="message">
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: [String, Array, Object],
      default: null,
    },
  },
  data() {
    return {
      setMessage: [],
    }
  },
  watch: {
    message() {
      this.setMessage = []

      const add = (value) => {
        if (Array.isArray(value)) {
          // 配列の場合
          value.forEach((element) => {
            this.setMessage.push(element)
          })
        } else if (typeof value === 'object') {
          // 連想配列の場合
          for (let i in value) {
            add(value[i])
          }
        } else if (typeof value === 'string') {
          // 文字列の場合
          this.setMessage.push(value)
        }
      }
      add(this.message)
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
