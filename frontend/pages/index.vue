<template>
  <div class="page-home">
    <TaskAddFAB
      :categoryData="testCategoryData"
      :tasks="testTasks"
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
    <TaskList
      :shownTasks="activeTab"
      :tasks="testTasks"
      :categoryData="testCategoryData"
      @task:deleted="deleteTaskData($event)"
      @task:updated="updateTaskData($event)"
      @category:updated="updateCategoryData($event)"
      @category:created="addCategoryData($event)"
    />
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      header: {
        title: 'ホーム'
      },
      activeTab: 1,
      tasks: [],
      categoryData: [],
      testTasks: [
        {'id': '1001', 'name': 'タスク１', 'date': '2021-02-27', 'detail': '教材Aのp23~36を学んで、問題集p41~44を解く。', 'categories': ['0001','0002'], 'isDone': true},
        {'id': '1002', 'name': 'タスク２未完了', 'date': '2021-02-27', 'detail': '', 'categories': ['0001'], 'isDone': false},
        {'id': '1003', 'name': 'タスク３タスク３未完了', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002'], 'isDone': false},
        {'id': '1004', 'name': 'タスク４タスク４タスク４タスク４', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002', '0003'], 'isDone': true},
        {'id': '1005', 'name': 'タスク５タスク５タスク５タスク５タスク５タスク５タスク５未完了', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002','0003'], 'isDone': false},
        {'id': '1006', 'name': 'タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002'], 'isDone': true},
      ],
      testCategoryData: {
        '0001': {'name': 'カテゴリ1カテゴリ1', 'color': '#FFC1C1'},
        '0002': {'name': 'カテゴリ2', 'color': '#FF9090'},
        '0003': {'name': 'カテゴリ3', 'color': '#D2BBF7'}
      }
    }
  },
  mounted() {
    this.updateHeader()
    this.fetchTaskData()
  },
  methods: {
    fetchTaskData() {
      // 仮
      // this.tasksにAPIで取得したタスクデータを保存
      console.log('fetchTaskData()')
    },
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
    addTaskData(newTaskData) {
      this.testTasks.splice(0, 0, newTaskData)
      console.log('add new task')
      console.log('new:')
      console.log(this.testTasks)
    },
    deleteTaskData(taskId) {
      // 仮
      console.log('deletedTask:')
      console.log(this.testTasks.find(task => task.id == taskId))
    },
    updateTaskData(updatedData) {
      const taskId = updatedData.id
      const targetTaskIndex = this.testTasks.findIndex((task) => {
        return task.id == taskId
      })
      
      Object.keys(updatedData).forEach(key => {
        if (key != 'id') {
          this.$set(this.testTasks[targetTaskIndex], key, updatedData[key])
        }
      })

      console.log('task updated.')
    },
    updateCategoryData(updatedCategoryData) {
      // カテゴリデータを更新
      const updatedCategoryId = Object.keys(updatedCategoryData)[0]

      Object.keys(this.testCategoryData[updatedCategoryId]).forEach(key => {
        this.$set(this.testCategoryData[updatedCategoryId], key, updatedCategoryData[updatedCategoryId][key])
      });

      console.log('category updated.')
    },
    addCategoryData(newCategoryData) {
      // カテゴリデータを追加
      const addedCategoryId = Object.keys(newCategoryData)[0]

      this.$set(this.testCategoryData, addedCategoryId, newCategoryData[addedCategoryId])

      console.log('category created.')
    }
  }
}
</script>