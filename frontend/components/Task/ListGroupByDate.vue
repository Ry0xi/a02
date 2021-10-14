<!--
  shownTasks: 0 -> 全て、1 -> 未完了のタスクのみ、2 -> 完了のみ
  tasks: {'id': String, 'name': String, date: String, 'categories': Array, 'isDone': Boolean}の配列
  categoryData: 各カテゴリのデータ。[categoryId(String)]: {'name': String, 'color': String}
  @category:updated: カテゴリが更新されたときに発火するイベント
                     新しいカテゴリデータを返す。※TaskCategoryEditorを参照
  @category:created: カテゴリが新規作成されたときに発火するイベント
                     新しいカテゴリデータを返す。※TaskCategoryEditorを参照
-->
<template>
  <div class="task-list-group-by-date">
    <div class="tasks-on-the-date" v-for="date in datesInTasks" :key="date">
      <h3 class="tasks-date">{{date}}</h3>
      <ul class="task-list">
        <li class="task-list-item" v-for="task in tasksGroupByDate[date]" :key="task.id">
          <TaskItem
            :id="'activator'+task.id"
            v-show="shownTasks == 0 || isShownTask(task)"
            :taskName="task.name"
            :taskDate="task.date"
            :taskDetail="task.detail"
            :categories="task.categories"
            :isDone="task.isDone"
            :categoryData="categoryData"
            :hideDoneBtn="hideDoneBtn"
          />
          <TaskInfo
            :activator="'#activator'+task.id"
            :taskId="task.id"
            :taskName="task.name"
            :taskDate="task.date"
            :taskDetail="task.detail"
            :categories="task.categories"
            :isDone="task.isDone"
            :categoryData="categoryData"
            @task:deleted="deleteTask($event)"
            @task:updated="updateTask($event)"
            @category:updated="updateCategoryData($event)"
            @category:created="addCategoryData($event)"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    shownTasks: {
      type: Number,
      default: 0
    },
    tasks: {
      type: Array
    },
    categoryData: {
      type: Object
    },
    hideDoneBtn: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    isShownTask: function(task) {
      // すべて表示する
      if (this.shownTasks === 0) {
        return true
      }

      const taskType = task.isDone ? 2 : 1
      if (this.shownTasks === taskType) {
        return true
      } else {
        return false
      }
    },
    deleteTask: function(taskId) {
      this.$emit('task:deleted', taskId)
    },
    updateTask: function(updatedData) {
      // 親コンポーネントに変更後のタスクオブジェクトを伝える
      this.$emit('task:updated', updatedData)
    },
    updateCategoryData(updatedCategoryData) {
      this.$emit('category:updated', updatedCategoryData)
    },
    addCategoryData(newCategoryData) {
      this.$emit('category:created', newCategoryData)
    }
  },
  computed: {
    datesInTasks: function() {
      // 昇順にソートされ、重複のない日付の配列
      return [...new Set(this.tasks.map((task) => task.date))].sort()
    },
    tasksGroupByDate: function() {
      let groupedTasks = {}
      this.datesInTasks.forEach(date => {
        groupedTasks[date] = this.tasks.filter((task) => task['date'] === date)
      })
      return groupedTasks
    }
  }
}
</script>

<style lang="scss" scoped>
.tasks-on-the-date {
  & + & {
    margin-top: 24px;
  }
}

.tasks-date {
  color: #525252;
}

.task-list {
  list-style: none;
  padding: 0;

  &-item + &-item{
    margin-top: 16px;
  }
}
</style>