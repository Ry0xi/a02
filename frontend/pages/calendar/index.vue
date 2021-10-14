<template>
  <div>
    <v-card outlined class="mb-4">
      <CalendarMonth v-model="date">
        <template #activator="{ on }">
          <v-btn v-on="on" text class="my-2">
            <v-icon class="mr-2" color="primary">mdi-calendar-month</v-icon>
            {{ formatDate }}
          </v-btn>
        </template>
      </CalendarMonth>

      <v-calendar v-model="date" color="primary" style="overflow: hidden">
        <template v-slot:day-label="{ date, day }">
          <div class="dayBox">
            <div class="dayBox_day">{{ day }}</div>
          </div>
          <draggable
            @add="onAdd(date)"
            :group="{ name: 'ITEMS' }"
            class="dayBox_drag"
            v-model="setItem"
          >
          </draggable>
        </template>
      </v-calendar>
    </v-card>

    <v-card outlined>
      <div class="taskBox">
        <div>
          <draggable
            v-model="tasks"
            class="taskBox_items"
            :group="{ name: 'ITEMS', pull: 'clone', put: false }"
          >
            <div v-for="task in tasks" :key="task.id" class="taskItem">
              {{ task.name }}
            </div>
          </draggable>
        </div>
      </div>
    </v-card>
    <TaskCreate
      v-model="dialog"
      :taskName="task.name"
      :taskDate="task.date"
      :isDone="false"
      :categoryData="{}"
      :tasks="[]"
    />
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  components: {
    draggable,
  },
  data() {
    return {
      header: {
        title: 'カレンダー',
      },
      date: new Date().toISOString().substr(0, 9),
      dialog: false,
      task: {
        name: '',
        date: '',
      },
      setItem: [],
      tasks: [
        { id: 1, name: 'task1' },
        { id: 2, name: 'task2' },
        { id: 3, name: 'task3' },
        { id: 4, name: 'task4' },
        { id: 5, name: 'task5' },
        { id: 6, name: 'task6' },
      ],
    }
  },
  computed: {
    // 日付をフォーマット
    formatDate() {
      const dt = new Date(this.date)
      const year = dt.getFullYear()
      const month = dt.getMonth() + 1
      return `${year}年${month}月`
    },
  },
  mounted() {
    this.updateHeader()
  },
  methods: {
    updateHeader() {
      // タイトルとして使いたい情報を渡す
      this.$nuxt.$emit('updateHeader', this.header.title)
    },
    // 追加時の処理
    onAdd(date) {
      this.task.name = this.setItem[0].name
      this.task.date = date
      this.dialog = true
      this.setItem = []
    },
  },
}
</script>

<style lang="scss">
.taskBox {
  overflow-y: scroll;
  width: 100%;
  height: 200px;
  padding: 12px;
  background-color: #fff;
  &_items {
    display: flex;
    flex-wrap: wrap;
  }
  &_item {
    padding: 5px 15px;
    margin: 5px;
    background-color: #fbeab9;
    border-radius: 10px;
  }
}

.taskItem {
  padding: 5px 15px;
  margin: 5px;
  background-color: #fbeab9;
  border-radius: 10px;
  cursor: pointer;
}

.dayBox {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  &_day {
    width: 100%;
    padding: 10px 0;
    font-size: 14px;
    color: #444;
  }
  &_active {
    background-color: red;
  }

  &_drag {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
}

.sortable-chosen {
  width: 35px;
  height: 35px;
  padding: 0;
  margin: 0;
  text-indent: 100%;
  overflow: hidden;
  white-space: nowrap;
  background-color: rgb(255, 195, 42);
  opacity: 0.5;
}
</style>
