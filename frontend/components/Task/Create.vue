<!--
activator:         ダイアログを起動させるためのエレメントをセレクタで指定。例):activator="#activator"
taskName:          表示するタスクのタイトル
taskDate:          表示するタスクの最新の表示日
taskDetail:        表示するタスクの内容
categories:        表示するタスクに設定されたカテゴリの配列
isDone:            表示するタスクが完了しているかどうか
categoryData:      カテゴリの情報をもつ配列
tasks:             全てのタスクのデータ
@task:created:     タスクの保存ボタンを押した時に発火するイベント
                   タスクオブジェクトを返す
                   {
                     'name': this.editableTaskName,
                     'categories': this.editableCategories,
                     'isDone': this.editableIsDone,
                     'date': this.editableTaskDate,
                     'detail': this.editableTaskDetail
                   }
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
            <!-- タスクの変更ダイアログを閉じる -->
            <v-btn icon @click="closeDialog">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>タスクの追加</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <!-- 保存ボタン -->
              <v-btn icon @click="createTask" :disabled="!canChangeData">
                <v-icon>mdi-check</v-icon>
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
        </v-card-title>

        <!-- scrollableプロパティに対応するためv-card-textを使う -->
        <v-card-text>
          <v-list three-line subheader>
            <v-subheader>基本情報</v-subheader>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>タスクタイトル</v-list-item-title>

                <v-text-field
                  v-model="editableTaskName"
                  single-line
                  outlined
                  clearable
                  placeholder="タスク名"
                  autofocus
                  class="mt-1"
                >
                </v-text-field>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>直近の表示日</v-list-item-title>

                <UserFormSingleDate
                  v-model="editableTaskDate"
                  placeholder="2021-01-01"
                />
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content style="position: relative">
                <v-list-item-title> カテゴリ </v-list-item-title>
                <v-btn
                  id="open-category-selector"
                  text
                  color="secondary"
                  style="position: absolute; top: 5px; right: 0"
                  @click.stop="openCategorySelector"
                >
                  <v-icon>mdi-plus-circle-outline</v-icon>
                  カテゴリーを選択
                </v-btn>

                <TaskCategoryList
                  v-if="editableCategories[0]"
                  :clearable="true"
                  @click:clear="deleteCategory($event)"
                  :categories="editableCategories"
                  :categoryData="categoryData"
                  class="mt-2"
                />
                <v-list-item-subtitle v-else
                  >カテゴリが設定されていません</v-list-item-subtitle
                >
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>内容</v-list-item-title>
                <v-textarea
                  v-model="editableTaskDetail"
                  outlined
                  rows="6"
                  auto-grow
                  no-resize
                  hint="教材のページやURLなどを記入すると便利です"
                  persistent-hint
                  placeholder="タスク内容をここに入力できます。"
                  class="mt-1"
                >
                </v-textarea>
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

    <!-- タスク追加時に表示されるお知らせ -->
    <v-snackbar v-model="snackbarCreate" timeout="4000" color="secondary">
      タスクを追加しました。
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
    taskName: {
      type: String,
      default: '',
    },
    categories: {
      type: Array,
      default: () => [],
    },
    isDone: {
      type: Boolean,
      default: false,
    },
    taskDate: {
      type: String,
      default: '',
    },
    taskDetail: {
      type: String,
      default: '',
    },
    categoryData: {
      type: Object,
    },
  },
  data() {
    return {
      dialog: false,
      snackbarCreate: false,
      categorySelector: false,
      categoryEditor: false,
      categoryIdForEditor: null,
      editableTaskName: String,
      editableCategories: Array,
      editableIsDone: Boolean,
      editableTaskDate: String,
      editableTaskDetail: String,
    }
  },
  computed: {
    edited: function () {
      if (
        this.taskName == this.editableTaskName &&
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
      if (this.edited && this.editableTaskName && this.editableTaskDate) {
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
  created: function () {
    this.resetDataForEdit()
  },
  methods: {
    resetDataForEdit() {
      // 編集用のデータを設定値にする
      this.editableTaskName = this.taskName
      this.editableCategories = this.categories
        ? this.categories.slice(0, this.categories.length)
        : []
      this.editableIsDone = this.isDone
      this.editableTaskDate = this.taskDate
      this.editableTaskDetail = this.taskDetail
    },
    closeDialog() {
      this.dialog = false
    },
    createTask() {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      const createdTaskData = {
        name: this.editableTaskName,
        categories: this.editableCategories,
        isDone: this.editableIsDone,
        date: this.editableTaskDate,
        detail: this.editableTaskDetail,
      }
      this.$emit('task:created', createdTaskData)
      this.snackbarCreate = true
      this.resetDataForEdit()
      this.closeDialog()
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
.task-info {
  &-data {
    font-size: 1.125rem;
  }

  &-detail {
    white-space: pre-wrap;
    line-height: 1.5;
  }
}
</style>
