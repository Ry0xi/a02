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
  padding: 8px 16px;

  &-name {
    font-size: 1.25rem;
    padding: 0;
    margin: 8px 0;
  }
}
</style>