// TODOs:
// - サーバーへの処理が失敗した場合にOffline_○○テーブルに登録
// - サーバーへの処理を行わないとき(失敗したときも含む)に各ページに表示するメッセージの扱い
// - オフラインでタスクを完了した場合の次回表示日をどうするか
export const state = () => ({
  online: window.navigator.onLine,
  tasks: null,
  taskData: null,
  categoryData: null,
})

export const mutations = {
  // オンラインステータス
  changeStatusToOnline(state) {
    state.online = true
    console.log('online now')
  },
  changeStatusToOffline(state) {
    state.online = false
    console.log('offline now')
  },
  replaceTasks(state, tasks) {
    state.tasks = tasks
  },
  replaceTaskData(state, taskData) {
    // データを整形して保持
    let newData = {}
    taskData.forEach((task) => {
      const taskId = task.id
      delete task.id
      newData[taskId] = task
    })
    // タスクデータの適用
    state.taskData = newData
  },
  replaceCategoryData(state, categoryData) {
    // データを整形して保持
    let newData = {}
    categoryData.forEach((category) => {
      newData[category.id] = {
        'name': category.name,
        'color': category.color
      }
    })
    state.categoryData = newData
  },
}

export const getters = {
  isOnline(state) {
    return state.online
  },
  tasks(state) {
    return state.tasks
  },
  tasksToday(state) {
    const today = new Date().toLocaleDateString().replaceAll('/', '-')
    const tasks = state.tasks
    return tasks?.filter(task => task.date == today) ?? null
    // オプショナルチェイニング演算子
    // https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Operators/Optional_chaining
    // Null合体演算子
    // https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator
  },
  taskData(state) {
    return state.taskData
  },
  categoryData(state) {
    return state.categoryData
  }
}

export const actions = {
  // API経由でTaskとHistoryの情報を取得
  // それらをIDBに保存し、保存したデータをVuexのStateに適用
  fetchAndApplyTasks({state, dispatch}) {
    console.log('fetchAndApplyTasks()')
    if (state.online) {
      // オンラインの場合
      const promiseGetTasks = dispatch('getTasksFromServer')
      const promiseGetHistory = dispatch('getHistoryFromServer')
  
      promiseGetTasks
      .then(tasks => {
        // test
        console.log('promiseGetTasks: tasks')
        console.log(tasks)
        return tasks
      })
      .then(tasks => dispatch('replaceIDBTaskWithNewTasks', tasks))
  
      Promise.all([
        promiseGetTasks,
        promiseGetHistory
      ])
      .then(data => {
        // test
        console.log('promiseAll: data')
        console.log(data)
        return data
      })
      .then(data => {
        const tasks = data[0]
        const history = data[1]
        // データを整形
        let formattedTasks = []
        tasks.forEach(task => {
          const taskData = {
            'task_id': task.id,
            'date': task.next_display_date,
            'is_done': false,
          }
          formattedTasks.push(taskData)
        })
        history.forEach((task) => {
          const taskData = {
            'date': task.completed_date,
            'is_done': true,
            'feedback': task.feedback,
            'task_id': task.task_id,
          }
          formattedTasks.push(taskData)
        })
        return formattedTasks
      })
      .then(tasks => {
        // test
        console.log('tasks')
        console.log(tasks)
        return tasks
      })
      .then(tasks => dispatch('replaceIDBTaskDateWithNewTasks', tasks))
      .then(() => dispatch('replaceAllTaskStateWithTasksFromIDB'))
      .catch(e => {
        console.error('fetchAndApplyTasks Error:', e.message)
      })
    } // if (state.online)
  },
  // IDBから取得したタスク関連の情報をVuexのStateに適用する
  replaceAllTaskStateWithTasksFromIDB({commit, dispatch}) {
    return Promise.all([
      dispatch('getTaskDataFromIDB')
      .then(taskData => commit('replaceTaskData', taskData)),
      dispatch('getTasksFromIDB')
      .then(tasks => commit('replaceTasks', tasks))
    ])
  },
  // サーバーへの新規追加とIDBへの登録処理
  // オフラインの場合は仮のIDでの登録とOffline_taskへの登録
  addTask({state, dispatch}, taskData) {

    const addTaskToIDB = taskData => {
      const formattedTaskData = {
        'task_id': taskData.id,
        'date': taskData.next_display_date,
        'is_done': false,
      }

      // test
      console.log('taskData')
      console.log(taskData)
      console.log('formattedTaskData')
      console.log(formattedTaskData)

      return Promise.all([
        dispatch('addTaskToIDBTask', taskData),
        dispatch('addTaskToIDBTaskDate', formattedTaskData)
      ])
    }

    if (state.online) {
      // オンラインの場合は、
      // データをサーバーに送信して、
      // 返り値の新規IDを元にIDBに保存
      return dispatch('addTaskToServer', taskData)
      .then(responsedTaskData => addTaskToIDB(responsedTaskData))
    } else {
      // オフラインの場合は、
      // 仮のIDでIDBに保存し、offline_taskテーブルに登録
      dispatch('makeTmpId', 'task')
      .then(id => {
        const dataToSave = {'id': id, ...taskData}
        return Promise.all([
          addTaskToIDB(dataToSave),
          dispatch('addTaskToIDBOfflineTask', {
            taskId: id,
            type: 'create',
            data: taskData,
          })
        ])
      })
    }
  },
  // サーバーからの削除とIDBからの削除を行う
  // オフラインの場合はIDBからのみ削除しOffline_taskに登録
  deleteTask({state, dispatch}, taskId) {
    if (state.online) {
      // オンラインの場合は、
      // サーバーとIDBから削除する
      return dispatch('deleteTaskOnServer', taskId)
      .then(() => {
        return Promise.all([
          dispatch('deleteTaskOnIDBTask', taskId),
          dispatch('deleteTaskOnIDBTaskDate', taskId)
        ])
      })
      .catch(e => console.error('deleteTask(Online) Error:', e.message))

    } else {
      // オフラインの場合は、
      // IDBから削除しOffline_taskに登録
      return Promise.all([
        dispatch('deleteTaskOnIDBTask', taskId),
        dispatch('deleteTaskOnIDBTaskDate', taskId),
        dispatch('addTaskToIDBOfflineTask', {
          taskId: taskId,
          type: 'delete',
          data: null,
        })
      ])
      .catch(e => console.error('deleteTask(Offline) Error:', e.message))
    }
  },
  // サーバーとIDBでタスクの更新を行う
  // オフラインの場合はIDBでの更新とOffline_taskへの登録を行う
  updateTask({state, dispatch}, {taskId, data}) {
    if (state.online) {
      // オンラインの場合は、
      // サーバーでの更新とIDBでの更新処理
      return Promise.all([
        dispatch('updateTaskOnServer', {
          taskId: taskId,
          data: data,
        }),
        dispatch('updateTaskOnIDBTask', {
          taskId: taskId,
          data: data,
        })
      ])
      .catch(e => console.error('updateTask Error:', e.message))
    } else {
      // オフラインの場合は、
      // IDBで更新し、Offline_taskに登録
      return Promise.all([
        dispatch('updateTaskOnIDBTask', {
          taskId: taskId,
          data: data,
        }),
        dispatch('addTaskToIDBOfflineTask', {
          taskId: taskId,
          type: 'update',
          data: data,
        })
      ])
      .catch(e => console.error('updateTask Error:', e.message))
    }
  },
  completeTask({state, dispatch}, {taskDateId, taskId, feedback}) {
    if (state.online) {
      // オンラインの場合は、
      // 2つのAPI通信とIDBでの更新処理
      return Promise.all([
        dispatch('completeTaskOnServer', {
          taskId: taskId,
          feedback: feedback,
        })
        .then(response => response.data)
        .then(taskData => {
          return dispatch('updateTaskOnIDBTask', {
            taskId: taskId,
            data: taskData,
          })
        }),
        dispatch('addTaskOnServerHistory', {
          taskId: taskId,
          feedback: feedback,
        }),
        dispatch('completeTaskOnIDBTaskDate', {
          taskDateId: taskDateId,
          feedback: feedback,
        })
      ])

    } else {
      // オフラインの場合は、
      // task_dateでの完了とOffline_taskへの登録を行う
      return Promise.all([
        dispatch('completeTaskOnIDBTaskDate', {
          taskDateId: taskDateId,
          feedback: feedback,
        }),
        dispatch('addTaskToIDBOfflineTask', {
          taskId: taskId,
          type: 'done',
          data: {
            'task_id': taskId,
            'feedback': feedback,
          }
        })
      ])
    }
  },
  // 仮の新規IDを生成(Vuex Stateに存在しているIDの最大値＋1)
  // let tmpId = null
  // return dispatch('makeTmpId', 'category')
  // .then(newId => tmpId = newId)
  makeTmpId({state}, type) {
    let existIds = []
    if (type == 'category') {
      existIds = Object.keys(state.categoryData).map(id => Number(id))
    } else if (type == 'task') {
      existIds = state.tasks.map(task => task.task_id)
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
  },
  // サーバーからカテゴリを取得しIDBに登録、VuexStateに反映
  fetchAndApplyCategoryData({state, commit, dispatch}) {
    if (state.online) {
      // オンラインの場合
      dispatch('getCategoryDataFromServer')
      .then(categoryData => {
        // データ形式を変換
        let dataForIDBCategory = []
        categoryData.forEach((category) => {
          const categoryToSave = {
            'id': category.id,
            'name': category.category_name,
            'color': category.color_code,
          }
          dataForIDBCategory.push(categoryToSave)
        })
        return dataForIDBCategory
      })
      .then(categoryData => {
        return dispatch('replaceIDBCategoryWithNewCategoryData', categoryData)
        .then(() => commit('replaceCategoryData', categoryData))
      })
      .catch(e => console.error('fetchAndApplyCategoryData Error:', e.message))
    } else {
      // オフラインの場合何もしない
    }
  },
  replaceCategoryStateWithCategoryOnIDBCategory({commit, dispatch}) {
    return dispatch('getCategoryDataFromIDBCategory')
    .then(categoryData => commit('replaceCategoryData', categoryData))
  },
  // カテゴリの情報をサーバーとIDBで更新
  // オフラインの場合は、IDBで更新し、Offline_categoryへ登録する
  updateCategoryData({state, dispatch}, {categoryId, data}) {
    // サーバーで更新するデータ
    const sendData = {
      'category_name': data.name,
      'color_code': data.color,
    }
    if (state.online) {
      // オンラインの場合
      return Promise.all([
        dispatch('updateCategoryOnServer', {
          categoryId: categoryId,
          data: sendData,
        }),
        dispatch('updateCategoryDataOnIDBCategory', {
          categoryId: categoryId,
          data: data,
        })
      ])
      .catch(e => console.error('updateCategoryData Error:', e.message))
    } else {
      // オフラインの場合
      return dispatch('updateCategoryDataOnIDBCategory', {
        categoryId: categoryId,
        data: data,
      })
      .then(() => dispatch('addCategoryToIDBOfflineCategory', {
        categoryId: categoryId,
        type: 'update',
        data: sendData,
      }))
      .catch(e => console.error('updateCategoryData Error:', e.message))
    }
  },
  // サーバーとIDBでカテゴリを追加する
  // オフラインの場合は仮のIDで追加し、Offline_categoryへ登録する
  addCategoryData({state, dispatch}, data) {
    // サーバーに送信するデータ
    const sendData = {
      'category_name': data.name,
      'color_code': data.color,
    }
    if (state.online) {
      // オンラインの場合
      return dispatch('addCategoryDataToServer', sendData)
      .then(categoryData => dispatch('addCategoryDataToIDBCategory', {
        'id': categoryData.id,
        ...data
      }))
      .catch(e => console.error('addCategoryData Error:', e.message))

    } else {
      // オフラインの場合
      let tmpId = null
      return dispatch('makeTmpId', 'category').then(newId => tmpId = newId)
      .then(() => {
        return Promise.all([
          dispatch('addCategoryDataToIDBCategory', {
            'id': tmpId,
            ...data
          }),
          dispatch('addCategoryToIDBOfflineCategory', {
            categoryId: tmpId,
            type: 'create',
            data: sendData,
          })
        ])
      })
      .catch(e => console.error('addCategoryData Error:', e.message))
    }
  },
  // 単一の処理
  // タスク関連の処理
  getTasksFromServer({state}) {
    if (state.online) {
      return this.$axios.get('/api/task/')
      .then(response => response.data)
    }
  },
  getHistoryFromServer({state}) {
    if (state.online) {
      return this.$axios.get('/api/history/')
      .then(response => response.data)
    }
  },
  getTasksFromIDB({}) {
    return this.$db.task_date.toArray()
  },
  getTaskDataFromIDB({}) {
    return this.$db.task.toArray()
  },
  addTaskToIDBOfflineTask({}, {taskId, type, data}) {
    // offline_taskへ登録
    if (type == 'delete') {
      // 追加操作が未同期の場合、追加した履歴ごと削除する
      return this.$db.offline_task.where({'task_id': taskId}).toArray()
      .then(tasks => {
        const deleteTaskUpdateOrDoneIfExist = () => {
          // 同じタスクIDで既にタスクの更新や完了が登録されていた場合はそれらをオフラインタスクから削除する
          const getOfflineTasksUpdateOrDone = this.$db.offline_task
          .where('task_id').equals(taskId).toArray()
          // ANDは使えないので後からフィルター
          .then(tasks => tasks.length ? tasks.filter(task => task.type == 'update' || task.type == 'done') : [])

          return getOfflineTasksUpdateOrDone
          .then(tasks => {
            if (tasks.length) {
              console.log('type:update||done exist')
              // 'update'や'done'があった場合はすべて削除する
              return this.$db.offline_task
              .where('id').anyOf(tasks.map(task => task.id))
              .delete()
              .then(count => console.log('deleted', count, 'items(update or done)'))
            } else {
              console.log('type:update||done NOT exist')
            }
          })
        }

        const indexCreate = tasks.findIndex(task => task.type == 'create')
        if (indexCreate !== -1) {
          // オフラインタスクにcreateが存在する場合はそのタスクの履歴をすべて削除
          console.log('type:create exist')
          return this.$db.offline_task
          .where('task_id').equals(taskId).delete()
        } else {
          // オフラインタスクにcreateが存在しない場合
          console.log('type:create NOT exist')
          return Promise.all([
            this.$db.offline_task.add({
              'task_id': taskId,
              'type': type,
              'data': data,
            }),
            deleteTaskUpdateOrDoneIfExist()
          ])
        }
      })

    } else if (type == 'update') {
      // 追加操作が未同期の場合、登録されている追加するデータを上書きする
      return this.$db.offline_task.where({'task_id': taskId}).toArray()
      .then(tasks => {
        const index = tasks.findIndex(task => task.type == 'create')
        if (index !== -1) {
          return this.$db.offline_task.update(tasks[index].id, {'data': data})
        } else {
          return this.$db.offline_task.add({
            'task_id': taskId,
            'type': type,
            'data': data,
          })
        }
      })
    } else {
      // typeがcreate, doneの場合
      return this.$db.offline_task.add({
        'task_id': taskId,
        'type': type,
        'data': data,
      })
    }

  },
  addTaskToServer({state}, task) {
    if (state.online) {
      return this.$axios.post('/api/task/', task)
      .then(response => response.data)
    }
  },
  addTaskToIDBTask({}, task) {
    return this.$db.task.add(task)
  },
  addTaskToIDBTaskDate({}, task) {
    return this.$db.task_date.add(task)
  },
  deleteTaskOnServer({state}, taskId) {
    if (state.online) {
      return this.$axios.delete('/api/task/'+String(taskId)+'/')
    }
  },
  deleteTaskOnIDBTask({}, taskId) {
    return this.$db.task.delete(taskId)
  },
  deleteTaskOnIDBTaskDate({}, taskId) {
    return this.$db.task_date
    .where('task_id')
    .equals(taskId)
    .delete()
  },
  updateTaskOnServer({state}, {taskId, data}) {
    if (state.online) {
      return this.$axios.put('/api/task/'+String(taskId)+'/', data)
    }
  },
  updateTaskOnIDBTask({}, {taskId, data}) {
    return this.$db.task.update(taskId, data)
  },
  completeTaskOnServer({state}, {taskId, feedback}) {
    if (state.online) {
      return this.$axios.put('/api/task-completed-task/'+String(taskId)+'/', {'feedback': feedback})
    }
  },
  addTaskOnServerHistory({state}, {taskId, feedback}) {
    if (state.online) {
      return this.$axios.post('/api/task-completed-history/', {
        'task_id': taskId,
        'feedback': feedback
      })
    }
  },
  completeTaskOnIDBTaskDate({}, {taskDateId, feedback}) {
    return this.$db.task_date.update(taskDateId, {
      'is_done': true,
      'feedback': feedback,
    })
  },
  replaceIDBTaskWithNewTasks({}, tasks) {
    return this.$db.task.clear()
    .then(() => this.$db.task.bulkAdd(tasks))
  },
  replaceIDBTaskDateWithNewTasks({}, tasks) {
    return this.$db.task_date.clear()
    .then(() => this.$db.task_date.bulkAdd(tasks))
  },
  // カテゴリ関連の処理
  getCategoryDataFromServer({state}) {
    if (state.online) {
      return this.$axios.get('/api/category/')
      .then(response => response.data)
    }
  },
  getCategoryDataFromIDBCategory({}) {
    return this.$db.category.toArray()
  },
  replaceIDBCategoryWithNewCategoryData({}, categoryData) {
    return this.$db.category.clear()
    .then(() => this.$db.category.bulkAdd(categoryData))
  },
  addCategoryToIDBOfflineCategory({}, {categoryId, type, data}) {
    // offline_categoryに登録
    if (type == 'update') {
      // 新規作成が未同期の場合、作成したデータを上書きする
      return this.$db.offline_category.where({'category_id': categoryId}).toArray()
      .then(categories => {
        const index = categories.findIndex(category => category.type == 'create')
        if (index !== -1) {
          return this.$db.offline_category.update(categories[index].id, {'data': data})
        } else {
          return this.$db.offline_category.add({
            'category_id': categoryId,
            'type': type,
            'data': data,
          })
        }
      })

    } else {
      return this.$db.offline_category.add({
        'category_id': categoryId,
        'type': type,
        'data': data,
      })
    }
  },
  updateCategoryOnServer({state}, {categoryId, data}) {
    if (state.online) {
      this.$axios.put('/api/category/'+categoryId+'/', data)
    }
  },
  updateCategoryDataOnIDBCategory({}, {categoryId, data}) {
    return this.$db.category.update(categoryId, data)
  },
  addCategoryDataToServer({state}, data) {
    if (state.online) {
      return this.$axios.post('/api/category/', data)
      .then(response => response.data)
    }
  },
  addCategoryDataToIDBCategory({}, categoryData) {
    return this.$db.category.add(categoryData)
  },
}