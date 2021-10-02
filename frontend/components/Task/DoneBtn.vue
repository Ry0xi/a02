<template>
  <v-dialog
    max-width="300"
    v-model="dialog"
    @click:outside="closeDialog"
  >
    <!-- 完了ボタン -->
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        outlined
        absolute
        bottom
        right
        v-bind="attrs"
        v-on="on"
        color="primary"
        class="done-task-btn"
      >
        <v-icon>mdi-check</v-icon>
      </v-btn>
    </template>
    <!-- ダイアログで完了後に選択 -->
    <template v-slot:default="dialog">
      <v-card class="done-task-dialog">
        <v-toolbar
          flat
          dark
          color="primary"
          class="done-task-dialog-header mb-4"
        >
          タスクの完了
        </v-toolbar>
        <v-card-text>
          <div class="done-task-dialog-title">完了度を選んでください</div>
        </v-card-text>
        <div class="done-task-dialog-level-of-completeness px-4 pt-1 pb-4">
          <v-btn
            block
            depressed
            rounded
            large
            retain-focus-on-click
            class="mb-1"
            :color="selectedItem == 1 ? 'primary' : '#f5f5f5'"
            @click="select(1)"
          >満足！</v-btn>
          <v-btn
            block
            depressed
            rounded
            large
            retain-focus-on-click
            class="mb-1"
            :color="selectedItem == 2 ? 'primary' : '#f5f5f5'"
            @click="select(2)"
          >まだまだ</v-btn>
          <v-btn
            block
            depressed
            rounded
            large
            retain-focus-on-click
            :color="selectedItem == 3 ? 'primary' : '#f5f5f5'"
            @click="select(3)"
          >全然…</v-btn>
        </div>
        <v-card-actions class="justify-end">
          <v-btn
            text
            @click="closeDialog"
          >
            キャンセル
          </v-btn>
          <v-btn
            color="primary"
            depressed
            rounded
            :disabled="selectedItem == null"
            @click="save"
          >
            完了
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      selectedItem: null,
      isBtnSelected: false
    }
  },
  methods: {
    select(item) {
      this.selectedItem = item
    },
    save() {
      console.log(this.selectedItem)
      this.closeDialog()
    },
    closeDialog() {
      this.dialog = false
      this.selectedItem = null
    },
  }
}
</script>

<style lang="scss" scoped>
.done-task {
  &-dialog {
    &-header {
      font-size: 18px;
    }
    &-title {
      font-size: 16px;
    }
    &-level-of-completeness {
      .v-btn {
        font-size: 17px;
      }
    }
  }
}
</style>