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
      class="taskListMarginBottom"
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
      taskData: null,
      loadingTask: false,
      categoryData: null,
      snackbarDelete: false,
      errorMessage: null,
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
        
        // データを整形して保持
        let newData = {}
        categoryData.forEach((category) => {
          newData[category.id] = {'name': category.name, 'color': category.color}
        })
        this.categoryData = newData
        console.log('categoryData >> 取得成功')
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
      if (this.$store.getters.isOnline) {
        // オンラインの場合
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

        // オンラインならサーバーからデータを取得・適用
        Promise.all([promiseTask, promiseHistory])
        .then(arrays => {
          return promiseClearTaskDate
          .then(() => {
            console.log('promiseClearTaskDate１')
            return arrays
          })
        })
        .then(arrays => promiseAddTaskDate(arrays[0], arrays[1]))
        .then(() => this.getTasksFromDB())
        .catch(e => {
          console.error('fetchTaskData Error: '+e.message)
        })

      } else {
        // オフラインの場合
        this.errorMessage = 'データの取得に失敗しました。ローカルデータを表示します。'
        this.getTasksFromDB()
      }
    },
    addTaskData(newTaskData) {
      // IDBに登録する
      const promiseAddTaskToIDB = taskData => {
        return this.$db.task.add(taskData).then(() => {
          console.log('タスク追加(IDB) >> 成功')
        }).catch((e) => {
          console.log('タスク追加(IDB) >> 失敗')
          console.error(e.message)
        }).then(() => {
          // データを整形
          let newData = {
            'task_id': taskData.id,
            'date': taskData.next_display_date,
            'is_done': false,
          }
          return this.$db.task_date.add(newData)
        })
      }

      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // サーバーに追加する
        const promiseAddTaskToServer = this.$axios.post('/api/task/', newTaskData)
        .then(response => response.data)
        .then(taskData => {
          console.log('タスク追加(API) >> 成功')
          return taskData
        }).catch((e) => {
          console.log('タスク追加(API) >> 失敗')
          console.error(e.message)
        })

        // オンライン時はデータを同期して保存
        promiseAddTaskToServer
        .then((taskData) => promiseAddTaskToIDB(taskData))
        .then(() => this.getTasksFromDB())
      } else {
        // オフライン時は仮のIDで保存し、offline_taskテーブルに追加
        const taskId = this.makeTmpId('task')
        const saveData = {'id': taskId, ...newTaskData}
        promiseAddTaskToIDB(saveData)
        .then(() => {
          this.errorMessage = 'タスク追加の同期に失敗しました。オンラインに復帰後同期します。'

          return this.$db.offline_task.add({
            'task_id': taskId,
            'type': 'create',
            'data': newTaskData,
          })
        })
        .then(() => this.getTasksFromDB())
      }
    },
    deleteTaskData(taskId) {
      // IDBから削除
      const promiseDeleteTaskOnIDB = this.$db.task.delete(taskId)
      .then(() => {
        console.log('タスク削除(IDB)1 >> 成功')

        return this.$db.task_date
        .where('task_id')
        .equals(taskId)
        .delete().then(() => {
          console.log('タスク削除(IDB)2 >> 成功')
        })
      })

      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // サーバーに送信(オンラインの場合)
        const promiseDeleteTaskOnServer = this.$axios.delete('/api/task/'+String(taskId)+'/')
        .then(() => {
          console.log('タスク削除(API) >> 成功')
        })

        promiseDeleteTaskOnIDB
        .then(() => promiseDeleteTaskOnServer)
        .catch(e => {
          console.log('タスク削除(Online) >> 失敗')
          console.error(e.message)
        })
        .then(() => {
          // 削除を通知
          this.snackbarDelete = true
          // タスクデータの再読み込み
          this.getTasksFromDB()
        })

      } else {
        // オフラインの場合
        promiseDeleteTaskOnIDB
        .then(() => {
          // offline_taskに登録
          return this.$db.offline_task.add({
            'task_id': taskId,
            'type': 'delete',
            'data': null,
          })
        })
        .catch(e => {
          console.log('タスク削除(Offline) >> 失敗')
          console.error(e.message)
        })
        .then(() => {
          this.errorMessage = 'タスク削除の同期に失敗しました。オンラインに復帰後同期します。'
          // 削除を通知
          this.snackbarDelete = true
          // タスクデータの再読み込み
          this.getTasksFromDB()
        })
      }
    },
    updateTaskData(updatedData) {
      const taskId = updatedData.id
      delete updatedData.id

      // IDBで更新する処理
      const promiseUpdateTaskOnIDB = this.$db.task.update(taskId, updatedData)
      .then(() => {
        console.log('タスク更新(IDB) >> 成功')
      })
      
      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // サーバーに送信する処理
        const promiseUpdateTaskOnServer = this.$axios.put('/api/task/'+String(taskId)+'/', updatedData)
        .then(() => {
          console.log('タスク更新(API) >> 成功')
        })

        promiseUpdateTaskOnIDB
        .then(() => promiseUpdateTaskOnServer)
        .catch(e => {
          console.log('タスク更新(Online) >> 失敗')
          console.error(e.message)
        })
        .then(() => {
          // タスクデータの再読み込み
          this.getTasksFromDB()
        })

      } else {
        // オフラインの場合
        promiseUpdateTaskOnIDB
        .then(() => {
          // offline_taskに登録
          return this.$db.offline_task.add({
            'task_id': taskId,
            'type': 'update',
            'data': updatedData,
          })
        })
        .catch(e => {
          console.log('タスク更新(Offline) >> 失敗')
          console.error(e.message)
        })
        .then(() => {
          this.errorMessage = 'タスク更新の同期に失敗しました。オンラインに復帰後同期します。'

          // タスクデータの再読み込み
          this.getTasksFromDB()
        })
      }
    },
    doneTask(data) {
      const taskDateId = data.taskDateId
      const taskFeedback = data.feedback

      const taskId = this.tasks.find(task => task.id === taskDateId).task_id

      // IDBを更新
      const promiseDoneTaskOnIDB = this.$db.task_date.update(taskDateId, {
        'is_done': true,
        'feedback': taskFeedback,
      })
      .then(() => {
        console.log('タスク完了(IDB) >> 成功')
      })

      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // API処理
        const promiseCompleteTask = this.$axios.put('/api/task-completed-task/'+String(taskId)+'/', {'feedback': taskFeedback})
        const promiseAddHistory = this.$axios.post('/api/task-completed-history/', {'task_id': taskId, 'feedback': taskFeedback})

        // サーバーに送信し、IDBにも保存
        Promise.all([promiseCompleteTask, promiseAddHistory, promiseDoneTaskOnIDB])
        .then(() => {
          console.log('タスク完了(Online) >> 成功')
          // タスクデータの再取得・読み込み
          this.fetchTasks()
        })
        .catch((e) => {
          console.log('タスク完了(Online) >> 失敗')
          console.error(e.message)
        })

      } else {
        // オフラインの場合
        promiseDoneTaskOnIDB
        .then(() => {
          // offline_taskに登録
          return this.$db.offline_task.add({
            'task_id': taskId,
            'type': 'done',
            'data': {
              'task_id': taskId,
              'feedback': taskFeedback,
            }
          })
        })
        .then(() => {
          console.log('タスク完了(Offline) >> 成功')
          this.errorMessage = 'タスク完了の同期に失敗しました。オンラインに復帰後同期します。'

          // タスクデータの再読み込み
          this.getTasksFromDB()
        })
        .catch((e) => {
          console.log('タスク完了(Offline) >> 失敗')
          console.error(e.message)
        })
      }
      
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

      // 更新するデータ
      const sendData = {
        'category_name': updatedCategoryData.name,
        'color_code': updatedCategoryData.color,
      }

      // IDBで更新する処理
      const promiseUpdateCategoryOnIDB = this.$db.category.update(targetId, updatedCategoryData)
      .then(() => {
        console.log('カテゴリ更新(IDB) >> 成功')
      })

      if (this.$store.getters.isOnline) {
        // オンラインの場合
        // サーバーに送信する処理
        const promiseUpdateCategoryOnServer = this.$axios.put('/api/category/'+targetId+'/', sendData)
        .then(() => {
          console.log('カテゴリ更新(API) >> 成功')
        })

        Promise.all([promiseUpdateCategoryOnIDB, promiseUpdateCategoryOnServer])
        .then(() => {
          // カテゴリデータの再読み込み
          this.getCategoryDataFromDB()
        })
        .catch(e => {
          console.log('カテゴリ更新(Online) >> 失敗')
          console.error(e.message)
        })

      } else {
        // オフラインの場合
        promiseUpdateCategoryOnIDB
        .then(() => {
          // offline_categoryに登録
          return this.$db.offline_category.add({
            'category_id': targetId,
            'type': 'update',
            'data': sendData,
          })
        })
        .then(() => {
          this.errorMessage = 'カテゴリ更新の同期に失敗しました。オンラインに復帰後同期します。'
          // カテゴリデータの再読み込み
          this.getCategoryDataFromDB()
        })
        .catch(e => {
          console.log('カテゴリ更新(Offline) >> 失敗')
          console.error(e.message)
        })
      }
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