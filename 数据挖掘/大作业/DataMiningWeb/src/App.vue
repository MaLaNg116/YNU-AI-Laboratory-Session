<script setup>
import DataShowing from "@/views/MainPage/DataShowing.vue";
import EffectDisplay from "@/views/MainPage/EffectDisplay.vue";
</script>

<template>
 <div class="my-container">
   <img src="./assets/YNU.jpg" alt="logo" style="width: 100%; height: auto"/>
   <div class="header">
     <h1 style="margin-top: -10px;font-size: 40px;font-weight: bolder">2023年秋季学期-数据挖掘课程</h1>
     <p style="font-size: 25px;font-weight: bolder">实验分析报告</p>
   </div>
   <DataShowing class="Data"/>
   <EffectDisplay class="Effect"/>
 </div>
</template>

<style scoped lang="less">
.my-container{
  padding: 40px 50px;
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-gap: 80px;
  grid-template-rows: 100px 300px auto;
  justify-content: center;
  align-items: center;
  height: 80%;
  border: rgba(222, 222, 222, 0.8) 1px solid;
  border-radius: 20px;
  width: 70%;
  min-width: 1000px;
  z-index: 0;
  transition: height ease 0.5s;
  box-shadow:
      0 1px 1px hsl(0deg 0% 0% / 0.075),
      0 2px 2px hsl(0deg 0% 0% / 0.075),
      0 4px 4px hsl(0deg 0% 0% / 0.075),
      0 8px 8px hsl(0deg 0% 0% / 0.075),
      0 16px 16px hsl(0deg 0% 0% / 0.075);

  .header{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
  }

  .Data {
    grid-column-start: 1;
    grid-column-end: 3;
  }

  .Effect {
    transition: ease 0.5s;
    grid-column-start: 1;
    grid-column-end: 3;
  }
}
</style>
