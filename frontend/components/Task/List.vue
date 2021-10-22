<!--
  shownTasks:         0 -> 全て、1 -> 未完了のタスクのみ、2 -> 完了のみ
  tasks:              {id, task_id, date, is_done}
  taskData:           タスクオブジェクトの配列
  categoryData:       各カテゴリのデータ。[categoryId(String)]: {'name': String, 'color': String}
  @task:done:         タスク完了時に発火するイベント。※TaskDoneBtnを参照
  @task:deleted:      タスクの削除ボタンを押した時に発火するイベント
  @task:updated:      タスクの保存ボタンを押した時に発火するイベント
  @category:updated:  カテゴリが更新されたときに発火するイベント
                      新しいカテゴリデータを返す。※TaskCategoryEditorを参照
  @category:created:  カテゴリが新規作成されたときに発火するイベント
                      新しいカテゴリデータを返す。※TaskCategoryEditorを参照
-->
<template>
  <ul class="task-list">
      <li class="task-list-item" v-for="task in tasks" :key="task.id">
        <TaskItem
          :id="'activator'+task.id"
          v-show="shownTasks == 0 || isShownTask(task)"
          :taskDateId="task.id"
          :taskName="taskData[task.task_id].name"
          :taskDate="taskData[task.task_id].date"
          :taskDetail="taskData[task.task_id].detail"
          :categories="taskData[task.task_id].categories"
          :isDone="task.is_done"
          :categoryData="categoryData"
          :hideDoneBtn="hideDoneBtn"
          @task:done="doneTask"
        />
        <TaskInfo
          :activator="'#activator'+task.id"
          :taskId="task.task_id"
          :taskName="taskData[task.task_id].name"
          :taskDate="taskData[task.task_id].date"
          :taskDetail="taskData[task.task_id].detail"
          :categories="taskData[task.task_id].categories"
          :isDone="task.is_done"
          :categoryData="categoryData"
          @task:deleted="deleteTask($event)"
          @task:updated="updateTask($event)"
          @category:updated="updateCategoryData($event)"
          @category:created="addCategoryData($event)"
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
    taskData: {
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

      const taskType = task.is_done ? 2 : 1
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
    },
    doneTask(taskId) {
      this.$emit('task:done', taskId)
    },
    updateCategoryData(updatedCategoryData) {
      this.$emit('category:updated', updatedCategoryData)
    },
    addCategoryData(newCategoryData) {
      this.$emit('category:created', newCategoryData)
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