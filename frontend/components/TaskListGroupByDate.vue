<!--
  shownTasks: 0 -> 全て、1 -> 未完了のタスクのみ、2 -> 完了のみ
  tasks: {'id': String, 'name': String, date: String, 'categories': Array, 'isDone': Boolean}の配列
  categoryData: 各カテゴリのデータ。[categoryId(String)]: {'name': String, 'color': String}
-->
<template>
  <div class="task-list-group-by-date">
    <div class="tasks-on-the-date" v-for="date in datesInTasks" :key="date">
      <h3 class="tasks-date text-h3">{{date}}</h3>
      <ul class="task-list">
        <li class="task-list-item" v-for="task in tasksGroupByDate[date]" :key="task.id">
          <TaskItem
            v-if="shownTasks == 0 || isShownTask(task)"
            :taskName="task.name"
            :categories="task.categories"
            :isDone="task.isDone"
            :categoryData="categoryData"
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
.task-list {
  list-style: none;
  padding: 0;

  &-item + &-item{
    margin-top: 16px;
  }
}
</style>