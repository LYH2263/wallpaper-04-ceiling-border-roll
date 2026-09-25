<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({})
const segmentLen = ref(null)
const msg = ref('')
onMounted(load)
async function load() {
  s.value = await getJSON('/api/settings')
  segmentLen.value = s.value.ceiling_segment_len != null ? Number(s.value.ceiling_segment_len) : null
}
async function saveSegment() {
  msg.value = ''
  try {
    s.value = await postJSON('/api/settings/ceiling-segment', { segment_len: Number(segmentLen.value) })
    segmentLen.value = s.value.ceiling_segment_len != null ? Number(s.value.ceiling_segment_len) : segmentLen.value
    msg.value = '已保存默认段长（仅影响之后的新单，旧单不重算）'
  } catch (e) { msg.value = String(e.message || e) }
}
</script>
<template><div class="page"><h1>设置</h1>
  <p>顶线默认每角段长(m)
    <input type="number" min="0" step="0.05" v-model.number="segmentLen" style="width:6rem" />
    <button @click="saveSegment">存默认段长</button></p>
  <p :class="msg.startsWith('已') ? 'muted' : 'warn'">{{ msg }}</p>
  <details><summary>原始设置</summary><pre>{{ s }}</pre></details>
</div></template>
