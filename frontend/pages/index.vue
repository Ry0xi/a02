<template>
  <div class="page-home">
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
    />
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
      tasks: [],
      categoryData: [],
      testTasks: [
        {'id': '1001', 'name': 'タスク１', 'categories': ['0001','0002'], 'isDone': true},
        {'id': '1002', 'name': 'タスク２未完了', 'categories': ['0001'], 'isDone': false},
        {'id': '1003', 'name': 'タスク３タスク３未完了', 'categories': ['0001','0002'], 'isDone': false},
        {'id': '1004', 'name': 'タスク４タスク４タスク４タスク４', 'categories': ['0001','0002', '0003'], 'isDone': true},
        {'id': '1005', 'name': 'タスク５タスク５タスク５タスク５タスク５タスク５タスク５未完了', 'categories': ['0001','0002'], 'isDone': false},
        {'id': '1006', 'name': 'タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６', 'categories': ['0001','0002'], 'isDone': true},
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