<script setup>
import {use} from "echarts/core";
import {CanvasRenderer} from "echarts/renderers";
import {PieChart} from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";
import VChart, {THEME_KEY} from "vue-echarts";
import {ref, provide, defineProps, toRaw} from "vue";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

provide(THEME_KEY, "light");

const data = defineProps(["data"]);
const list = Object.values(toRaw(data.data))
const keys = list.map(item => item.name)


const option = ref({
  title: {
    text: "Percentage by Sex",
    left: "center"
  },
  tooltip: {
    trigger: "item",
    formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
    orient: "vertical",
    left: "left",
    data: keys
  },
  series: [
    {
      name: "Percentage by Sex",
      type: "pie",
      radius: "55%",
      center: ["50%", "60%"],
      data: list,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: "rgba(0, 0, 0, 0.5)"
        }
      }
    }
  ]
});
</script>

<template>
  <v-chart class="chart" :option="option"/>
</template>

<style scoped lang="less">
.chart {
  height: 300px;
}
</style>