<!--
taskId:           タスクのID
taskName:         タスクのタイトル
categories:       タスクに登録しているカテゴリの配列
isDone:           タスクを完了しているかどうか
taskDate:         タスクの表示日
taskDeteil:       タスクの内容
hideDoneBtn:      タスクアイテムに完了ボタンを非表示にするかどうか
isAutoAddedTask:  タスクの自動追加のオンオフ
@task:done:       タスク完了時に発火するイベント。※TaskDoneBtnを参照
-->
<template>
  <v-card class="task-item" outlined>
    <v-card-title class="task-item-name">{{ taskName }}</v-card-title>
    <TaskCategoryList :categoryData="categoryData" :categories="categories" />

    <TaskDoneBtn :taskDateId="taskId" v-if="!isDone" v-show="!hideDoneBtn" @task:done="doneTask" />
  </v-card>
</template>

<script>
export default {
  props: {
    taskId: {
      type: Number,
      required: true,
    },
    taskName: {
      type: String,
    },
    categories: {
      type: Array,
    },
    isDone: {
      type: Boolean,
    },
    taskDate: {
      type: String,
      default: '未入力',
    },
    taskDetail: {
      type: String,
      default: '未入力',
    },
    categoryData: {
      type: Object,
    },
    // 完了ボタンを非表示にするかどうか
    hideDoneBtn: {
      type: Boolean,
      default: false,
    },
    isAutoAddedTask: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    doneTask(taskId) {
      this.$emit('task:done', taskId)
    },
  },
}
</script>

<style lang="scss" scoped>
.task-item {
  padding: 6px 16px;

  &-name {
    font-size: 18px;
    margin: 5px 0;
    padding: 0;
  }
}
</style>
