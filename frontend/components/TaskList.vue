<!--
  shownTasks: 0 -> 全て、1 -> 未完了のタスクのみ、2 -> 完了のみ
-->
<template>
  <ul class="task-list">
      <li class="task-list-item" v-for="task in tasks" :key="task.id">
        <TaskItem
          v-if="isShownTask(task)"
          :taskName="task.name"
          :categories="task.categories"
          :isDone="task.isDone"
          :categoryData="categoryData"
        />
      </li>
  </ul>
</template>

<script>
export default {
  props: {
    shownTasks: {
      type: Number,
      default: 0
    },
    tasks: {
      type: Array
    },
    categoryData: {
      type: Object
    }
  },
  methods: {
    isShownTask: function(task) {
      // すべて表示する
      if (this.shownTasks === 0) {
        return true
      }

      const taskType = task.isDone ? 2 : 1
      if (this.shownTasks === taskType) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.task-list {
  list-style: none;
  padding: 0;

  &-item + &-item{
    margin-top: 16px;
  }
}
</style>