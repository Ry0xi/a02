<!--
id:     カテゴリID(既存のものを編集する場合のみ指定)
name:   カテゴリ名(既存のものを編集する場合のみ指定)
color:  カテゴリの色(既存のものを編集する場合のみ指定)
@back:  戻るボタンを押した時に発火するイベント
@done:  完了(追加)ボタンを押した時に発火するイベント
@category:created: 追加ボタンを押して、カテゴリを作成した後に発火するイベント
                   新しいカテゴリデータを返す。{'name': 'タスク名', 'color': '#XXXXXX'}
@category:updated: 追加ボタンを押して、カテゴリを更新した後に発火するイベント
                   更新されたカテゴリデータを返す。{'id': 1 'name': 'タスク名', 'color': '#XXXXXX'}
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
          @click="goBack"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-toolbar-title class="category-editor-header-title">
          <span v-if="categoryId">カテゴリを編集</span>
          <span v-else>カテゴリを追加</span>
        </v-toolbar-title>
      </v-toolbar>
    </v-card-title>

    <!-- 親コンポーネントのv-dialogにおけるscrollableプロパティに対応するためv-card-textを使う -->
    <v-card-text>
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>カテゴリ名</v-list-item-title>
            <v-text-field
              v-model="newCategoryName"
              outlined
              single-line
              autofocus
              placeholder="マイカテゴリ"
              class="mt-1"
            ></v-text-field>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>カテゴリの色</v-list-item-title>
            <v-item-group
              v-model="newCategoryColor"
              mandatory
            >
              <v-row
                v-for="nRow in Math.ceil(colors.length / 5)"
                :key="nRow"
                class="ma-auto align-center justify-center"
              >
                <v-col
                  v-for="nCol in 5"
                  :key="nCol"
                  class="pa-1"
                >
                  <v-item
                    :value="colors[(nCol - 1) + (nRow - 1) * 5]"
                    v-slot="{ active, toggle }"
                  >
                    <v-card
                      @click="toggle"
                      :color="colors[(nCol - 1) + (nRow - 1) * 5]"
                      flat
                      width="100%"
                      :style="{aspectRatio: 1, border: active ? '2px solid #707070' : 'none'}"
                    >
                      <v-scroll-y-transition>
                        <v-icon
                          v-if="active"
                          dark
                          class="icon-selected"
                        >mdi-check</v-icon>
                      </v-scroll-y-transition>
                    </v-card>
                  </v-item>
                </v-col>
              </v-row>
            </v-item-group>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>

    <v-card-actions>
      <v-btn
        block
        depressed
        rounded
        :disabled="!newCategoryName || !newCategoryColor"
        height="42"
        color="primary"
        @click="save"
      >
        <span v-if="categoryId">完了</span>
        <span v-else>追加</span>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
const DEFAULT_COLOR = '#FFC1C1'
export default {
  props: {
    id: {
      type: Number,
      default: null
    },
    name: {
      type: String,
      default: ''
    },
    color: {
      type: String,
      default: DEFAULT_COLOR
    }
  },
  data() {
    return {
      categoryId: this.id,
      newCategoryName: this.name,
      newCategoryColor: this.color,
      colors: ['#FFC1C1','#FF9090','#D2BBF7','#8B89B9','#B9E4FF','#8EA9F4','#FFE989','#FFCB83','#A3E69A','#74B27A']
    }
  },
  watch: {
    id: function(newId) {
      this.categoryId = newId
    },
    name: function(newName) {
      this.newCategoryName = newName
    },
    color: function(newColor) {
      this.newCategoryColor = newColor
    }
  },
  methods: {
    save() {
      // 変化がなかった場合や入力がされていない場合は何もしない
      if (!this.newCategoryName ||
          !this.newCategoryColor || 
          this.id == this.categoryId && this.name == this.newCategoryName && this.color == this.newCategoryColor) {
        
        this.resetData()
        this.$emit('done')
        return
      }

      const newCategoryData = {
        'name': this.newCategoryName,
        'color': this.newCategoryColor
      }

      if (this.categoryId) {
        newCategoryData.id = this.categoryId
        this.$emit('category:updated', newCategoryData)
      } else {
        this.$emit('category:created', newCategoryData)
      }

      this.resetData()
      this.$emit('done')
    },
    goBack() {
      this.resetData()
      this.$emit('back')
    },
    resetData() {
      this.categoryId = ''
      this.newCategoryName = ''
      this.newCategoryColor = DEFAULT_COLOR
    }
  }
}
</script>

<style lang="scss" scoped>
.category-editor {
  &-header-title {
    font-size: 20px;
    font-weight: bold;
    color: #707070;
  }
}

.icon-selected {
  width: 100%;
  height: 100%;
}
</style>