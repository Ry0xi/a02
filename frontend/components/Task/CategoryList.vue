<!--
  @param
-->
<template>
  <ul class="task-category-list">
    <li class="task-category-list-item" v-for="category in categories" :key="category">
      <v-chip
        :color="categoryData[category]['color']"
      >{{categoryData[category]['name']}}</v-chip>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    categoryData: {
      type: Object,
      required: true
    },
    categories: {
      type: Array
    }
  }
}
</script>

<style lang="scss" scoped>
.task-category {
  &-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
    width: calc(100% - 36px);
    padding: 0;

    list-style: none;

    &-item {
      width: max-content;
      margin-bottom: 8px;
      margin-right: 8px;

      &:last-child {
        margin-right: 0;
      }
    }
  }
}
</style>