<!--
activator:         ダイアログを起動させるためのエレメントをセレクタで指定。例):activator="#activator"
taskId:            表示するタスクのID
taskName:          表示するタスクのタイトル
taskDate:          表示するタスクの最新の表示日
taskDetail:        表示するタスクの内容
categories:        表示するタスクに設定されたカテゴリの配列
isDone:            表示するタスクが完了しているかどうか
categoryData:      カテゴリの情報をもつ配列
@task:deleted:     タスクの削除ボタンを押した時に発火するイベント
@task:updated:     タスクの保存ボタンを押した時に発火するイベント
@category:updated: カテゴリが更新されたときに発火するイベント
                   新しいカテゴリデータを返す。{ '0005': {'name': 'タスク名', 'color': '#XXXXXX'} }
@category:created: カテゴリが新規作成されたときに発火するイベント
                   新しいカテゴリデータを返す。{ '0005': {'name': 'タスク名', 'color': '#XXXXXX'} }
-->
<template>
  <div class="task-info">
    <v-dialog
      v-model="dialog"
      :activator="activator"
      fullscreen
      scrollable
    >
      <!-- タスクの詳細を表示するダイアログ -->
      <v-card tile>
        <!-- scrollableプロパティに対応するためv-card-titleを使う -->
        <v-card-title class="pa-0">
          <v-toolbar
            dark
            flat
            color="primary"
          >
            <!-- 詳細ダイアログを閉じる -->
            <v-btn
              v-if="!editable"
              icon
              @click="dialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <!-- タスクの変更ダイアログを閉じる -->
            <v-btn
              v-else
              icon
              @click="closeTaskEditor"
            >
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <v-toolbar-title v-if="!editable">タスクの詳細</v-toolbar-title>
            <v-toolbar-title v-else>タスクの編集</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <!-- 削除ボタン -->
              <v-btn
                icon
                v-if="!editable"
                @click="deleteTask"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>

              <!-- 編集ボタン -->
              <v-btn
                icon
                v-if="!editable"
                @click="openTaskEditor"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>

              <!-- 保存ボタン -->
              <v-btn
                v-else
                icon
                @click="updateTask"
                :disabled="!canChangeData"
              >
                <v-icon>mdi-content-save</v-icon>
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
        </v-card-title>
        
        <!-- scrollableプロパティに対応するためv-card-textを使う -->
        <v-card-text>
          <v-list
            three-line
            subheader
          >
            <v-subheader>基本情報</v-subheader>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>タスクタイトル</v-list-item-title>
                <v-list-item-subtitle v-if="!editable">{{ taskName }}</v-list-item-subtitle>
                <v-text-field
                  v-else
                  v-model="editableTaskName"
                  single-line
                  outlined
                  clearable
                  placeholder="タスク名"
                  class="mt-1"
                >
                </v-text-field>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>直近の表示日</v-list-item-title>
                <v-list-item-subtitle v-if="!editable">{{ taskDate }}</v-list-item-subtitle>
                <UserFormSingleDate
                  v-else
                  v-model="editableTaskDate"
                  placeholder="2021-01-01"
                />
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content style="position: relative;">
                <v-list-item-title>
                  カテゴリ
                </v-list-item-title>
                <v-btn
                  id="open-category-selector"
                  v-if="editable"
                  text
                  color="secondary"
                  style="position: absolute; top: 5px; right: 0;"
                  @click.stop="openCategorySelector"
                >
                  <v-icon>mdi-plus-circle-outline</v-icon>
                  カテゴリーを選択
                </v-btn>
                
                <TaskCategoryList
                  v-if="editable ? editableCategories[0] : categories[0]"
                  :clearable="editable"
                  @click:clear="deleteCategory($event)"
                  :categories="editable ? editableCategories : categories"
                  :categoryData="categoryData"
                  class="mt-2"
                />
                <v-list-item-subtitle v-else>カテゴリが設定されていません</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>内容</v-list-item-title>
                <v-list-item-subtitle v-if="!editable">{{ taskDetail }}</v-list-item-subtitle>
                <v-textarea
                  v-else
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
      @click:outside="$refs.categorySelector.save(), closeCategorySelector()"
    >
      <TaskCategorySelector
        ref="categorySelector"
        :categories="editableCategories"
        :categoryData="categoryData"
        @back="closeCategorySelector()"
        @editCategory="openCategoryEditor($event)"
        @createNewCategory="openCategoryEditor(''), closeCategorySelector()"
        @change="editableCategories = $event"
      />
    </v-dialog>

    <!-- カテゴリを新規作成・編集するエディタ -->
    <v-dialog
      v-model="categoryEditor"
      scrollable
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

    <!-- タスク削除時に表示されるお知らせ -->
    <v-snackbar
      v-model="snackbar"
      timeout="4000"
      color="brown darken-4"
    >
      タスクを削除しました。
    </v-snackbar>
  </div>
</template>

<script>
export default {
  props: {
    activator: {
      type: String,
      required: true
    },
    taskId: {
      type: String,
      required: true
    },
    taskName: {
      type: String
    },
    categories: {
      type: Array
    },
    isDone: {
      type: Boolean
    },
    taskDate: {
      type: String
    },
    taskDetail: {
      type: String
    },
    categoryData: {
      type: Object
    },
  },
  data() {
    return {
      dialog: false,
      editable: false,
      snackbar: false,
      categorySelector: false,
      categoryEditor: false,
      categoryIdForEditor: '',
      editableTaskName: String,
      editableCategories: Array,
      editableIsDone: Boolean,
      editableTaskDate: String,
      editableTaskDetail: String
    }
  },
  computed: {
    edited: function() {
      if (
        this.taskName == this.editableTaskName
        && JSON.stringify(this.categories) == JSON.stringify(this.editableCategories)
        && this.isDone == this.editableIsDone
        && this.taskDate == this.editableTaskDate
        && this.taskDetail == this.editableTaskDetail
      ) {
        return false
      } else {
        return true
      }
    },
    canChangeData: function() {
      if (this.edited && this.editableTaskName && this.editableTaskDate) {
        return true
      } else {
        return false
      }
    },
    categoryNameForEditor: {
      get() {
        return this.categoryIdForEditor ? this.categoryData[this.categoryIdForEditor].name : ''
      }
    },
    categoryColorForEditor: {
      get() {
        return this.categoryIdForEditor ? this.categoryData[this.categoryIdForEditor].color : ''
      }
    }
  },
  created: function() {
    this.resetDataForEdit()
  },
  methods: {
    resetDataForEdit() {
      // 編集用のデータを設定値にする
      this.editableTaskName = this.taskName
      this.editableCategories = this.categories.slice(0, this.categories.length)
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
      this.snackbar = true
    },
    updateTask() {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      const updatedTaskData = {
        'id': this.taskId,
        'name': this.editableTaskName,
        'categories': this.editableCategories,
        'isDone': this.editableIsDone,
        'date': this.editableTaskDate,
        'detail': this.editableTaskDetail
      }
      this.$emit('task:updated', updatedTaskData)
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
    }
  }
}
</script>

<style lang="scss" scoped>
.v-list-item__title {
  font-size: 1.125rem;
}
</style>