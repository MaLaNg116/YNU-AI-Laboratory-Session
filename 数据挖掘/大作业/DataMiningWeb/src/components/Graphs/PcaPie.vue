<script setup>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import {ref, provide, defineProps, computed, toRaw, onMounted} from "vue";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);
provide(THEME_KEY, "light");

const props = defineProps(["title", "legend", "data", "width", "height", "isRender"]);

const styleObject = ref({
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
    trigger: "item",
    formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
    orient: "vertical",
    left: "right",
    data: legend
  },
  series: [
    {
      name: props.title,
      type: "pie",
      radius: "55%",
      center: ["50%", "60%"],
      data: data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: "rgba(0, 0, 0, 0.5)"
        }
      }
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