<template>
  <TaskListGroupByDate
    :shownTasks="0"
    :tasks="testTasks"
    :categoryData="testCategoryData"
  />
</template>

<script>
export default {
  data() {
    return {
      header: {
        title: 'タスク一覧'
      },
      tasks: [],
      categoryData: [],
      testTasks: [
        {'id': '1001', 'name': 'タスク１', 'date': '2021-3-20', 'categories': ['0001','0002'], 'isDone': true},
        {'id': '1002', 'name': 'タスク２未完了', 'date': '2021-3-15', 'categories': ['0001'], 'isDone': false},
        {'id': '1003', 'name': 'タスク３タスク３未完了', 'date': '2021-3-16', 'categories': ['0001','0002'], 'isDone': false},
        {'id': '1004', 'name': 'タスク４タスク４タスク４タスク４', 'date': '2021-3-17', 'categories': ['0001','0002', '0003'], 'isDone': true},
        {'id': '1005', 'name': 'タスク５タスク５タスク５タスク５タスク５タスク５タスク５未完了', 'date': '2021-3-18', 'categories': ['0001','0002'], 'isDone': false},
        {'id': '1006', 'name': 'タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６', 'date': '2021-3-18', 'categories': ['0001','0002'], 'isDone': true},
      ],
      testCategoryData: {
        '0001': {'name': 'カテゴリ1', 'color': '#FFE5DE'},
        '0002': {'name': 'カテゴリ2', 'color': '#CBD8FC'},
        '0003': {'name': 'カテゴリ3', 'color': '#E6C4FF'}
      }
    }
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    }
  }
}
</script>