<template>
  <v-dialog
    max-width="600"
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
        @click="isBtnSelected = false"
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
            @click="isBtnSelected = true"
          >満足！</v-btn>
          <v-btn
            block
            depressed
            rounded
            large
            retain-focus-on-click
            class="mb-1"
            @click="isBtnSelected = true"
          >まだまだ</v-btn>
          <v-btn
            block
            depressed
            rounded
            large
            retain-focus-on-click
            @click="isBtnSelected = true"
          >全然…</v-btn>
        </div>
        <v-card-actions class="justify-end">
          <v-btn
            text
            @click="dialog.value = false"
          >
            キャンセル
          </v-btn>
          <v-btn
            color="primary"
            depressed
            rounded
            :disabled="!isBtnSelected"
            @click="dialog.value = false"
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
      isBtnSelected: false
    }
  }
}
</script>

<style lang="scss" scoped>
.done-task {
  &-btn {
    .v-btn {
      &:active,
      &:focus {
        &::before {
          background-color: transparent;
        }
      }
    }
  }

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

        &:active,
        &:focus {
          background-color: transparent;

          &::before {
            opacity: 0.4;
          }
        }

        &::before {
          background-color: var(--v-primary-base, currentColor);
        }
      }
    }
  }
}
</style>