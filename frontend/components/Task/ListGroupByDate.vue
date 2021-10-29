<!--
  shownTasks: 0 -> 全て、1 -> 復習中のタスク、2 -> 復習完了のタスク
  tasks:              {id, task_id, date, is_done}
  taskData:           タスクオブジェクトの配列
  categoryData: 各カテゴリのデータ。[categoryId(String)]: {'name': String, 'color': String}
  @task:done:        タスク完了時に発火するイベント。※TaskDoneBtnを参照
  @task:deleted:     タスクの削除ボタンを押した時に発火するイベント
  @task:updated:     タスクの保存ボタンを押した時に発火するイベント 
  @category:updated: カテゴリが更新されたときに発火するイベント
                     新しいカテゴリデータを返す。※TaskCategoryEditorを参照
  @category:created: カテゴリが新規作成されたときに発火するイベント
                     新しいカテゴリデータを返す。※TaskCategoryEditorを参照
-->
<template>
  <div>
    <div v-for="date in dateList" :key="date" class="task">
      <h3 v-if="isShowDate(date)" class="task-date">{{ $formatDate(date) }}</h3>
      <ul class="task-items">
        <li
          v-for="(key, index) in TaskGroupByDate[date]"
          v-if="isShowTask(taskData[key].is_update)"
          :key="index"
          class="task-item"
        >
          <TaskItem
            :id="'activator' + key"
            :taskDateId="taskDateId(key)"
            :taskTitle="taskData[key].title"
            :taskDate="taskData[key].next_display_date"
            :taskDetail="taskData[key].detail"
            :categories="taskData[key].category"
            :isDone="!taskData[key].is_update"
            :categoryData="categoryData"
            :hideDoneBtn="hideDoneBtn"
            @task:done="doneTask"
          />
          <TaskInfo
            :activator="'#activator' + key"
            :taskId="Number(key)"
            :taskTitle="taskData[key].title"
            :taskDate="taskData[key].next_display_date"
            :taskDetail="taskData[key].detail"
            :categories="taskData[key].category"
            :isDone="taskData[key].is_update"
            :categoryData="categoryData"
            @task:deleted="deleteTask($event)"
            @task:updated="updateTask($event)"
            @category:updated="updateCategoryData($event)"
            @category:created="addCategoryData($event)"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    shownTasks: {
      type: Number,
      default: 0,
    },
    tasks: {
      type: Array,
    },
    taskData: {
      type: Object,
    },
    categoryData: {
      type: Object,
    },
    hideDoneBtn: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    isShowTask(is_update) {
      const value = this.shownTasks === 1 ? false : true
      return is_update === value ? false : true
    },
    isShowDate(date) {
      const value = this.shownTasks === 1 ? true : false
      return this.taskSearch(date).some(
        item => item.is_update === value
      )
    },
    isShownTask: function (task) {
      // すべて表示する
      if (this.shownTasks === 0) {
        return true
      }

      const taskType = task.is_done ? 2 : 1
      if (this.shownTasks === taskType) {
        return true
      } else {
        return false
      }
    },
    // 取り出すタスクの日付、is_updateの真偽値
    taskSearch(date, value) {
      let values = []
      Object.keys(this.taskData).forEach((key) => {
        if (this.taskData[key].next_display_date === date) {
          values.push(this.taskData[key])
        }
      })
      return values
    },
    taskDateId(key) {
      return this.tasks.find(v => v.task_id == key && v.is_done === false).id
    },
    deleteTask: function (taskId) {
      this.$emit('task:deleted', taskId)
    },
    updateTask: function (updatedData) {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      this.$emit('task:updated', updatedData)
    },
    doneTask(taskId) {
      this.$emit('task:done', taskId)
    },
    updateCategoryData(updatedCategoryData) {
      this.$emit('category:updated', updatedCategoryData)
    },
    addCategoryData(newCategoryData) {
      this.$emit('category:created', newCategoryData)
    },
  },
  computed: {
    dateList() {
      return [
        ...new Set(
          Object.keys(this.taskData).map(
            (key) => this.taskData[key].next_display_date
          )
        ),
      ].sort()
    },
    TaskGroupByDate() {
      let data = {}
      let values = []
        this.dateList.forEach((date) => {
          Object.keys(this.taskData).forEach((key) => {
            console.log(key)
            console.log(this.taskData[key].next_display_date === date)
            if (this.taskData[key].next_display_date === date) {
              values.push(key)
            }
          })
        data[date] = values
        values = []
      })
      return data
    }
  },
}
</script>

<style lang="scss" scoped>
.tasks-on-the-date {
  & + & {
    margin-top: 20px;
  }
}
.task {
  margin-bottom: 20px;
  &-date {
    padding: 0 10px 10px;
    font-size: 16px;
    color: #747474;
  }
  &-items {
    list-style: none;
    padding: 0;
  }
  &-item {
    margin-bottom: 10px;
  }
}
</style>
