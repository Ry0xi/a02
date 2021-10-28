// TODOs:
// - サーバーへの処理が失敗した場合にOffline_○○テーブルに登録
// - サーバーへの処理を行わないとき(失敗したときも含む)に各ページに表示するメッセージの扱い
// - addTaskToIDBOfflineTask(|Category)の、既にCreateがあった場合のdeleteやupdateの処理
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
    state.categoryData = categoryData
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
    const today = new Date().toISOString().substr(0, 10)
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
}

export const actions = {
  // API経由でTaskとHistoryの情報を取得
  // それらをIDBに保存し、保存したデータをVuexのStateに適用
  fetchAndApplyTasks({dispatch, commit, state, getters}) {
    console.log('fetchAndApplyTasks()')
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
    .then(() => {
      // test
      console.log('state.tasks:', state.tasks)
      console.log('state.taskData:', state.taskData)
      console.log('getters.tasks:', getters.tasks)
      console.log('getters.taskData:', getters.taskData)
    })
    .catch(e => {
      console.error('fetchAndApplyTasks Error:', e.message)
    })
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
            type: 'created',
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
  // 単一の処理
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
    return this.$db.offline_task.add({
      'task_id': taskId,
      'type': type,
      'data': data,
    })
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
    return this.$db.task.put({'id': taskId, ...data})
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
  }
}