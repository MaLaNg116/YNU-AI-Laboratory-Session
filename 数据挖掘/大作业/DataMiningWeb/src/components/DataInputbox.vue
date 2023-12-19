<script lang="ts" setup>
import {computed, reactive, ref} from 'vue'
import type {FormInstance, FormRules} from 'element-plus'
import axios from "axios";
import {ElMessage} from "element-plus";

const props = defineProps(["URL", "pca_dim"])
const URL = computed(() => {
  return props.URL + props.pca_dim
})
const predicted = ref("无")

interface RuleForm {
  length: string
  diameter: string
  height: string
  whole: string
  shucked: string
  viscera: string
  shell: string
  rings: number
}

const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  length: '',
  diameter: '',
  height: '',
  whole: '',
  shucked: '',
  viscera: '',
  shell: '',
  rings: null
})

const exp = "^[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?$"
const list_name = ['length', 'diameter', 'height', 'whole', 'shucked', 'viscera', 'shell', 'rings']
const isSubmit = ref(false)
let submit_data = []

const checkLength = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Length'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 1 || value <= 0) {
        callback(new Error('Length must be between 0 and 1'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkDiameter = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Diameter'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 1 || value <= 0) {
        callback(new Error('Diameter must be between 0 and 1'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkHeight = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Height'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 2 || value <= 0) {
        callback(new Error('Height must be between 0 and 2'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkWhole = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Whole Weight'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 4 || value <= 0) {
        callback(new Error('Whole Weight must be between 0 and 4'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkShucked = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Shucked Weight'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 2 || value <= 0) {
        callback(new Error('Shucked Weight must be between 0 and 2'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkViscera = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Viscera Weight'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 1 || value <= 0) {
        callback(new Error('Viscera Weight must be between 0 and 1'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkShell = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Shell Weight'))
  }
  setTimeout(() => {
    if (!value.match(exp)) {
      callback(new Error('Please input digits'))
    } else {
      if (value > 1.5 || value <= 0) {
        callback(new Error('Shell Weight must be between 0 and 1.5'))
      } else {
        callback()
      }
    }
  }, 100)
}

const checkRings = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input Rings'))
  }
  setTimeout(() => {
    if (!Number.isInteger(value)) {
      callback(new Error('Please input integer'))
    } else {
      if (value < 0 || value > 40) {
        callback(new Error('Rings must be between 0 and 40'))
      } else {
        callback()
      }
    }
  }, 100)
}

const rules = reactive<FormRules<RuleForm>>({
  length: [
    {required: true, validator: checkLength, trigger: 'blur'},
  ],
  diameter: [
    {required: true, validator: checkDiameter, trigger: 'blur'},
  ],
  height: [
    {required: true, validator: checkHeight, trigger: 'blur'},
  ],
  whole: [
    {required: true, validator: checkWhole, trigger: 'blur'},
  ],
  shucked: [
    {required: true, validator: checkShucked, trigger: 'blur'},
  ],
  viscera: [
    {required: true, validator: checkViscera, trigger: 'blur'},
  ],
  shell: [
    {required: true, validator: checkShell, trigger: 'blur'},
  ],
  rings: [
    {required: true, validator: checkRings, trigger: 'blur'},
  ]
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  isSubmit.value = true
  submit_data = []
  await formEl.validate((valid, fields) => {
    if (valid) {
      for (let i = 0; i < list_name.length; i++) {
        submit_data.push(parseFloat(ruleForm[list_name[i]]))
      }
      GetPredict(URL, submit_data)
    } else {
      console.log('error submit!', fields)
      isSubmit.value = false
    }
  })
}
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

async function GetPredict(URL, submit_data) {
  await axios.post(`${URL.value}`, submit_data).then(res => {
    console.log(res.data)
    predicted.value = res.data.data.predict
    isSubmit.value = false
    ElMessage.success('Predicted!')
  }).catch(() => {
    isSubmit.value = false
    ElMessage.error('Oops! 错误发生了, 请重新尝试! ')
  })
}
</script>

<template>
  <div class="input-area">
    <el-form
        ref="ruleFormRef"
        :model="ruleForm"
        :rules="rules"
        label-position="right"
        label-width="120px"
        class="demo-ruleForm"
        :size="formSize"
        status-icon
    >
      <el-form-item label="Length" prop="length">
        <el-input size="default" placeholder="0.33" v-model="ruleForm.length"/>
      </el-form-item>
      <el-form-item label="Diameter" prop="diameter">
        <el-input size="default" placeholder="0.255" v-model="ruleForm.diameter"/>
      </el-form-item>
      <el-form-item label="Height" prop="height">
        <el-input size="default" placeholder="0.08" v-model="ruleForm.height"/>
      </el-form-item>
      <el-form-item label="Whole weight" prop="whole">
        <el-input size="default" placeholder="0.205" v-model="ruleForm.whole"/>
      </el-form-item>
      <el-form-item label="Shucked weight" prop="shucked">
        <el-input size="default" placeholder="0.0895" v-model="ruleForm.shucked"/>
      </el-form-item>
      <el-form-item label="Viscera weight" prop="viscera">
        <el-input size="default" placeholder="0.0395" v-model="ruleForm.viscera"/>
      </el-form-item>
      <el-form-item label="Shell weight" prop="shell">
        <el-input size="default" placeholder="0.055" v-model="ruleForm.shell"/>
      </el-form-item>
      <el-form-item label="Rings" prop="rings">
        <el-input size="default" placeholder="7" v-model.number="ruleForm.rings"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)" :loading="isSubmit">
          <template #loading>
            <div class="custom-loading">
              <svg class="circular" viewBox="-10, -10, 50, 50">
                <path
                    class="path"
                    d="
            M 30 15
            L 28 17
            M 25.61 25.61
            A 15 15, 0, 0, 1, 15 30
            A 15 15, 0, 1, 1, 27.99 7.5
            L 15 15
          "
                    style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
                />
              </svg>
            </div>
          </template>
          Predict
        </el-button>
        <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
      </el-form-item>
    </el-form>
  </div>
  <div class="predict-result">
    <span style="margin-top: -40px">{{ predicted }}</span>
  </div>
</template>

<style scoped lang="less">
.input-area {
  display: unset;
  padding: 10px 10px;
  flex-basis: 0;
  flex-grow: 1;
  width: 200px;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.predict-result{
  width: 50px;
  height: auto;
  display: flex;
  flex-basis: 0;
  flex-grow: 1;
  justify-content: center;
  align-items: center;
  font-size: 300px;
  font-weight: bold;
  color: rgba(64, 158, 255, 0.8);
  border: 1px solid #ccc;
  border-radius: 8px;
}

.el-button .custom-loading .circular {
  margin-right: 6px;
  width: 18px;
  height: 18px;
  animation: loading-rotate 2s linear infinite;
}

.el-button .custom-loading .circular .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-button-text-color);
  stroke-linecap: round;
}
</style>