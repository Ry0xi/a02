<!--
日付選択フォーム(１つのみ)
v-model:      日付
-->
<template>
  <v-dialog
    ref="dialog"
    v-model="dialog"
    :return-value.sync="inputDate"
    persistent
    width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="inputDate"
        single-line
        readonly
        outlined
        append-icon="mdi-calendar-month"
        v-bind="attrs"
        v-on="on"
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
        @click="dialog = false"
      >
        Cancel
      </v-btn>
      <v-btn
        text
        color="primary"
        @click="$refs.dialog.save(inputDate)"
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
    date: Date
  },
  data() {
    return {
      dialog: false,
    }
  },
  computed: {
    inputDate: {
      get() {
        return this.date
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  }
}
</script>

<style>

</style>