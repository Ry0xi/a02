<template>
  <div class="page-home">
    <TaskAddFAB
      :categoryData="categoryData"
      @task:created="addTaskData($event)"
      @category:updated="updateCategoryData($event)"
      @category:created="addCategoryData($event)"
    />
    <Tab
      leftName="未完了"
      rightName="完了"
      v-model="activeTab"
      class="mb-8"
    />
    <ErrorMessage :message="errorMessage" />
    <!-- !loadingTaskがないとタスク削除後読み込み最中にレンダーしてしまう -->
    <TaskList
      v-if="!loadingTask && tasks && taskData && categoryData"
      :shownTasks="activeTab"
      :tasks="tasks"
      :taskData="taskData"
      :categoryData="categoryData"
      @task:deleted="deleteTaskData($event)"
      @task:updated="updateTaskData($event)"
      @task:done="doneTask"
      @category:updated="updateCategoryData($event)"
      @category:created="addCategoryData($event)"
      class="task-list-margin-bottom"
    />
    
    <!-- タスク削除時に表示されるお知らせ -->
    <v-snackbar
      v-model="snackbarDelete"
      timeout="2000"
    >
      タスクを削除しました。
    </v-snackbar>
  </div>
</template>

<script>
export default {
  middleware: 'update',
  data() {
    return {
      header: {
        title: 'ホーム'
      },
      activeTab: 1,
      loadingTask: false,
      snackbarDelete: false,
      errorMessage: null,
    }
  },
  computed: {
    tasks() {
      return this.$store.getters.tasksToday
    },
    taskData() {
      return this.$store.getters.taskData
    },
    categoryData() {
      return this.$store.getters.categoryData
    }
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
    addTaskData(newTaskData) {
      this.$store.dispatch('addTask', newTaskData)
      .then(() => {
        this.loadingTask = true
        this.$store.dispatch('replaceAllTaskStateWithTasksFromIDB')
        .then(() => this.loadingTask = false)
      })
    },
    deleteTaskData(taskId) {
      this.$store.dispatch('deleteTask', taskId)
      .then(() => {
        this.loadingTask = true
        this.$store.dispatch('replaceAllTaskStateWithTasksFromIDB')
        .then(() => this.loadingTask = false)
      })
    },
    updateTaskData(updatedData) {
      const taskId = updatedData.id
      delete updatedData.id

      this.$store.dispatch('updateTask', {
          taskId: taskId,
          data: updatedData,
        })
      .then(() => {
        this.loadingTask = true
        this.$store.dispatch('replaceAllTaskStateWithTasksFromIDB')
        .then(() => this.loadingTask = false)
      })
    },
    doneTask(data) {
      const taskDateId = data.taskDateId
      const taskFeedback = data.feedback

      const taskId = this.tasks.find(task => task.id === taskDateId).task_id

      this.$store.dispatch('completeTask', {
        taskDateId: taskDateId,
        taskId: taskId,
        feedback: taskFeedback,
      })
      .then(() => {
        this.loadingTask = true
        this.$store.dispatch('replaceAllTaskStateWithTasksFromIDB')
        .then(() => this.loadingTask = false)
      })
    },
    updateCategoryData(updatedCategoryData) {
      // カテゴリデータを更新
      const targetId = updatedCategoryData.id
      delete updatedCategoryData.id

      this.$store.dispatch('updateCategoryData', {
        categoryId: targetId,
        data: updatedCategoryData,
      })
      .then(() => this.$store.dispatch('replaceCategoryStateWithCategoryOnIDBCategory'))
    },
    addCategoryData(newCategoryData) {
      this.$store.dispatch('addCategoryData', newCategoryData)
      .then(() => this.$store.dispatch('replaceCategoryStateWithCategoryOnIDBCategory'))
    },
  }
}
</script>