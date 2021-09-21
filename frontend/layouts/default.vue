<template>
  <v-app>
    <v-main>
      <v-container class="main-container">
        <Nuxt />
      </v-container>
    </v-main>

    <GlobalNavBottom />
  </v-app>
</template>

<script>
export default {
  
}
</script>

<style scoped>
.main-container {
  background-color: #fff;
  background-image: url("/img/bg.png");
  background-size: contain;
  background-position: top left;
  background-repeat: repeat-x;
  min-height: 100%;
}
</style>