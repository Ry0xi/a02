<template>
  <div>
    <Calendar v-model="date">
      <template #activator="{ on }">
        <v-btn v-on="on" text>
          <v-icon class="mr-2" color="primary">mdi-calendar-month</v-icon>
          {{ formatDate }}
        </v-btn>
      </template>
    </Calendar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      header: {
        title: 'カレンダー',
      },
      date: new Date().toISOString().substr(0, 7),
    }
  },
  computed: {
    // 日付をフォーマット
    formatDate() {
      const dt = new Date(this.date)
      const year = dt.getFullYear()
      const month = dt.getMonth() + 1
      return `${year}年${month}月`
    },
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
  },
}
</script>
