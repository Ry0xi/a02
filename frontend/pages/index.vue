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
      tasks: null,
      taskData: null,
      loadingTask: false,
      categoryData: null,
      snackbarDelete: false,
    }
  },
  mounted() {
    this.updateHeader()
    this.getCategoryDataFromDB()
    this.getTasksFromDB()
  },
  methods: {
    async getTasksFromDB() {
      console.log('getTasksFromDB')
      this.loadingTask = true
      // タスクデータの取得
      await this.$db.task.toArray()
      .then((tasks) => {
        console.log('tasks >> 取得成功')
        console.log(tasks)

        // データを整形して保持
        let newData = {}
        tasks.forEach((task) => {
          const taskId = task.id
          delete task.id
          delete task.is_done
          newData[taskId] = task
        })
        // タスクデータの適用
        this.taskData = newData
      })
      .catch((e) => {
        console.log('tasks >> 取得失敗')
        console.log(e.message)
      })
      // タスクリストを取得
      await this.$db.task_date.toArray()
      .then(tasks => {
        this.tasks = tasks
      })

      this.loadingTask = false
    },
    async getCategoryDataFromDB() {
      console.log('getCategoryDataFromDB')

      // カテゴリを取得
      await this.$db.category.toArray()
      .then((categoryData) => {
        console.log('categoryData >> 取得成功')

        // データを整形して保持
        let newData = {}
        categoryData.forEach((category) => {
          newData[category.id] = {'name': category.name, 'color': category.color}
        })
        this.categoryData = newData
      })
      .catch((e) => {
        console.log('categoryData >> 取得失敗')
        console.log(e.message)
      })
    },
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
    // fetchTasks() {
    //   console.log('fetchTasks()')
    //   axios.get('/api/task/').then((response) => {
    //     console.log('タスク取得 >> 成功')
    //     console.log(response.data)

    //     // IDBに保存
    //     // this.$db.task.clear()
    //     // this.$db.task.bulkAdd(response.data)

    //   }).catch((e) => {
    //     console.log('タスク取得 >> 失敗')
    //   })
    // },
    async addTaskData(newTaskData) {
      // サーバーに追加する
      // this.$axios.post('/api/task/', newTaskData).then((response) => {
        
      // })

      // 【テスト】
      const newId = this.makeTmpId('task')
      newTaskData.id = newId

      // IDBに登録する
      this.$db.task.add(newTaskData).then(() => {
        console.log('タスク追加 >> 成功')

        this.$db.task_date.add({
          'task_id': newTaskData.id,
          'date': newTaskData.next_display_date,
          'is_done': false,
        }).then(() => this.getTasksFromDB())
      })
      
    },
    deleteTaskData(taskId) {
      // IDBから削除
      this.$db.task.delete(taskId).then(() => {
        console.log('task deleted.')

        this.$db.task_date
          .where('task_id')
          .equals(taskId)
          .delete().then(() => {
          console.log('task deleted.')
          // タスクデータの再読み込み
          this.getTasksFromDB()
        })
      })
      
      // 削除を通知
      this.snackbarDelete = true
    },
    updateTaskData(updatedData) {
      const taskId = updatedData.id
      delete updatedData.id

      this.$db.task.update(taskId, updatedData).then(() => {
        console.log('task updated.')
        // タスクデータの再読み込み
        this.getTasksFromDB()
      })

    },
    doneTask(taskDateId) {
      // IDBを更新
      this.$db.task_date.update(taskDateId, {'is_done': true}).then(() => {
        // タスクデータの再読み込み
        this.getTasksFromDB()
      })
    },
    updateCategoryData(updatedCategoryData) {
      // カテゴリデータを更新
      const targetId = updatedCategoryData.id
      delete updatedCategoryData.id

      this.$db.category.update(targetId, updatedCategoryData).then(() => {
        console.log('category updated.')
        // カテゴリデータの再読み込み
        this.getCategoryDataFromDB()
      })

    },
    addCategoryData(newCategoryData) {
      // カテゴリデータを追加
      // 【テスト】
      const newId = this.makeTmpId('category')
      newCategoryData.id = newId

      this.$db.category.add(newCategoryData).then(() => {
        console.log('category created.')
        // カテゴリデータの再読み込み
        this.getCategoryDataFromDB()
      })
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