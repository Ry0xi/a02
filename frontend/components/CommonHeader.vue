<template>
  <header>
    <v-container>
      <h1>{{ title }}</h1>
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

<style>

</style>