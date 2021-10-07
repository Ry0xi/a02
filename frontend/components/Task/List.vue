<!--
  shownTasks: 0 -> 全て、1 -> 未完了のタスクのみ、2 -> 完了のみ
  tasks: {'id': String, 'name': String, 'categories': Array, 'isDone': Boolean}の配列
  categoryData: 各カテゴリのデータ。[categoryId(String)]: {'name': String, 'color': String}
-->
<template>
  <ul class="task-list">
      <li class="task-list-item" v-for="task in tasks" :key="task.id">
        <TaskItem
          :id="'activator'+task.id"
          v-show="shownTasks == 0 || isShownTask(task)"
          :taskName="task.name"
          :taskDate="task.date"
          :taskDetail="task.detail"
          :categories="task.categories"
          :isDone="task.isDone"
          :categoryData="categoryData"
          :hideDoneBtn="hideDoneBtn"
        />
        <TaskInfoDialog
          :activator="'#activator'+task.id"
          :taskId="task.id"
          :taskName="task.name"
          :taskDate="task.date"
          :taskDetail="task.detail"
          :categories="task.categories"
          :isDone="task.isDone"
          :categoryData="categoryData"
          @task:deleted="deleteTask($event)"
          @task:updated="updateTask($event)"
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
    },
    hideDoneBtn: {
      type: Boolean,
      default: false
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
    },
    deleteTask: function(taskId) {
      this.$emit('task:deleted', taskId)
    },
    updateTask: function(updatedData) {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      this.$emit('task:updated', updatedData)
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