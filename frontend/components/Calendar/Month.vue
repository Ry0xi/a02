<!--
年月の選択ダイアログ
v-model:  月日 (2021-02)
-->
<template>
  <v-dialog v-model="dialog" max-width="300px">
    <template #activator>
      <slot name="activator" :on="{ click: open }"></slot>
    </template>
    <v-card>
      <v-date-picker
        v-model="editDate"
        type="month"
        full-width
        locale="jp-ja"
        color="primary"
      ></v-date-picker>
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
    prop: 'date',
    event: 'save',
  },
  props: {
    date: {
      type: String,
      default: '2021-01',
    },
  },
  data() {
    return {
      dialog: false,
      editDate: '',
    }
  },
  methods: {
    open() {
      this.editDate = this.date
      this.dialog = true
    },
    close() {
      this.dialog = false
    },
    save() {
      this.dialog = false
      this.$emit('save', this.editDate)
    },
  },
}
</script>
