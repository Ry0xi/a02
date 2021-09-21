<template>
  <v-bottom-navigation
    app
    color="secondary"
  >
    <v-btn v-for="menu in menus" :key="menu.title" :to="menu.to">
      <span>{{ menu.title }}</span>
      <v-icon>{{ menu.icon }}</v-icon>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
export default {
  data () {
    return {
      menus: [
        {
          icon: 'mdi-home',
          title: 'ホーム',
          to: '/'
        },
        {
          icon: 'mdi-format-list-bulleted',
          title: 'タスク',
          to: '/tasks'
        },
        {
          icon: 'mdi-calendar-month',
          title: 'カレンダー',
          to: '/calendar'
        },
        {
          icon: 'mdi-cog',
          title: '設定',
          to: '/settings'
        }
      ],
    }
  }
}
</script>