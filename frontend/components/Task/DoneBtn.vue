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
        class="btn-done"
      >
        <v-icon>mdi-check</v-icon>
      </v-btn>
    </template>
    <!-- ダイアログで完了後に選択 -->
    <template v-slot:default="dialog">
      <v-card>
        <v-toolbar
          flat
          dark
          color="primary"
          class="mb-4"
        >タスクの完了</v-toolbar>
        <v-card-text>
          <div class="text-h5">完了度を選んでください</div>
        </v-card-text>
        <div>
          <v-btn
            block
            depressed
            class="mb-1"
            @click="isBtnSelected = true"
          >満足！</v-btn>
          <v-btn
            block
            depressed
            class="mb-1"
            @click="isBtnSelected = true"
          >まだまだ</v-btn>
          <v-btn
            block
            depressed
            @click="isBtnSelected = true"
          >全然…</v-btn>
        </div>
        <v-card-actions class="justify-end">
          <v-btn
            color="primary"
            depressed
            :disabled="!isBtnSelected"
            @click="dialog.value = false"
          >完了</v-btn>
          <v-btn
            text
            @click="dialog.value = false"
          >閉じる</v-btn>
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

<style>

</style>