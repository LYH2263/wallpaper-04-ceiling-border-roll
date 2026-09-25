<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1); const out = ref(null)
const borderEnabled = ref(false); const corners = ref(4); const settings = ref({}); const err = ref('')
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  settings.value = await getJSON('/api/settings')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) rollId.value = rolls.value[0].id
  syncCorners()
})
function syncCorners() {
  const w = walls.value.find(w => w.id === wallId.value)
  if (w) corners.value = w.corners ?? 4
}
watch(wallId, syncCorners)
async function run(save) {
  err.value = ''
  const qs = `wall_id=${wallId.value}&roll_id=${rollId.value}&border_enabled=${borderEnabled.value}&corners=${corners.value}`
  try {
    out.value = save
      ? await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true, border_enabled: borderEnabled.value, corners: corners.value })
      : await getJSON(`/api/estimate?${qs}`)
  } catch (e) { out.value = null; err.value = e.message }
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <label><input type="checkbox" v-model="borderEnabled" /> 顶线</label>
  <template v-if="borderEnabled">
    <label>墙角数 <input type="number" v-model.number="corners" min="1" step="1" style="width:4em" /></label>
    <span>· 每角段长 {{ settings.border_segment_len }} m（设置页可改）</span>
  </template>
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <p v-if="err" class="warn">{{ err }}</p>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m
  <span v-if="out.border?.enabled"> · 顶线 <strong>{{ out.border.rolls }} 卷</strong>（{{ out.border.corners }} 角 × {{ out.border.segment_len_m }}m ÷ {{ out.border.effective_len_m }}m）</span>
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" /></div>
  </div>
</template>
