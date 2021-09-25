<template>
  <header>
    <v-container>
      <h1 class="common-header-title">{{ title }}</h1>
    </v-container>
  </header>
</template>

<script>
export default {
  props: {
    title: { type: String, default: '' }
  }
}
</script>

<style scoped>
.common-header-title {
  color: #434343;
  font-size: 26px;
}
</style>