<!--
categories:       タスクに登録されているカテゴリのIDのリスト
categoryData:     全てのカテゴリのデータの配列
                  ['0001': {'name': 'カテゴリ１', 'color': '#XXXXXX'},
                  '0002': {'name': 'カテゴリ２', 'color': '#XXXXXX'},]
@back:            戻るボタンを押した時に発火するイベント
@createNewCategory:  カテゴリの新規作成ボタンを押した時に発火するイベント
@editCategory:    カテゴリの編集ボタンを押した時に発火するイベント
                  編集するカテゴリのidを渡す
@change:          タスクに登録されたカテゴリに変更があった際に発火するイベント
                  変更後のカテゴリの配列を返す
-->
<template>
  <v-card flat>
    <!-- 親コンポーネントのv-dialogにおけるscrollableプロパティに対応するためv-card-titleを使う -->
    <v-card-title class="pa-0">
      <v-toolbar
        flat
        class="transparent"
      >
        <v-btn
          icon
          color="secondary"
          @click="back()"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title class="category-selector-header-title">カテゴリを選択</v-toolbar-title>
      </v-toolbar>
    </v-card-title>
    
    <!-- 親コンポーネントのv-dialogにおけるscrollableプロパティに対応するためv-card-textを使う -->
    <v-card-text>
      <v-list>
        <v-list-item-group
          v-model="newCategories"
          multiple
        >
          <v-list-item
            v-for="(category, categoryId) in categoryData"
            :key="categoryId"
            :value="categoryId"
          >
            <template v-slot:default="{ active }">
              <v-card
                width="36"
                max-width="36"
                height="36"
                flat
                :color="category.color"
                class="mr-2 category-list-color"
              ></v-card>
              <v-list-item-content>
                <v-list-item-title v-text="category.name"></v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-checkbox
                  :input-value="active"
                  color="primary"
                ></v-checkbox>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn
                  icon
                  color="#707070"
                  @click.stop="$emit('editCategory', Number(categoryId))"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </v-list-item-action>
            </template>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card-text>

    <v-card-actions>
      <v-btn
        text
        color="secondary"
        class="mx-auto"
        @click="$emit('createNewCategory')"
      >
        <v-icon>mdi-plus-circle-outline</v-icon>
        カテゴリを新規作成
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    categories: Array,
    categoryData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      newCategories: this.categories
    }
  },
  watch: {
    categories: function(newArray) {
      this.newCategories = newArray
    }
  },
  methods: {
    back() {
      this.save()
      this.$emit('back')
    },
    save() {
      if (JSON.stringify(this.categories) == JSON.stringify(this.newCategories)) {
        return true
      } else {
        // 変更があった場合はイベントを発火。
        this.$emit('change', this.newCategories)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.category-selector {
  &-header-title {
    font-size: 20px;
    font-weight: bold;
    color: #707070;
  }
}

.category-list {
  &-color {
    border-radius: 40%;
  }
}

.theme--light.v-list-item--active::before,
.theme--dark.v-list-item--active::before {
  // カテゴリ選択時の背景色を削除
  opacity: 0;
}
</style>