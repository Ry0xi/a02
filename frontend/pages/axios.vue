<template>
  <div>
    <div class="text-center">axios テスト</div>
    <v-card class="pa-6" outlined>
      <v-text-field
        v-model="edit.category_name"
        solo
        outlined
        flat
        label="カテゴリ名"
      ></v-text-field>
      <v-text-field
        v-model="edit.color_code"
        solo
        outlined
        flat
        label="カラーコード"
      ></v-text-field>
      <ErrorMessage :message="message" />
      <v-btn block depressed @click="add" class="my-4" color="primary">
        追加
      </v-btn>

      <v-btn block depressed @click="token" class="my-4" color="primary">
        無効なトークンに変更
      </v-btn>

      <div class="list" v-for="category in categories" :key="category.id">
        <div class="list_id">{{ category.category_name }}</div>
        <div class="list_title">{{ category.color_code }}</div>
        <div class="list_btn">
          <v-btn text @click="remove(category.id)">削除</v-btn>
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
      categories: [],
      edit: {
        category_name: null,
        color_name: null,
      },
      default: {
        id: null,
        category_name: null,
        color_name: null,
      },
    }
  },
  mounted() {
    this.get()
  },
  methods: {
    async get() {
      await this.$axios.get('/api/category/').then((response) => {
        this.categories = response.data
      })
    },
    async add() {
      this.message = null
      await this.$axios
        .post('/api/category/', this.edit)
        .then(() => {
          this.message = '追加しました'
        })
        .catch((error) => {
          this.message = error.response.data
        })
      this.edit = Object.assign({}, this.default)
      this.get()
    },
    async remove(id) {
      await this.$axios
        .delete(`/api/category/${id}/`)
        .then(() => {
          this.message = '削除しました'
        })
        .catch(() => {
          this.message = '追加できませんでした'
        })
      this.get()
    },
    token() {
      this.$auth.setUserToken('')
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
