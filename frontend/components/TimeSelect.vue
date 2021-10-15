<!--
時間選択ダイアログ
v-model: 時間
-->
<template>
  <v-dialog v-model="dialog" max-width="300px">
    <template #activator="on">
      <slot name="activator" :on="{ click: open }"></slot>
    </template>
    <v-card>
      <v-time-picker v-model="editTime" format="24hr" full-width>
      </v-time-picker>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="close">キャンセル</v-btn>
        <v-btn depressed class="primary" @click="save">OK</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  model: {
    prop: 'time',
    event: 'save',
  },
  props: {
    time: {
      type: String,
      default: '08:00',
    },
  },
  data() {
    return {
      dialog: false,
      editTime: '',
    }
  },
  methods: {
    open() {
      this.editTime = this.time
      this.dialog = true
    },
    close() {
      this.dialog = false
    },
    save() {
      this.dialog = false
      this.$emit('save', this.editTime)
    },
  },
}
</script>
