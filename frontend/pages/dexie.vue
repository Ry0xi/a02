<template>
  <div>
    <div class="text-center">dexie.js サンプル</div>
    <v-card class="pa-6" outlined>
      <v-text-field
        v-model="edit.id"
        solo
        outlined
        flat
        label="id"
      ></v-text-field>
      <v-text-field
        v-model="edit.title"
        solo
        outlined
        flat
        label="タスク名"
      ></v-text-field>
      <div class="text-center">{{ message }}</div>
      <v-btn block depressed @click="add" class="my-4" color="primary">
        追加
      </v-btn>
      <v-btn block depressed @click="dbDelete" class="my-4" color="error">
        データベースを削除
      </v-btn>

      <div class="list" v-for="task in tasks" :key="task.id">
        <div class="list_id">{{ task.id }}</div>
        <div class="list_title">{{ task.title }}</div>
        <div class="list_btn">
          <v-btn text @click="remove(task.id)">削除</v-btn>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: null,
      tasks: [],
      edit: {
        id: null,
        title: null,
        detail: null,
        url: null,
        category_id: null,
      },
      default: {
        id: null,
        title: null,
        detail: null,
        url: null,
        category_id: null,
      },
    }
  },
  mounted() {
    this.get()
  },
  methods: {
    async get() {
      await this.$db.task.toArray().then((tasks) => {
        this.tasks = tasks
      })
    },
    add() {
      this.message = null
      this.$db.task
        .add(this.edit)
        .then((tasks) => {
          this.tasks = tasks
          this.message = '追加しました'
        })
        .catch(() => {
          this.message = '追加できませんでした'
        })
      this.edit = Object.assign({}, this.default)
      this.get()
    },
    remove(id) {
      this.$db.task
        .delete(id)
        .then(() => {
          this.message = '削除しました'
        })
        .catch(() => {
          this.message = '追加できませんでした'
        })
      this.get()
    },
    dbDelete() {
      this.$db.delete()
      this.$router.go(this.$router.currentRoute)
    },
  },
}
</script>

<style lang="scss" scoped>
.list {
  display: flex;
  align-items: center;
  padding: 10px 5px;
  border-bottom: solid 1px #ddd;
  &_id {
    width: 20%;
  }
  &_btn {
    margin-left: auto;
  }
}
</style>
