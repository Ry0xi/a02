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
      </template>
      <v-date-picker
        v-model="editDate"
        scrollable
        locale="jp-ja"
        :min="new Date().toISOString().substr(0, 10)"
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
      this.$emit('update', this.editDate)
      this.dialog = false
    },
  },
}
</script>
