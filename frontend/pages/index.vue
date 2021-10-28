<template>
  <div class="page-home">
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
      // カテゴリデータを追加
      // サーバーに送信
      const sendData = {
        'category_name': newCategoryData.name,
        'color_code': newCategoryData.color,
      }

      // IDBに追加する処理
      const promiseAddCategoryToIDB = categoryData => {
        const data = {'id': categoryData.id, ...newCategoryData}

        return this.$db.category.add(data)
        .then(() => {
          console.log('カテゴリ新規作成(IDB) >> 成功')
        })
      }
      
      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // サーバーに追加する処理
        const promiseAddCategoryToServer = this.$axios.post('/api/category/', sendData)
        .then((response) => {
          console.log('カテゴリ新規作成(API) >> 成功')
          return response.data
        })

        promiseAddCategoryToServer
        .then(categoryData => promiseAddCategoryToIDB(categoryData))
        .then(() => {
          // カテゴリデータの再読み込み
          this.getCategoryDataFromDB()
        })
        .catch((e) => {
          console.log('カテゴリ新規作成(Online) >> 失敗')
          console.error(e.message)
        })

      } else {
        // オフラインの場合
        const newId = this.makeTmpId('category')
        promiseAddCategoryToIDB({'id': newId})
        .then(() => {
          // offline_categoryに登録
          return this.$db.offline_category.add({
            'category_id': newId,
            'type': 'create',
            'data': sendData,
          })
        })
        .then(() => {
          this.errorMessage = 'カテゴリ新規作成の同期に失敗しました。オンラインに復帰後同期します。'
          // カテゴリデータの再読み込み
          this.getCategoryDataFromDB()
        })
        .catch((e) => {
          console.log('カテゴリ新規作成(Offline) >> 失敗')
          console.error(e.message)
        })
      }
    },
    makeTmpId(type) {
      // 【追加系api通信が新規IDを返すようになるまで使用】仮の新規IDを生成
      let existIds = []
      if (type == 'category') {
        existIds = Object.keys(this.categoryData).map(id => Number(id))
      } else if (type == 'task') {
        existIds = this.tasks.map(task => task.task_id)
      } else {
        return
      }

      // 存在しているIDの最大値＋1
      let maxId = null
      if (existIds[0]) {
        maxId = existIds.reduce((a, b) => {
          return Math.max(a, b)
        })
        return maxId + 1
      } else {
        return 1
      }
    }
  }
}
</script>