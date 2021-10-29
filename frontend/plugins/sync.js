export default ({ $db, $axios, store }, inject) => {
  //   CRUD
  const create = async (value, uri) => {
    return await $axios
      .post(uri, value.data)
      .then((response) => {
        return response
      })
      .catch((error) => {
        return error
      })
  }
  
  const update = async (value, uri, idName) => {
    return await $axios
      .put(uri + value[idName] + '/', value.data)
      .then((response) => {
        return response
      })
      .catch((error) => {
        return error
      })
  }

  const remove = async (value, uri, idName) => {
    return await $axios
      .delete(uri + value[idName] + '/', value.data)
      .then((response) => {
        return response
      })
      .catch((error) => {
        return error
      })
  }

  const done = async (value) => {
    return await $axios
      .put('/api/task-completed-task/' + value.task_id + '/', {
        feedback: value.data.feedback,
      })
      .then((response) => {
        return response
      })
      .catch((error) => {
        return error
      })
  }

  const removeRecord = (id, tableName) => {
    $db[tableName].delete(id)
  }

  //   タスクの同期処理
  const task = async (items) => {
    await Promise.all(
      items.map(async (item) => {
        if (item.type === 'create') {
          await create(item, '/api/task/').then((response) => {
            $db.task.put(taskFormat(response.data))
            taskChange(item.id, response.data.id)
            removeRecord(item.id, 'offline_task')
          })
        } else if (item.type === 'update') {
          await update(item, '/api/task/', 'task_id').then((response) => {
            $db.task.put(taskFormat(response.data))
            removeRecord(item.id, 'offline_task')
          })
        } else if (item.type === 'delete') {
          await remove(item, '/api/task/', 'task_id').then(() => {
            removeRecord(item.id, 'task')
            removeRecord(item.id, 'offline_task')
          })
        } else if (item.type === 'done') {
          await done(item).then((response) => {
            $db.task.update(response.data.id, taskDoneFormat(response.data))
            removeRecord(item.id, 'offline_task')
          })
        }
      })
    )
  }

  //   カテゴリーの同期処理
  const category = async (items) => {
    await Promise.all(
      items.map(async (item) => {
        if (item.type === 'create') {
          await create(item, '/api/category/').then((response) => {
            $db.category.put(categoryFormat(response.data))
            categoryChange(item.id, response.data.id)
            removeRecord(item.id, 'offline_category')
          })
        } else if (item.type === 'update') {
          await update(item, '/api/category/', 'category_id').then(
            (response) => {
              $db.category.put(categoryFormat(response.data))
              removeRecord(item.id, 'offline_category')
            }
          )
        } else if (item.type === 'delete') {
          await remove(item, '/api/category/', 'category_id').then(() => {
            removeRecord(item.id, 'offline_category')
            removeRecord(item.id, 'category')
          })
        }
      })
    )
  }

  //   フォーマット
  const taskFormat = (task) => {
    return {
      id: task.id,
      title: task.title,
      detail: task.detail,
      url: task.url,
      priority: task.priority,
      next_display_date: task.next_display_date,
      display_times: task.display_times,
      consecutive_times: task.consecutive_times,
      is_update: task.is_update,
      category: task.category,
      created_at: task.created_at,
    }
  }

  const taskDoneFormat = (task) => {
    return {
      id: task.id,
      priority: task.priority,
      next_display_date: task.next_display_date,
      display_times: task.display_times,
      consecutive_times: task.consecutive_times,
      is_update: task.is_update,
    }
  }

  const categoryFormat = (category) => {
    return {
      id: category.id,
      name: category.category_name,
      color: category.color_code,
    }
  }

  //   オフラインタスクのカテゴリーを更新
  const categoryChange = (before_id, after_id) => {
    $db.offline_task.toArray().then((response) => {
      const tasks = response

      tasks.forEach((task) => {
        if (task.category !== undefined) {
          task.category.forEach((id, index) => {
            if (id === before_id) {
              task.category[index] = after_id
            }
          })
        }
      })
    })
  }

  //   オフラインタスクの"done"のtask_idを更新
  const taskChange = (before_id, after_id) => {
    $db.offline_task.toArray().then((response) => {
      const tasks = response

      tasks.forEach((task, index) => {
        if (task.task_id === before_id) {
          tasks[index].task_id = after_id
        }
      })
    })
  }

  const sync = async () => {
    const responseCategory = await $db.offline_category.toArray()
    await category(responseCategory)

    const responseTask = await $db.offline_task.toArray()
    await task(responseTask)

    store.dispatch('replaceAllTaskStateWithTasksFromIDB')
    store.dispatch('replaceCategoryStateWithCategoryOnIDBCategory')
  }
  
  inject('sync', sync)
}
