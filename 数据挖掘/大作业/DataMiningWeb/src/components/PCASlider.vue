<script setup>
import {onMounted, ref, watch} from 'vue'
const emit = defineEmits(['changePCA'])

const value = ref(8)
// 挂载时触发
onMounted(() => {
  emit('changePCA', value.value)
})

const handleChange = (val) => {
  // 值改变时触发
  emit('changePCA', val)
}
</script>

<template>
  <div class="slider-demo-block">
    <span class="demonstration">Dimensions of PCA retention</span>
    <el-slider @change="handleChange" :min="1" :max="8" size="small" v-model="value" :step="1" show-stops />
  </div>
</template>

<style scoped lang="less">
.slider-demo-block {
  padding: 0 20px;
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>