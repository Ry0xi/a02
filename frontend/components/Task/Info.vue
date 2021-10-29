<!--
activator:         ダイアログを起動させるためのエレメントをセレクタで指定。例):activator="#activator"
taskId:            表示するタスクのID
taskTitle:         表示するタスクのタイトル
taskDate:          表示するタスクの最新の表示日
taskDetail:        表示するタスクの内容
categories:        表示するタスクに設定されたカテゴリの配列
isDone:            表示するタスクが完了しているかどうか
categoryData:      カテゴリの情報をもつ配列
@task:deleted:     タスクの削除ボタンを押した時に発火するイベント
@task:updated:     タスクの保存ボタンを押した時に発火するイベント
@category:updated: カテゴリが更新されたときに発火するイベント
                   新しいカテゴリデータを返す。※TaskCategoryEditorを参照
@category:created: カテゴリが新規作成されたときに発火するイベント
                   新しいカテゴリデータを返す。※TaskCategoryEditorを参照
-->
<template>
  <div class="task-info">
    <v-dialog
      v-model="dialog"
      :activator="activator"
      fullscreen
      scrollable
      transition="dialog-bottom-transition"
    >
      <!-- タスクの詳細を表示するダイアログ -->
      <v-card tile>
        <!-- scrollableプロパティに対応するためv-card-titleを使う -->
        <v-card-title class="pa-0">
          <v-toolbar dark flat color="primary">
            <!-- 詳細ダイアログを閉じる -->
            <v-btn v-if="!editable" icon @click="dialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <!-- タスクの変更ダイアログを閉じる -->
            <v-btn v-else icon @click="closeTaskEditor">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <v-toolbar-title v-if="!editable">タスクの詳細</v-toolbar-title>
            <v-toolbar-title v-else>タスクの編集</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <!-- 削除ボタン -->
              <v-btn icon v-if="!editable" @click="openDialogDelete">
                <v-icon>mdi-delete</v-icon>
              </v-btn>

              <!-- 編集ボタン -->
              <v-btn icon v-if="!editable" @click="openTaskEditor">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>

              <!-- 保存ボタン -->
              <v-btn v-else icon @click="updateTask" :disabled="!canChangeData">
                <v-icon>mdi-content-save</v-icon>
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
        </v-card-title>

        <!-- scrollableプロパティに対応するためv-card-textを使う -->
        <v-card-text class="pt-4 px-2">
          <v-list three-line subheader>
            <!-- <v-subheader>基本情報</v-subheader> -->
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>タイトル</v-list-item-title>
                <p v-if="!editable" class="task-info-data">
                  {{ taskTitle }}
                </p>

                <v-text-field
                  v-else
                  v-model="editableTaskTitle"
                  single-line
                  outlined
                  clearable
                  hide-details
                  placeholder="タスク名"
                  class="mt-1"
                >
                </v-text-field>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>直近の表示日</v-list-item-title>
                <p v-if="!editable" class="task-info-data">
                  {{ taskDate }}
                </p>

                <UserFormSingleDate
                  v-else
                  v-model="editableTaskDate"
                  placeholder="2021-01-01"
                />
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <div class="d-flex align-center justify-space-between">
                  <v-list-item-title>カテゴリ</v-list-item-title>
                  <v-btn
                    id="open-category-selector"
                    v-if="editable"
                    text
                    class="pa-0"
                    color="secondary"
                    @click.stop="openCategorySelector"
                  >
                    カテゴリを選択
                    <v-icon class="ml-2">mdi-plus-circle</v-icon>
                  </v-btn>
                </div>

                <TaskCategoryList
                  v-if="editable ? editableCategories[0] : categories[0]"
                  :clearable="editable"
                  @click:clear="deleteCategory($event)"
                  :categories="editable ? editableCategories : categories"
                  :categoryData="categoryData"
                  class="mt-2"
                />
                <v-list-item-subtitle v-else class="px-1">
                  カテゴリが設定されていません
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>内容</v-list-item-title>
                <!-- ここのpタグ内を改行すると表示にも反映されてしまう -->
                <div v-if="!editable">
                  <p v-if="taskDetail" class="task-info-data task-info-detail">{{ taskDetail }}</p>
                  <v-list-item-subtitle v-else class="px-1">
                    タスクの詳細は未入力です
                  </v-list-item-subtitle>
                </div>
                <v-textarea
                  v-else
                  v-model="editableTaskDetail"
                  outlined
                  rows="6"
                  auto-grow
                  no-resize
                  hint="教材のページやURLなどを記入すると便利です"
                  persistent-hint
                  placeholder="タスク内容をここに入力できます"
                  class="mt-1"
                >
                </v-textarea>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-list v-if="!editable">
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>ステータス</v-list-item-title>
                <p v-if="!isDone" class="task-info-data">復習完了</p>
                <p v-else class="task-info-data">復習中</p>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>完了履歴</v-list-item-title>
                <div class="history" v-if="Object.keys(taskHistory).length">
                  <div v-for="task in taskHistory" :key="task.id" class="history-list">
                    <div class="history-date">{{ $formatDate(task.date) }}</div>
                    <div class="history-vallue">{{ feedbackFormat(task.feedback) }}</div>
                  </div>
                </div>
                <v-list-item-subtitle v-else class="px-1">
                  履歴がありません
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- カテゴリを選択するダイアログ -->
    <v-dialog
      v-model="categorySelector"
      scrollable
      max-width="400"
      @click:outside="$refs.categorySelector.save(), closeCategorySelector()"
    >
      <TaskCategorySelector
        ref="categorySelector"
        :categories="editableCategories"
        :categoryData="categoryData"
        @back="closeCategorySelector()"
        @editCategory="openCategoryEditor($event)"
        @createNewCategory="openCategoryEditor(), closeCategorySelector()"
        @change="editableCategories = $event"
      />
    </v-dialog>

    <!-- カテゴリを新規作成・編集するエディタ -->
    <v-dialog
      v-model="categoryEditor"
      scrollable
      max-width="400"
      @click:outside="openCategorySelector(), closeCategoryEditor()"
    >
      <TaskCategoryEditor
        :id="categoryIdForEditor"
        :name="categoryNameForEditor"
        :color="categoryColorForEditor"
        @back="openCategorySelector(), closeCategoryEditor()"
        @done="openCategorySelector(), closeCategoryEditor()"
        @category:created="addCategoryData($event)"
        @category:updated="updateCategoryData($event)"
      />
    </v-dialog>

    <!-- 削除ボタンを押した際に確認するダイアログ -->
    <v-dialog v-model="dialogDelete" max-width="400">
      <v-card>
        <div class="d-flex align-center pa-4">
          <v-icon color="yellow darken-2" class="mr-2">
            mdi-alert-circle-outline
          </v-icon>
          タスクを削除しますか？
        </div>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialogDelete"> キャンセル </v-btn>
          <v-btn
            dark
            depressed
            color="#ef7067"
            @click="
              deleteTask()
              closeDialogDelete()
            "
          >
            削除
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- タスク更新時に表示されるお知らせ -->
    <v-snackbar
      v-model="snackbarUpdate"
      timeout="4000"
      color="secondary"
    >
      タスクを更新しました。
    </v-snackbar>
  </div>
</template>

<script>
export default {
  props: {
    activator: {
      type: String,
      required: true,
    },
    taskId: {
      type: Number,
      required: true,
    },
    taskTitle: {
      type: String,
    },
    categories: {
      type: Array,
      default: () => [],
    },
    isDone: {
      type: Boolean,
    },
    taskDate: {
      type: String,
    },
    taskDetail: {
      type: String,
    },
    categoryData: {
      type: Object,
    },
  },
  data() {
    return {
      dialog: false,
      editable: false,
      snackbarUpdate: false,
      categorySelector: false,
      categoryEditor: false,
      dialogDelete: false,
      categoryIdForEditor: null,
      editableTaskTitle: String,
      editableCategories: Array,
      editableIsDone: Boolean,
      editableTaskDate: String,
      editableTaskDetail: String,
      taskHistory: []
    }
  },
  computed: {
    edited: function () {
      if (
        this.taskTitle == this.editableTaskTitle &&
        JSON.stringify(this.categories) ==
          JSON.stringify(this.editableCategories) &&
        this.isDone == this.editableIsDone &&
        this.taskDate == this.editableTaskDate &&
        this.taskDetail == this.editableTaskDetail
      ) {
        return false
      } else {
        return true
      }
    },
    canChangeData: function () {
      if (this.edited && this.editableTaskTitle && this.editableTaskDate) {
        return true
      } else {
        return false
      }
    },
    categoryNameForEditor: {
      get() {
        return this.categoryIdForEditor
          ? this.categoryData[this.categoryIdForEditor].name
          : ''
      },
    },
    categoryColorForEditor: {
      get() {
        return this.categoryIdForEditor
          ? this.categoryData[this.categoryIdForEditor].color
          : ''
      },
    },
  },
  mounted: function () {
    this.resetDataForEdit()
    this.getTaskHistory()
  },
  methods: {
    getTaskHistory() {
      this.$db.task_date.where('task_id').equals(this.taskId).reverse().sortBy('date').then((response) => {
        this.taskHistory = response.filter((task) => task.is_done === true)
      })
    },
    feedbackFormat(value) {
      if(value === 1) {
        return '普通'
      } else if(value === 2) {
        return '満足'
      } else if(value === 0) {
        return '全然'
      }
    },
    resetDataForEdit() {
      // 編集用のデータを設定値にする
      this.editableTaskTitle = this.taskTitle
      this.editableCategories = this.categories ? this.categories.slice(0, this.categories.length) : []
      this.editableIsDone = this.isDone
      this.editableTaskDate = this.taskDate
      this.editableTaskDetail = this.taskDetail
    },
    openTaskEditor() {
      this.resetDataForEdit()
      this.editable = true
    },
    closeTaskEditor() {
      this.editable = false
    },
    deleteTask() {
      this.$emit('task:deleted', this.taskId)
      this.dialog = false
    },
    updateTask() {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      const updatedTaskData = {
        'id': this.taskId,
        'title': this.editableTaskTitle,
        'category': this.editableCategories,
        'next_display_date': this.editableTaskDate,
        'detail': this.editableTaskDetail,
        'url': null,
      }
      this.$emit('task:updated', updatedTaskData)
      this.editable = false
      this.snackbarUpdate = true
    },
    openCategorySelector() {
      this.categorySelector = true
    },
    closeCategorySelector() {
      this.categorySelector = false
    },
    openCategoryEditor(categoryId) {
      this.categoryIdForEditor = categoryId
      this.categoryEditor = true
    },
    closeCategoryEditor() {
      this.categoryIdForEditor = null
      this.categoryEditor = false
    },
    openDialogDelete() {
      this.dialogDelete = true
    },
    closeDialogDelete() {
      this.dialogDelete = false
    },
    deleteCategory(categoryId) {
      // 編集可能なカテゴリの配列から引数の配列を削除
      const categoryIndex = this.editableCategories.indexOf(categoryId)
      this.$delete(this.editableCategories, categoryIndex)
      console.log('category deleted')
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

<style lang="scss" scoped>
.v-list-item__title {
  padding-bottom: 8px;
  font-size: 15px;
  font-weight: bold;
  color: #606060;
}

.task-info {
  &-data {
    padding: 0 5px;
    font-size: 16px;
  }
  &-detail {
    font-size: 16px;
    white-space: pre-wrap;
    line-height: 1.5;
  }
}

.history {
  font-size: 16px;
  &-list {
    display: flex;
    padding: 10px 5px;
    border-bottom: solid 1px #ddd;
  }
  &-date {
    margin-right: auto;
  }
  &-value {}
}
</style>
