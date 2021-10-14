<!--
日付選択フォーム(１つのみ)
v-model:      日付
placeholder:  入力フォームに表示するプレイスホルダー
-->
<template>
  <v-dialog
    ref="dialog"
    v-model="dialog"
    persistent
    width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        :value="newDate ? newDate : date"
        single-line
        readonly
        outlined
        append-icon="mdi-calendar-month"
        v-bind="attrs"
        v-on="on"
        :placeholder="placeholder"
        class="mt-1"
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="inputDate"
      scrollable
      locale="jp-ja"
      :day-format="date => new Date(date).getDate()"
      color="primary"
    >
      <v-spacer></v-spacer>
      <v-btn
        text
        color="primary"
        @click="closeDialog"
      >
        Cancel
      </v-btn>
      <v-btn
        text
        color="primary"
        @click="sendNewDate(), closeDialog()"
      >
        OK
      </v-btn>
    </v-date-picker>
  </v-dialog>
</template>

<script>
export default {
  model: {
    prop: 'date',
    event: 'input'
  },
  props: {
    date: String,
    placeholder: String
  },
  data() {
    return {
      dialog: false,
      newDate: null
    }
  },
  computed: {
    inputDate: {
      get() {
        return this.newDate ? this.newDate : this.date
      },
      set(value) {
        this.newDate = value
      }
    }
  },
  methods: {
    closeDialog: function() {
      this.refreshInputDate()
      this.dialog = false
    },
    refreshInputDate: function() {
      this.newDate = null
    },
    sendNewDate: function() {
      if (this.newDate && this.newDate != this.date) {
        this.$emit('input', this.newDate)
      }
    }
  }
}
</script>

<style>

</style>