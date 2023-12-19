<script setup lang="ts">
import {computed, ref} from 'vue'
import type {TabsPaneContext} from 'element-plus'
import NaiveBayes from "@/views/MainPage/ResultsShow/NaiveBayes.vue";
import DecisionTree from "@/views/MainPage/ResultsShow/DecisionTree.vue";
import RandomForest from "@/views/MainPage/ResultsShow/RandomForest.vue";
import SVM from "@/views/MainPage/ResultsShow/SVM.vue";
import MLP from "@/views/MainPage/ResultsShow/MLP.vue";

const activeName = ref('NaiveBayes')


const isNaiveBayesLoaded = ref(false)
const NaiveBayesLoaded = (isLoaded: boolean) => {
  isNaiveBayesLoaded.value = isLoaded
}

const isDecisionTreeLoaded = ref(false)
const DecisionTreeLoaded = (isLoaded: boolean) => {
  isDecisionTreeLoaded.value = isLoaded
}

const isRandomForestLoaded = ref(false)
const RandomForestLoaded = (isLoaded: boolean) => {
  isRandomForestLoaded.value = isLoaded
}

const isSVMLoaded = ref(false)
const SVMLoaded = (isLoaded: boolean) => {
  isSVMLoaded.value = isLoaded
}

const isMLPLoaded = ref(false)
const MLPLoaded = (isLoaded: boolean) => {
  isMLPLoaded.value = isLoaded
}

const handleClick = (tab: TabsPaneContext, event: Event) => {
  // console.log(activeName.value)
  // console.log(isShow.value[activeName.value])
}
</script>

<template>
  <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
    <el-tab-pane v-loading="!isNaiveBayesLoaded" label="NaiveBayes" name="NaiveBayes">
      <NaiveBayes v-show="activeName === 'NaiveBayes'" @loaded="NaiveBayesLoaded" :activating="activeName === 'NaiveBayes'"></NaiveBayes>
    </el-tab-pane>
    <el-tab-pane v-loading="!isDecisionTreeLoaded" label="DecisionTree" name="DecisionTree">
      <DecisionTree v-show="activeName === 'DecisionTree'" @loaded="DecisionTreeLoaded" :activating="activeName === 'DecisionTree'"></DecisionTree>
    </el-tab-pane>
    <el-tab-pane v-loading="!isRandomForestLoaded" label="RandomForest" name="RandomForest">
      <RandomForest v-show="activeName === 'RandomForest'" @loaded="RandomForestLoaded" :activating="activeName === 'RandomForest'"></RandomForest>
    </el-tab-pane>
    <el-tab-pane v-loading="!isSVMLoaded" label="SVM" name="SVM">
      <SVM v-show="activeName === 'SVM'" @loaded="SVMLoaded" :activating="activeName === 'SVM'"></SVM>
    </el-tab-pane>
    <el-tab-pane v-loading="!isMLPLoaded" label="MLP" name="MLP">
      <MLP v-show="activeName === 'MLP'" @loaded="MLPLoaded" :activating="activeName === 'MLP'"></MLP>
    </el-tab-pane>
<!--    <el-tab-pane label="K-Means" name="K-Means">K-Means</el-tab-pane>-->
<!--    <el-tab-pane label="DBSCAN" name="DBSCAN">DBSCAN</el-tab-pane>-->
  </el-tabs>
</template>

<style scoped lang="less">
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>