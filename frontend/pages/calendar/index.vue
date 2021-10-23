<template>
  <div>
    <v-card outlined class="mb-4">
      <CalendarMonth v-model="date">
        <template #activator="{ on }">
          <v-btn v-on="on" text class="my-2">
            <v-icon class="mr-2" color="primary">mdi-calendar-month</v-icon>
            {{ formatDate }}
          </v-btn>
        </template>
      </CalendarMonth>

      <v-calendar v-model="date" color="primary" style="overflow: hidden">
        <template v-slot:day-label="{ date, day }">
          <div class="dayBox">
            <div class="dayBox_day">{{ day }}</div>
          </div>
          <draggable
            @add="onAdd(date)"
            :group="{ name: 'ITEMS' }"
            class="dayBox_drag"
            v-model="setItem"
          >
          </draggable>
        </template>
      </v-calendar>
    </v-card>

    <v-card outlined>
      <div class="taskBox">
        <div>
          <draggable
            v-model="taskItems"
            class="taskBox_items"
            :group="{ name: 'ITEMS', pull: 'clone', put: false }"
          >
            <div
              v-for="(task, index) in taskItems"
              :key="index"
              class="taskItem"
            >
              {{ task.title }}
            </div>
          </draggable>
        </div>
      </div>
    </v-card>
    <TaskCreate
      v-model="dialog"
      :taskTitle="task.title"
      :taskDate="task.date"
      :categoryData="categoryData"
      @task:created="addTaskData($event)"
      @category:updated="updateCategoryData($event)"
      @category:created="addCategoryData($event)"
    />
    <v-snackbar v-model="snackbar">
      今日以前にタスクは追加できません。
    </v-snackbar>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  components: {
    draggable,
  },
  data() {
    return {
      header: {
        title: 'カレンダー',
      },
      date: new Date().toISOString().substr(0, 10),
      dialog: false,
      task: {
        title: '',
        date: '',
      },
      setItem: [],
      taskItems: [],
      tasks: [],
      categoryData: null,
      snackbar: false,
    }
  },
  computed: {
    // 日付をフォーマット
    formatDate() {
      const dt = new Date(this.date)
      const year = dt.getFullYear()
      const month = dt.getMonth() + 1
      return `${year}年${month}月`
    },
  },
  mounted() {
    this.updateHeader()
    this.getCategoryDataFromDB()
    this.getTasksFromDB()
  },
  methods: {
    async getTasksFromDB() {
      console.log('getTasksFromDB')

      await this.$db.task
        .toArray()
        .then((tasks) => {
          console.log('tasks >> 取得成功')
          console.log(tasks)

          this.tasks = tasks
          this.taskItems = this.dedupe(this.tasks)
        })
        .catch((e) => {
          console.log('tasks >> 取得失敗')
          console.log(e.message)
        })
    },
    async getCategoryDataFromDB() {
      console.log('getCategoryDataFromDB')

      // カテゴリを取得
      await this.$db.category
        .toArray()
        .then((categoryData) => {
          console.log('categoryData >> 取得成功')

          // データを整形して保持
          let newData = {}
          categoryData.forEach((category) => {
            newData[category.id] = {
              name: category.name,
              color: category.color,
            }
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
    // 重複の削除
    dedupe(tasks) {
      return tasks.filter(
        (element, index, self) =>
          self.findIndex((e) => e.title === element.title) === index
      )
    },
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
    },
    // 追加時の処理
    onAdd(date) {
      const now = new Date(this.date)
      const targetDate = new Date(date)
      if (targetDate >= now) {
        this.task.title = this.setItem[0].title
        this.task.date = date
        this.dialog = true
        this.setItem = []
      } else {
        this.snackbar = true
      }
    },
  },
}
</script>

<style lang="scss">
.taskBox {
  overflow-y: scroll;
  width: 100%;
  height: 200px;
  padding: 12px;
  background-color: #fff;
  &_items {
    display: flex;
    flex-wrap: wrap;
  }
  &_item {
    padding: 5px 15px;
    margin: 5px;
    background-color: #fbeab9;
    border-radius: 10px;
  }
}

.taskItem {
  padding: 5px 15px;
  margin: 5px;
  background-color: #fbeab9;
  border-radius: 10px;
  cursor: pointer;
}

.dayBox {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  &_day {
    width: 100%;
    padding: 10px 0;
    font-size: 14px;
    color: #444;
  }
  &_active {
    background-color: red;
  }

  &_drag {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
}

.sortable-chosen {
  width: 35px;
  height: 35px;
  padding: 0;
  margin: 0;
  text-indent: 100%;
  overflow: hidden;
  white-space: nowrap;
  background-color: rgb(255, 195, 42);
  opacity: 0.5;
}
</style>
