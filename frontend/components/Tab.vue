<!--
タブの切替ボタン
v-model:    右タブが押されている時:1 / 左タブが押されている時:2
rightName:  右のタブの名前
leftName:   左のタブの名前
width:      タブの幅
-->
<template>
  <div :style="styles" class="tab">
    <div @click="change(1)" class="tab_item" :class="{ active: setTab === 1 }">
      {{ leftName }}
    </div>
    <div @click="change(2)" class="tab_item" :class="{ active: setTab === 2 }">
      {{ rightName }}
    </div>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'tab',
    event: 'change',
  },
  props: {
    tab: Number,

    leftName: {
      type: String,
      default: 'tab1',
    },
    rightName: {
      type: String,
      default: 'tab2',
    },
    width: {
      type: String,
      default: '300px',
    },
  },
  computed: {
    setTab: {
      get() {
        return this.tab
      },
      set(value) {
        return this.$emit('change', value)
      },
    },
    // css変数の追加
    styles() {
      return {
        '--tab-width': this.width,
      }
    },
  },
  methods: {
    // タブの切替
    change(num) {
      this.setTab = num
    },
  },
}
</script>

<style lang="scss" scoped>
.tab {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: var(--tab-width);
  height: 50px;
  margin: 0 auto;
  background-color: #f5f5f5;
  border-radius: 20px;
  cursor: pointer;
  &_item {
    width: 50%;
    height: 100%;
    color: #aaa;
    font-weight: bold;
    border-radius: 20px;
    text-align: center;
    line-height: 50px;
    transition: 0.2s;

    &.active {
      color: #fff;
      background-color: #f8c852;
      transition: 0.2s;
    }
  }
}
</style>
