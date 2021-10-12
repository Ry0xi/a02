<!--
categoryData:      カテゴリの情報をもつ配列
tasks:             全てのタスクのデータ
@task:created:     タスクの保存ボタンを押した時に発火するイベント
                   タスクオブジェクトを返す
                   {
                     'id': this.taskId,
                     'name': this.editableTaskName,
                     'categories': this.editableCategories,
                     'isDone': this.editableIsDone,
                     'date': this.editableTaskDate,
                     'detail': this.editableTaskDetail
                   }
@category:updated: カテゴリが更新されたときに発火するイベント
                   新しいカテゴリデータを返す。{ '0005': {'name': 'タスク名', 'color': '#XXXXXX'} }
@category:created: カテゴリが新規作成されたときに発火するイベント
                   新しいカテゴリデータを返す。{ '0005': {'name': 'タスク名', 'color': '#XXXXXX'} }
-->
<template>
  <div class="task-add-fab">
    <v-btn
      id="activator"
      fab
      fixed
      right
      elevation="8"
      color="primary"
      style="bottom: 64px;"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>

    <TaskCreate
      activator="#activator"
      :isDone="false"
      :categoryData="categoryData"
      :tasks="tasks"
      @task:created="createTask($event)"
      @category:updated="updateCategoryData($event)"
      @category:created="addCategoryData($event)"
    />
  </div>
</template>

<script>
export default {
  props: {
    categoryData: {
      type: Object,
      required: true
    },
    tasks: {
      type: Array,
      required: true
    }
  },
  methods: {
    createTask(createdTaskData) {
      this.$emit('task:created', createdTaskData)
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

</style>