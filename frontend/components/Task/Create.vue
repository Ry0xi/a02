<!--
v-model:           ダイアログ
taskName:          表示するタスクのタイトル
taskDate:          表示するタスクの最新の表示日
taskDetail:        表示するタスクの内容
categories:        表示するタスクに設定されたカテゴリの配列
categoryData:      カテゴリの情報をもつ配列
tasks:             全てのタスクのデータ
@task:created:     タスクの保存ボタンを押した時に発火するイベント
                   タスクオブジェクトを返す
                   {
                     'title': this.editableTaskName,
                     'category': this.editableCategories,
                     'date': this.editableTaskDate,
                     'detail': this.editableTaskDetail
                   }
@category:updated: カテゴリが更新されたときに発火するイベント
                   新しいカテゴリデータを返す。※TaskCategoryEditorを参照
@category:created: カテゴリが新規作成されたときに発火するイベント
                   新しいカテゴリデータを返す。※TaskCategoryEditorを参照
-->
<template>
  <div class="task-create">
    <v-dialog v-model="setDialog" fullscreen transition="dialog-bottom-transition">
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
                <v-icon>mdi-content-save</v-icon>
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
        </v-card-title>
        <!-- scrollableプロパティに対応するためv-card-textを使う -->
        <v-card-text class="px-2">
          <v-list three-line subheader>
            <v-subheader>基本情報</v-subheader>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>タイトル</v-list-item-title>

                <v-text-field
                  v-model="editableTaskName"
                  single-line
                  outlined
                  clearable
                  hide-details
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
              <v-list-item-content>
                <div class="d-flex align-center justify-space-between">
                  <v-list-item-title>カテゴリ</v-list-item-title>
                  <v-btn
                    id="open-category-selector"
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
                  v-if="editableCategories[0]"
                  :clearable="true"
                  @click:clear="deleteCategory($event)"
                  :categories="editableCategories"
                  :categoryData="categoryData"
                  class="mt-2"
                />
                <v-list-item-subtitle v-else>
                  カテゴリが設定されていません
                </v-list-item-subtitle>
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
    <v-snackbar
      v-model="snackbarCreate"
      timeout="2000"
    >
      タスクを追加しました。
    </v-snackbar>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'dialog',
    event: 'update',
  },
  props: {
    dialog: {
      type: Boolean,
    },
    taskName: {
      type: String,
      default: '',
    },
    categories: {
      type: Array,
      default: () => [],
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
      snackbarCreate: false,
      categorySelector: false,
      categoryEditor: false,
      categoryIdForEditor: null,
      editableTaskName: String,
      editableCategories: Array,
      editableTaskDate: String,
      editableTaskDetail: String,
    }
  },
  computed: {
    setDialog: {
      get() {
        return this.dialog
      },
      set(value) {
        return this.$emit('update', value)
      },
    },
    edited: function () {
      if (
        this.taskName == this.editableTaskName &&
        JSON.stringify(this.categories) ==
          JSON.stringify(this.editableCategories) &&
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
  watch: {
    setDialog() {
      if (this.setDialog === true) {
        this.setData()
      }
    },
  },
  methods: {
    setData() {
      this.editableTaskName = this.taskName
      this.editableCategories = this.categories
        ? this.categories.slice(0, this.categories.length)
        : []
      this.editableTaskDate = this.taskDate
      this.editableTaskDetail = this.taskDetail
    },
    closeDialog() {
      this.setDialog = false
    },
    createTask() {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      const createdTaskData = {
        'title': this.editableTaskName,
        'category': this.editableCategories,
        'next_display_date': this.editableTaskDate,
        'detail': this.editableTaskDetail
      }
      this.$emit('task:created', createdTaskData)
      this.snackbarCreate = true
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
.task-create {
  &-data {
    font-size: 1.125rem;
  }

  &-detail {
    white-space: pre-wrap;
    line-height: 1.5;
  }
}
</style>
