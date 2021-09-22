<!--
ボタン
@click: イベントの発火
-->
<template>
  <div @click="$emit('click', $event)" class="btn">
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.btn {
  width: 100%;
  height: 50px;
  line-height: 50px;
  text-align: center;
  font-weight: bold;
  border-radius: 20px;
  color: #fff;
  background-color: #f8c852;
  transition: 0.1s;
  cursor: pointer;
  &:active {
    opacity: 0.5;
  }
}
</style>
