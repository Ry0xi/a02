<template>
  <v-card class="task-item" outlined>
    <v-card-title class="task-item-name">{{ taskName }}</v-card-title>
    <TaskCategoryList :categoryData="categoryData" :categories="categories" />

    <TaskDoneBtn v-if="!isDone" v-show="!hideDoneBtn" />
  </v-card>
</template>

<script>
export default {
  props: {
    taskName: {
      type: String,
    },
    categories: {
      type: Array,
    },
    isDone: {
      type: Boolean,
    },
    taskDate: {
      type: String,
      default: '未入力',
    },
    taskDetail: {
      type: String,
      default: '未入力',
    },
    categoryData: {
      type: Object,
    },
    // 完了ボタンを非表示にするかどうか
    hideDoneBtn: {
      type: Boolean,
      default: false,
    },
    notifications: {
      type: Boolean,
      default: true,
    },
    isAutoAddedTask: {
      type: Boolean,
      default: true,
    },
  },
}
</script>

<style lang="scss" scoped>
.task-item {
  padding: 6px 16px;

  &-name {
    font-size: 18px;
    margin: 5px 0;
    padding: 0;
  }
}
</style>
