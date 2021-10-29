<!--
categoryData:      カテゴリの情報をもつ配列
@task:created:     タスクの保存ボタンを押した時に発火するイベント
                   タスクオブジェクトを返す ※TaskCreateを参照
@category:updated: カテゴリが更新されたときに発火するイベント
                   新しいカテゴリデータを返す。※TaskCategoryEditorを参照
@category:created: カテゴリが新規作成されたときに発火するイベント
                   新しいカテゴリデータを返す。※TaskCategoryEditorを参照
-->
<template>
  <div class="task-add-fab">
    <v-btn
      fab
      fixed
      elevation="8"
      color="primary"
      style="bottom: 69px; right: 13px"
      @click="dialog = true"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>

    <TaskCreate
      v-model="dialog"
      :isDone="false"
      :categoryData="categoryData"
      @task:created="createTask($event)"
      @category:updated="updateCategoryData($event)"
      @category:created="addCategoryData($event)"
    />
  </div>
</template>

<script>
export default {
  props: {
    categoryData: {
      type: Object,
    },
  },
  data() {
    return {
      dialog: false,
    }
  },
  methods: {
    createTask(createdTaskData) {
      this.$emit('task:created', createdTaskData)
    },
    updateCategoryData(updatedCategoryData) {
      this.$emit('category:updated', updatedCategoryData)
    },
    addCategoryData(newCategoryData) {
      this.$emit('category:created', newCategoryData)
    },
  },
}
</script>

<style lang="scss" scoped></style>
