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
    this.fetchTasks()
    this.fetchCategoryData()
  },
  methods: {
    getTasksFromDB() {
      console.log('getTasksFromDB()')
      this.loadingTask = true

      // IDBからタスクを取得
      const promiseTaskData = this.$db.task.toArray()
      .then((tasks) => {
        console.log('Got tasks from table: task')

        // データを整形して保持
        let newData = {}
        tasks.forEach((task) => {
          const taskId = task.id
          delete task.id
          newData[taskId] = task
        })
        // タスクデータの適用
        this.taskData = newData
      })
      // タスクリストを取得
      const promiseTaskDate = this.$db.task_date.toArray()
      .then(tasks => {
        console.log('Got tasks from table: task_date.')
        this.tasks = tasks
      })

      Promise.all([promiseTaskData, promiseTaskDate])
      .then(() => {
        this.loadingTask = false
      })
    },
    getCategoryDataFromDB() {
      console.log('getCategoryDataFromDB()')

      // IDBからカテゴリを取得
      this.$db.category.toArray()
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
        console.error(e.message)
      })
    },
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
    fetchTasks() {
      console.log('fetchTasks()')
      // サーバーから未完了のタスクデータを取得し、保存する
      const promiseTask = this.$axios.get('/api/task/').then(response => response.data)
      .then(tasks => {
        console.log('promiseTask１')
        console.log('タスク取得(API) >> 成功')
        // IDBからタスクを削除
        return this.$db.task.clear()
        .then(() => {
          console.log('promiseTask２')
          // タスクデータをIDBに保存
          return this.$db.task.bulkAdd(tasks).then(() => {
            console.log('promiseTask３')
            console.log('タスク保存(IDB) >> 成功')
            return tasks
          }).catch((e) => {
            console.log('タスク保存(IDB) >> 失敗')
            console.error(e.message)
          })
        })
        .catch((e) => {
          console.log('タスク(IDB)削除 >> 失敗')
        })
      })

      // サーバーから完了済のタスクデータを取得する
      const promiseHistory = this.$axios.get('/api/history/')
      .then(response => response.data)
      .then(history => {
        console.log('promiseHistory１')
        console.log('ヒストリー取得(API) >> 成功')
        return history
      })

      // task_dateを削除する
      const promiseClearTaskDate = this.$db.task_date.clear()

      // task_dateにタスクリストを追加する
      const promiseAddTaskDate = (tasks, history) => {
        console.log('promiseAddTaskDate１')
        // データを整形
        let newTaskData = []
        tasks.forEach(task => {
          const taskData = {
            'task_id': task.id,
            'date': task.next_display_date,
            'is_done': false,
          }
          newTaskData.push(taskData)
        })
        history.forEach((task) => {
          const taskData = {
            'date': task.completed_date,
            'is_done': true,
            'feedback': task.feedback,
            'task_id': task.task_id,
          }
          newTaskData.push(taskData)
        })
        // IDBに保存
        return this.$db.task_date.bulkAdd(newTaskData).then(() => {
          console.log('タスクリスト保存(IDB) >> 成功')
        }).catch(e => {
          console.log('タスクリスト保存(IDB) >> 失敗')
          console.error(e.message)
        })
      }


      Promise.all([promiseTask, promiseHistory])
      .then(arrays => {
        return promiseClearTaskDate
        .then(() => {
          console.log('promiseClearTaskDate１')
          return arrays
        })
      })
      .then(arrays => {
        return promiseAddTaskDate(arrays[0], arrays[1])
      })
      .then(() => this.getTasksFromDB())
      .catch((e) => {
        console.error('fetchTaskData Error: '+e.message)
      })
    },
    addTaskData(newTaskData) {
      // サーバーに追加する
      this.$axios.post('/api/task/', newTaskData).then((response) => {
        console.log('タスク追加(API) >> 成功')

        // IDBに登録する
        this.$db.task.add(response.data).then(() => {
          console.log('タスク追加(IDB1) >> 成功')
        }).catch((e) => {
          console.log('タスク追加(IDB) >> 失敗')
          console.error(e.message)
        }).then(() => {
          // データを整形
          let newData = {
            'task_id': response.data.id,
            'date': response.data.next_display_date,
            'is_done': false,
          }
          this.$db.task_date.add(newData).then(() => {
            this.getTasksFromDB()
          })
        })

      }).catch((e) => {
        console.log('タスク追加(API) >> 失敗')
        console.error(e.message)
      })
    },
    deleteTaskData(taskId) {
      // サーバーに送信
      this.$axios.delete('/api/task/'+String(taskId)+'/').then(() => {
        console.log('タスク削除(API) >> 成功')

        // IDBから削除
        this.$db.task.delete(taskId).then(() => {
          console.log('タスク削除(IDB)1 >> 成功')

          this.$db.task_date
          .where('task_id')
          .equals(taskId)
          .delete().then(() => {
            console.log('タスク削除(IDB)2 >> 成功')
            // 削除を通知
            this.snackbarDelete = true
            // タスクデータの再読み込み
            this.getTasksFromDB()
          })
        }).catch((e) => {
          console.log('タスク削除(IDB) >> 失敗')
        })

      }).catch((e) => {
        console.log('タスク削除(API) >> 失敗')
        console.error(e.message)
      })
    },
    updateTaskData(updatedData) {
      const taskId = updatedData.id
      delete updatedData.id
      
      // サーバーに送信
      this.$axios.put('/api/task/'+String(taskId)+'/', updatedData).then(() => {
        console.log('タスク更新(API) >> 成功')

        // IDBで更新
        this.$db.task.update(taskId, updatedData).then(() => {
          console.log('タスク更新(IDB) >> 成功')
          // タスクデータの再読み込み
          this.getTasksFromDB()
        }).catch((e) => {
          console.log('タスク更新(IDB) >> 失敗')
          console.error(e.message)
        })

      }).catch((e) => {
        console.log('タスク更新(API) >> 失敗')
        console.error(e.message)
      })
    },
    doneTask(data) {
      const taskDateId = data.taskDateId
      const taskFeedback = data.feedback

      const taskId = this.tasks.find(task => task.id === taskDateId).task_id

      const promiseCompleteTask = this.$axios.put('/api/task-completed-task/'+String(taskId)+'/', {'feedback': taskFeedback})
      const promiseAddHistory = this.$axios.post('/api/task-completed-history/', {'task_id': taskId, 'feedback': taskFeedback})
      
      // サーバーに送信
      Promise.all([promiseCompleteTask, promiseAddHistory]).then((response) => {
        console.log('タスク完了(API) >> 成功')
        console.log(response)

        // IDBを更新
        this.$db.task_date.update(taskDateId, {'is_done': true, 'feedback': taskFeedback})
        .then(() => {
          console.log('タスク完了(IDB) >> 成功')
          // タスクデータの再読み込み
          this.getTasksFromDB()
        })
        .catch((e) => {
          console.log('タスク完了(IDB) >> 失敗')
          console.error(e.message)
        })

      }).catch((e) => {
        console.log('タスク完了(API) >> 失敗')
        console.error(e.message)
      })
    },
    fetchCategoryData() {
      // サーバーからカテゴリデータを取得し、IDBを更新する
      console.log('fetchCategoryData()')

      // サーバーからデータを取得
      this.$axios.get('/api/category/').then((response) => {
        console.log('カテゴリ取得(API) >> 成功')
        console.log(response.data)

        // IDB用にデータを整形
        const dataToSave = []
        response.data.forEach((category) => {
          const categoryToSave = {
            'id': category.id,
            'name': category.category_name,
            'color': category.color_code,
          }
          dataToSave.push(categoryToSave)
        })
        console.log('カテゴリデータ整形 >> 完了')

        // IDBのデータを削除
        this.$db.category.clear().catch((e) => {
          console.log('カテゴリ削除 >> 失敗')
          console.error(e.message)
        })

        // IDBに保存
        this.$db.category.bulkAdd(dataToSave).then(() => {
          console.log('カテゴリ一斉追加 >> 成功')

          // サーバーから取得し、IDBに保存したデータを適用
          this.getCategoryDataFromDB()

        }).catch((e) => {
          console.log('カテゴリ一斉追加 >> 失敗')
          console.error(e.message)
        })

      }).catch((e) => {
        console.log('カテゴリ取得(API) >> 失敗')
        console.error(e.message)
      })

    },
    updateCategoryData(updatedCategoryData) {
      // カテゴリデータを更新
      const targetId = updatedCategoryData.id
      delete updatedCategoryData.id

      // サーバーに送信
      const sendData = {
        'category_name': updatedCategoryData.name,
        'color_code': updatedCategoryData.color,
      }
      this.$axios.put('/api/category/'+targetId+'/', sendData).then(() => {
        console.log('カテゴリ更新(API) >> 成功')

        // IDBで更新
        this.$db.category.update(targetId, updatedCategoryData).then(() => {
          console.log('カテゴリ更新(IDB) >> 成功')
          // カテゴリデータの再読み込み
          this.getCategoryDataFromDB()
        }).catch((e) => {
          console.log('カテゴリ更新(IDB) >> 失敗')
          console.error(e.message)
        })

      }).catch((e) => {
        console.log('カテゴリ更新(API) >> 失敗')
        console.error(e.message)
      })

    },
    addCategoryData(newCategoryData) {
      // カテゴリデータを追加
      // サーバーに送信
      const sendData = {
        'category_name': newCategoryData.name,
        'color_code': newCategoryData.color,
      }
      this.$axios.post('/api/category/', sendData).then((response) => {
        console.log('カテゴリ新規作成(API) >> 成功')
        console.log(response.data)

        // IDBに追加
        newCategoryData.id = response.data.id
        this.$db.category.add(newCategoryData).then(() => {
          console.log('カテゴリ新規作成(IDB)) >> 成功')
          // カテゴリデータの再読み込み
          this.getCategoryDataFromDB()
        }).catch((e) => {
          console.log('カテゴリ新規作成(IDB)) >> 失敗')
          console.error(e.message)
        })
      }).catch((e) => {
        console.log('カテゴリ新規作成(API) >> 失敗')
        console.error(e.message)
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