<template>
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
          <v-btn
            v-if="!editable"
            icon
            @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-btn
            v-else
            icon
            @click="editable = false"
          >
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-toolbar-title v-if="!editable">タスクの詳細</v-toolbar-title>
          <v-toolbar-title v-else>タスクの編集</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <!-- 編集ボタン -->
            <v-btn
              icon
              v-if="!editable"
              @click="enableEditing"
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
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>カテゴリ</v-list-item-title>
              <TaskCategoryList
                v-if="categories[0]"
                :categories="categories"
                :categoryData="categoryData"
                style="width: 100%;"
              />
              <v-list-item-subtitle v-else>カテゴリが設定されていません</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        
      </v-card-text>

    </v-card>
  </v-dialog>
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
      editableTaskName: this.taskName,
      editableCategories: this.categories,
      editableIsDone: this.isDone,
      editableTaskDate: this.taskDate,
      editableTaskDetail: this.taskDetail
    }
  },
  computed: {
    edited: function() {
      if (
        this.taskName == this.editableTaskName
        && this.categories == this.editableCategories
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
    }
  },
  methods: {
    enableEditing() {
      this.editable = true
      // 入力フォームにデータバインドをする際に、前の変更が反映されないように、ダイアログを開くたびに初期化
      this.editableTaskName = this.taskName
      this.editableCategories = this.categories
      this.editableIsDone = this.isDone
      this.editableTaskDate = this.taskDate
      this.editableTaskDetail = this.taskDetail
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
    }
  }
}
</script>

<style lang="scss" scoped>
.v-list-item__title {
  font-size: 1.125rem;
}
</style>