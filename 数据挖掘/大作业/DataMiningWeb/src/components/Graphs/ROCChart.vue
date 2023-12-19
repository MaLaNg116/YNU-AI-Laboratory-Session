<script setup>
import {use} from "echarts/core";
import {CanvasRenderer} from "echarts/renderers";
import {LineChart} from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent
} from "echarts/components";
import VChart, {THEME_KEY} from "vue-echarts";
import {ref, provide, defineProps, computed, toRaw, onMounted, watch} from "vue";

use([
  ToolboxComponent,
  GridComponent,
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);
provide(THEME_KEY, "light");

const props = defineProps(["title", "legend", "data", "auc", "width", "height", "isRender"]);

const styleObject = ref({
  width: props.width,
  height: props.height
})

const legend = computed(() => {
  let class_name = Object.values(toRaw(props.legend))
  let auc = Object.values(toRaw(props.auc))
  for (let i = 0; i < class_name.length; i++) {
    class_name[i] = "Class " + class_name[i] + " (AUC: " + parseFloat(auc[i].toFixed(2)) + ")"
  }
  return class_name
})
const data = computed(() => {
  return Object.values(toRaw(props.data))
})

const option = computed(() => {
  return {
    title: {
      text: props.title,
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: legend.value,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'value',
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: legend.value[0],
        type: 'line',
        symbolSize:0,
        smooth: 0.5,
        data: data.value[0]
      },
      {
        name: legend.value[1],
        type: 'line',
        symbolSize:0,
        smooth: 0.5,
        data: data.value[1]
      },
      {
        name: legend.value[2],
        type: 'line',
        symbolSize:0,
        smooth: 0.5,
        data: data.value[2]
      },
    ]
  }
})

const isRender = computed(() => {
  return props.isRender
})
const isShow = ref(false)

onMounted(() => {
  isRender.value ? isShow.value = true : isShow.value = false
})
</script>

<template>
  <v-chart v-if="isShow" :style="styleObject" class="chart" :option="option"/>
</template>

<style scoped lang="less">
.chart {
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}
</style>