<script setup>
import PCASlider from "@/components/PCASlider.vue";
import PieChart from "@/components/Graphs/PcaPie.vue";
import axios from "axios";
import {computed, onMounted, ref, toRaw, watch} from "vue";
import {ElMessage} from "element-plus";
import HistogramChart from "@/components/Graphs/AccHistogram.vue";
import HeatMap from "@/components/Graphs/ConfusionMatrix.vue";
import ROCChart from "@/components/Graphs/ROCChart.vue";
import DataInputbox from "@/components/DataInputbox.vue";

const emit = defineEmits(['loaded'])
const props = defineProps(['activating'])

const isRender = computed(() => {
  return props.activating
})

const URL = "http://localhost:5000";
const data = ref(null)

const newKeys = ref(['Length', 'Diameter', 'Height', 'Whole', 'Shucked', 'Viscera', 'Shell', 'Rings'])
const pca_Data = ref([])
const pca_keys = ref([])
const pca_dim = ref(8)

const time = ref([])
const time_legend = ref(['Training Time', 'Test Time'])

const confusion_matrix = ref([])
const confusion_matrix_legend = ref([])

const acc = ref({})
const acc_legend = ref(['Valid ACC', 'Test ACC'])

const roc_data = ref([])
const roc_legend = ref([])
const roc_auc = ref([])

const params = ref({})
const best_param = ref([])

async function GetDecisionTree(dim) {
  emit('loaded', false)
  await axios.get(`${URL}/GetDecisionTree/${dim}`).then(res => {
    // 终止加载动画
    emit('loaded', true)

    // 清空数据
    pca_Data.value = []
    pca_keys.value = []
    time.value = []

    // 处理PCA数据
    // 切割标签
    pca_keys.value = newKeys.value.slice(0, dim)
    // 重新赋值
    data.value = res.data.data
    console.log(data.value)
    pca_keys.value.forEach((key, index) => {
      pca_Data.value.push({name: key, value: data.value["explained_variance_ratios"][index]});
    });

    // 处理时间数据
    time.value.push(data.value["training_time"])
    time.value.push(data.value["test_time"])

    // 处理混淆矩阵数据
    confusion_matrix.value = data.value["conf_matrix"]
    confusion_matrix_legend.value = data.value["conf_matrix_label"]

    // 处理准确率数据
    acc.value = {
      "valid_acc": data.value["best_score"] / 100,
      "test_acc": data.value["accuracy"]
    }

    // 处理ROC数据
    roc_data.value = data.value["roc_data"]
    roc_auc.value = data.value["roc_auc"]
    roc_legend.value = data.value["label"]

    // 处理参数数据
    params.value = data.value["params"]
    best_param.value = data.value["best_params"]
  }).catch((err) => {
    console.log(err)
    emit('loaded', true)
    ElMessage.error('Oops! 错误发生了, 请重新尝试! ')
  })
}

const PCA_dim = (dim) => {
  GetDecisionTree(dim)
  pca_dim.value = dim
  return dim
}
</script>

<template>
  <div>
    <PCASlider @changePCA="PCA_dim"></PCASlider>
    <div class="predict-area">
      <DataInputbox
          :URL="`${URL}/GetDecisionTree/`"
          :pca_dim="pca_dim"
      ></DataInputbox>
    </div>
    <div class="text-area">
      <span class="content">&emsp;&emsp;对决策树分类器的参数{{
          Object.keys(best_param).toString()
        }}进行了交叉验证，该参数用于控制树的深度，从而影响模型的复杂度和泛化能力。验证范围为{{ params }}。</span>
      <br/>
      <span class="content">&emsp;&emsp;最优参数组合为：{{ best_param }}</span>
    </div>
    <div class="graph-container">
      <PieChart
          v-if="isRender"
          title="PCA Contribution Rate"
          :data="pca_Data"
          :legend="pca_keys"
          :isRender="isRender"
          width="400px"
          height="300px"
      ></PieChart>
      <HistogramChart
          v-if="isRender"
          title="Time Consuming"
          :data="time"
          :legend="time_legend"
          :isRender="isRender"
          name="Time"
          width="400px"
          height="300px"
      ></HistogramChart>
      <HeatMap
          v-if="isRender"
          title="Confusion Matrix"
          :data="confusion_matrix"
          :legend="confusion_matrix_legend"
          :isRender="isRender"
          width="400px"
          height="300px"
      ></HeatMap>
      <HistogramChart
          v-if="isRender"
          title="Accuracy"
          :data="acc"
          :legend="acc_legend"
          :isRender="isRender"
          name="Accuracy"
          width="400px"
          height="300px"
      ></HistogramChart>
      <ROCChart
          v-if="isRender"
          title="ROC Curve"
          :legend="roc_legend"
          :data="roc_data"
          :auc="roc_auc"
          :isRender="isRender"
          width="900px"
          height="500px"
      ></ROCChart>
    </div>
  </div>
</template>

<style scoped lang="less">
.predict-area {
  width: 100%;
  height: auto;
  padding: 20px 20px;
  display: flex;
  gap: 40px;
  flex-direction: row;
  justify-content: space-between;
  align-items: stretch;
  margin-bottom: 40px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.text-area {
  padding: 15px;
  width: 100%;
  height: auto;
  margin-bottom: 40px;

  .content {
    color: rgba(64, 158, 255, 0.8);
    font-family: "JetBrainsMono NF", sans-serif;
    font-size: 15px;
    font-weight: bold;
    line-height: 1.5;
    text-align: justify;
  }
}

.graph-container {
  width: 100%;
  padding: 20px 20px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>