<template>
  <div class="page-tasks">
    <TaskAddFAB
      v-if="categoryData"
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
    <TaskListGroupByDate
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
  data() {
    return {
      header: {
        title: 'タスク一覧'
      },
      activeTab: 1,
      loadingTask: false,
      snackbarDelete: false,
      errorMessage: null,
    }
  },
  computed: {
    tasks() {
      return this.$store.getters.tasks
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
    fetchCategoryData() {
      console.log('fetchCategoryData()')

      // IDBに保存
      const promiseAddAllCategoryToIDB = dataToSave => {
        // IDBのデータを削除
        this.$db.category.clear()
        return this.$db.category.bulkAdd(dataToSave)
        .then(() => {
          console.log('カテゴリ一斉追加 >> 成功')
        })
      }

      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // サーバーからデータを取得する処理
        const promiseGetCategoryFromServer = this.$axios.get('/api/category/')
        .then((response) => {
          console.log('カテゴリ取得(API) >> 成功')
          return response.data
        })

        promiseGetCategoryFromServer
        .then(categories => {
          // IDB用にデータを整形
          let dataToSave = []
          categories.forEach((category) => {
            const categoryToSave = {
              'id': category.id,
              'name': category.category_name,
              'color': category.color_code,
            }
            dataToSave.push(categoryToSave)
          })
          return dataToSave
        })
        .then((categories) => promiseAddAllCategoryToIDB(categories))
        .then(() => this.getCategoryDataFromDB())
        .catch(e => {
          console.error('fetchCategoryData Error:', e.message)
        })

      } else {
        // オフラインの場合
        this.errorMessage = 'カテゴリデータの取得に失敗しました。ローカルデータを表示します。'
        this.getCategoryDataFromDB()
      }
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