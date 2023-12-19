<script setup>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
    GridComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import {ref, provide, defineProps, computed, toRaw, reactive, onMounted} from "vue";

use([
  GridComponent,
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);
provide(THEME_KEY, "light");

const props = defineProps(["title", "legend", "data", "name", "width", "height", "isRender"]);

const styleObject = reactive({
  width: props.width,
  height: props.height
})

const legend = computed(() => {
  return Object.values(toRaw(props.legend))
})
const data = computed(() => {
  return Object.values(toRaw(props.data))
})

const option = ref({
  title: {
    text: props.title,
    left: "center"
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: legend,
      axisTick: {
        alignWithLabel: true
      }
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: props.name,
      type: 'bar',
      barWidth: '60%',
      data: data
    }
  ]
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
  <v-chart v-if="isShow" :style="styleObject" class="chart" :option="option" />
</template>

<style scoped>
.chart {
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}
</style>