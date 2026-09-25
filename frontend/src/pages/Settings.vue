<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({}); const seg = ref(0.5); const msg = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  seg.value = parseFloat(s.value.border_segment_len ?? '0.5')
})
async function save() {
  msg.value = ''
  try {
    s.value = await postJSON('/api/settings', { key: 'border_segment_len', value: String(seg.value) })
    msg.value = '已保存'
  } catch (e) { msg.value = e.message }
}
</script>
<template>
  <div class="page"><h1>设置</h1>
  <p>顶线默认每角段长（m）<input type="number" v-model.number="seg" min="0.01" step="0.1" style="width:6em" />
  <button @click="save">保存</button> {{ msg }}</p>
  <pre>{{ s }}</pre></div>
</template>
