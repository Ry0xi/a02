<!--
  clearable:    チップを削除できるかどうか
  categories:   表示するカテゴリの配列
  categoryData: 表示するカテゴリに関する配列
  @click:clear: チップを削除した際に発火するイベント。カテゴリIDを返す
-->
<template>
  <ul class="task-category-list">
    <li class="task-category-list-item" v-for="category in shownCategories" :key="category">
      <v-chip
        :close="clearable"
        :color="categoryData[category]['color']"
        @click:close="deleteCategory(category)"
      >
        {{categoryData[category]['name']}}
      </v-chip>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    clearable: {
      type: Boolean,
      default: false
    },
    categoryData: {
      type: Object,
      required: true
    },
    categories: {
      type: Array
    }
  },
  data() {
    return {
      shownCategories: this.categories
    }
  },
  watch: {
    categories: {
      handler: function(dataAfter, dataBefore) {
        this.shownCategories = dataAfter
      },
      deep: true
    }
  },
  methods: {
    deleteCategory(categoryId) {
      this.$emit('click:clear', categoryId)
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