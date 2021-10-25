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
  // 
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
  taskData(state) {
    return state.taskData
  },
}

export const actions = {
  fetchAndApplyTasks({dispatch, commit, state, getters}) {
    console.log('fetchAndApplyTasks()')
    const promiseGetTasks = dispatch('getTasksFromServer')
    const promiseGetHistory = dispatch('getHistoryFromServer')

    promiseGetTasks
    .then(tasks => {
      console.log('promiseGetTasks: tasks')
      console.log(tasks)
      return tasks
    })
    .then(tasks => dispatch('replaceIDBTaskWithNewTasks', tasks))

    Promise.all([
      promiseGetTasks,
      promiseGetHistory
    ])
    .then((data) => {
      console.log('promiseAll: data')
      console.log(data)
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
    .then(() => {
      return Promise.all([
        dispatch('getTaskDataFromIDB')
        .then(taskData => commit('replaceTaskData', taskData)),
        dispatch('getTasksFromIDB')
        .then(tasks => commit('replaceTasks', tasks))
      ])
    })
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
  replaceIDBTaskWithNewTasks({}, tasks) {
    return this.$db.task.clear()
    .then(() => this.$db.task.bulkAdd(tasks))
  },
  replaceIDBTaskDateWithNewTasks({}, tasks) {
    return this.$db.task_date.clear()
    .then(() => this.$db.task_date.bulkAdd(tasks))
  }
}