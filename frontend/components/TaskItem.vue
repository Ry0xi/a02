<template>
  <v-card class="task-item">
    <v-card-title class="task-item-name">{{ taskName }}</v-card-title>
    <TaskCategoryList
      :categoryData="categoryData"
      :categories="categories"
    />
  </v-card>
</template>

<script>
export default {
  props: {
    taskName: {
      type: String
    },
    categories: {
      type: Array
    },
    isDone: {
      type: Boolean
    },
    categoryData: {
      type: Object
    }
  }
}
</script>

<style lang="scss" scoped>
.task-item {
  padding: 16px 16px 8px;

  &-name {
    font-size: 1.25rem;
  }
}
</style>