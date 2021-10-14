<template>
  <v-dialog max-width="300" v-model="dialog" @click:outside="closeDialog">
    <!-- 完了ボタン -->
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        absolute
        right
        v-bind="attrs"
        v-on="on"
        color="primary"
        style="bottom: 9px"
      >
        <v-icon large>mdi-check-circle-outline</v-icon>
      </v-btn>
    </template>
    <!-- ダイアログで完了後に選択 -->
    <v-card>
      <v-toolbar flat dark color="primary">
        <v-toolbar-title> タスクの完了</v-toolbar-title>
      </v-toolbar>

      <div class="pa-4">完了度を選んでください</div>
      <div class="px-4">
        <v-btn
          block
          depressed
          large
          retain-focus-on-click
          class="mb-2"
          :color="getBtnColor(1)"
          @click="select(1)"
          >満足
        </v-btn>
        <v-btn
          block
          depressed
          large
          retain-focus-on-click
          class="mb-2"
          :color="getBtnColor(2)"
          @click="select(2)"
          >普通
        </v-btn>
        <v-btn
          block
          depressed
          large
          retain-focus-on-click
          class="mb-2"
          :color="getBtnColor(3)"
          @click="select(3)"
          >全然
        </v-btn>
      </div>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog"> キャンセル </v-btn>
        <v-btn
          color="primary"
          depressed
          :disabled="selectedItem == null"
          @click="save"
        >
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      selectedItem: null,
      isBtnSelected: false,
    }
  },
  methods: {
    select(item) {
      this.selectedItem = item
    },
    getBtnColor(item) {
      return this.selectedItem == item ? 'primary' : '#f5f5f5'
    },
    save() {
      console.log(this.selectedItem)
      this.closeDialog()
    },
    closeDialog() {
      this.dialog = false
      this.selectedItem = null
    },
  },
}
</script>
