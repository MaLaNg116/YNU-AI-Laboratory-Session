<script setup>
import axios from "axios";
import {ref} from 'vue'
import {ElMessage} from 'element-plus'
import DataPie from "@/components/DataPie.vue";

axios.defaults.timeout = 300000

const data = ref(null)
const isLoading = ref(true)
const countSex = ref({M: 0, I: 0, F: 0});

async function getData() {
  await axios.get('http://localhost:5000/GetData').then(res => {
    // 返回数据
    let tmp = res.data.data

    // 保留最后100条数据
    data.value = tmp.slice(-100).sort((a, b) => b.id - a.id)
    isLoading.value = false

    // 计算性别比例
    let CountTmp = tmp.reduce((acc, curr) => {
      acc[curr.sex]++;
      return acc;
    }, countSex.value);
    countSex.value = Object.entries(CountTmp).map(([name, value]) => ({name, value: String(value)}))

    // 在控制台输出结果
    console.log(countSex.value);
  }).catch(err => {
    console.log(err)
    isLoading.value = false
    ElMessage.error('数据加载失败！')
  });
}

getData()
</script>

<template>
  <div class="data-showing">
    <div class="data-table">
      <el-table v-loading="isLoading" :data="data" style="width: 550px" height="255px">
        <el-table-column fixed prop="id" label="ID" width="60"/>
        <el-table-column fixed prop="sex" label="Sex" width="50"/>
        <el-table-column prop="length" label="Length" width="70"/>
        <el-table-column prop="diameter" label="Diameter" width="85"/>
        <el-table-column prop="height" label="Height" width="70"/>
        <el-table-column prop="whole" label="Whole" width="70"/>
        <el-table-column prop="shucked" label="Shucked" width="80"/>
        <el-table-column prop="viscera" label="Viscera" width="70"/>
        <el-table-column prop="shell" label="Shell" width="60"/>
        <el-table-column prop="rings" label="Rings" width="70"/>
      </el-table>
    </div>
    <div v-loading="isLoading" class="data-graph">
      <DataPie v-if="!isLoading" :data="countSex" ></DataPie>
    </div>
  </div>
</template>

<style scoped lang="less">
.data-showing {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 40px;
  width: 100%;
  height: 100%;
  justify-content: space-between;

  .data-table {
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    width: 100%;
    height: 100%;
    border: rgba(220, 223, 230) 1px solid;
    border-radius: 4px;
    box-shadow: 0 1px 2px hsl(0deg 0% 0% / 0.075);
  }

  .data-graph {
    display: flex;
    padding: 20px;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    border: rgba(220, 223, 230) 1px solid;
    border-radius: 10px;
  }
}
</style>