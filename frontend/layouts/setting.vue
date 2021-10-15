<template>
  <v-app class="app-container">
    <v-main>
      <v-container>
        <v-card outlined>
          <v-toolbar flat>
            <v-btn large icon color="primary" @click="backSetting">
              <v-icon>mdi-arrow-left-circle</v-icon>
            </v-btn>
            <v-toolbar-title>{{ title }}</v-toolbar-title>
          </v-toolbar>
          <div class="pa-6">
            <Nuxt />
          </div>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      title: '',
      backUrl: '',
    }
  },
  created() {
    this.setListener()
  },
  methods: {
    setListener() {
      this.$nuxt.$on('updateHeader', this.setHeader)
    },
    setHeader(header) {
      this.title = header.title || ''
      this.backUrl = header.backUrl || '/setting'
    },
    backSetting() {
      this.$router.push({ path: this.backUrl })
    },
  },
}
</script>

<style scoped>
.app-container {
  background-color: #fff;
  background-image: url('/img/bg-sp.png');
  background-size: cover;
  background-position: top center;
}
</style>
