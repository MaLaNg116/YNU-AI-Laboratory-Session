<script setup>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { HeatmapChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  VisualMapComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import {ref, provide, defineProps, computed, toRaw, reactive, onMounted} from "vue";

use([
  VisualMapComponent,
  CanvasRenderer,
  HeatmapChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);
provide(THEME_KEY, "light");

const props = defineProps(["title", "legend", "data", "width", "height", "isRender"]);

const styleObject = reactive({
  width: props.width,
  height: props.height
})

const legend = computed(() => {
  return Object.values(toRaw(props.legend))
})

const data = computed(() => {
  return Object.values(toRaw(props.data)).map(function (item) {
    return [item[1], item[0], item[2] || '-'];
  })
})

const x_aixs = computed(() => {
  return legend.value[1]
})

const y_aixs = computed(() => {
  return legend.value[0]
})

const option = ref({
  title: {
    text: props.title,
    left: "center"
  },
  tooltip: {
    position: 'top'
  },
  grid: {
    height: '50%',
    top: '10%'
  },
  xAxis: {
    type: 'category',
    data: x_aixs,
    splitArea: {
      show: true
    }
  },
  yAxis: {
    type: 'category',
    data: y_aixs,
    splitArea: {
      show: true
    }
  },
  visualMap: {
    min: 0,
    max: 300,
    calculable: true,
    orient: 'horizontal',
    left: 'center',
    bottom: '5%'
  },
  series: [
    {
      name: props.title,
      type: 'heatmap',
      data: data,
      label: {
        show: true
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
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

<style scoped lang="less">
.chart {
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}
</style>