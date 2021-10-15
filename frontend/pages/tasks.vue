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

    <TaskListGroupByDate
      v-if="tasks && categoryData"
      :shownTasks="activeTab"
      :tasks="tasks"
      :categoryData="categoryData"
      @task:deleted="deleteTaskData($event)"
      @task:updated="updateTaskData($event)"
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
      tasks: null,
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

      await this.$db.task.toArray()
      .then((tasks) => {
        console.log('tasks >> 取得成功')
        console.log(tasks)

        let taskData = []
        tasks.forEach((task) => {
          const objTaskData = {
            'id': task.id,
            'name': task.title,
            'date': task.date,
            'detail': task.detail,
            'categories': task.category_ids,
            'isDone': task.is_done,
          }
          taskData.push(objTaskData)
        })

        this.tasks = taskData
      })
      .catch((e) => {
        console.log('tasks >> 取得失敗')
        console.log(e.message)
      })
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
        this.getTasksFromDB()
      })
      
    },
    deleteTaskData(taskId) {
      // IDBから削除
      this.$db.task.delete(taskId).then(() => {
        console.log('task deleted.')
        // タスクデータの再読み込み
        this.getTasksFromDB()
      })
            
      // 削除を通知
      this.snackbarDelete = true
    },
    updateTaskData(updatedData) {
      const taskId = updatedData.id
      delete updatedData.id
      const taskData = {
        'title': updatedData.name,
        'date': updatedData.date,
        'detail': updatedData.detail,
        'category_ids': updatedData.categories,
        'is_done': updatedData.isDone,
      }

      this.$db.task.update(taskId, taskData).then(() => {
        console.log('task updated.')
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
        existIds = this.tasks.map(task => task.id)
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