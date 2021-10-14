<!--
日付選択フォーム(１つのみ)
v-model:      日付
placeholder:  入力フォームに表示するプレイスホルダー
-->
<template>
  <div>
    <v-dialog v-model="dialog" persistent width="300px">
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          v-model="date"
          single-line
          readonly
          outlined
          append-icon="mdi-calendar-month"
          v-bind="attrs"
          v-on="on"
          @click="edit"
          :placeholder="placeholder"
          class="mt-1"
        ></v-text-field>
        <v-snackbar v-model="snackbar"> 表示日は過去にできません </v-snackbar>
      </template>
      <v-date-picker
        v-model="editDate"
        scrollable
        locale="jp-ja"
        :day-format="(date) => new Date(date).getDate()"
        color="primary"
      >
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="close"> キャンセル </v-btn>
        <v-btn depressed color="primary" @click="save"> OK </v-btn>
      </v-date-picker>
    </v-dialog>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'date',
    event: 'update',
  },
  props: {
    date: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      dialog: false,
      editDate: null,
      snackbar: false,
    }
  },
  computed: {
    inputDate: {
      get() {
        return this.date
      },
    },
  },
  methods: {
    edit() {
      this.editDate = this.date
    },
    close() {
      this.dialog = false
    },
    save() {
      const now = new Date()
      now.setDate(now.getDate() - 1)
      const dt = new Date(this.editDate)
      if (dt < now) {
        this.dialog = false
        this.snackbar = true
      } else {
        this.$emit('update', this.editDate)
        this.dialog = false
      }
    },
  },
}
</script>
