<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(1); const rollId = ref(1); const out = ref(null)
const ceilingOn = ref(false)
const corners = ref(null)
const segmentLen = ref(null)
const err = ref('')
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (walls.value.length) { wallId.value = walls.value[0].id; corners.value = walls.value[0].corner_count ?? null }
  if (rolls.value.length) rollId.value = rolls.value[0].id
  const s = await getJSON('/api/settings')
  if (s.ceiling_segment_len != null) segmentLen.value = Number(s.ceiling_segment_len)
})
watch(wallId, () => {
  const w = walls.value.find(x => x.id === wallId.value)
  corners.value = w?.corner_count ?? null
})
function numOrNull(v) {
  if (v === '' || v == null) return null
  const n = Number(v)
  return Number.isFinite(n) ? n : null
}
function ceilingParams() {
  const p = { ceiling_on: ceilingOn.value }
  if (ceilingOn.value) {
    const c = numOrNull(corners.value); if (c != null) p.corners = c
    const s = numOrNull(segmentLen.value); if (s != null) p.segment_len = s
  }
  return p
}
async function run(save) {
  err.value = ''
  try {
    const p = ceilingParams()
    if (save) {
      out.value = await postJSON('/api/estimate', { wall_id: wallId.value, roll_id: rollId.value, save: true, ...p })
    } else {
      const qs = new URLSearchParams({ wall_id: wallId.value, roll_id: rollId.value, ...Object.fromEntries(Object.entries(p).map(([k,v]) => [k, String(v)])) })
      out.value = await getJSON(`/api/estimate?${qs}`)
    }
  } catch (e) { err.value = String(e.message || e) }
}
</script>
<template>
  <div class="page"><h1>算卷工作台</h1>
  <select v-model.number="wallId"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <fieldset class="ceiling-box">
    <legend>顶线（腰卷）</legend>
    <label><input type="checkbox" v-model="ceilingOn" /> 开顶线</label>
    <label v-if="ceilingOn">墙角数 <input type="number" min="1" step="1" v-model.number="corners" style="width:5rem" /></label>
    <label v-if="ceilingOn">每角段长(m) <input type="number" min="0" step="0.05" v-model.number="segmentLen" style="width:6rem" /></label>
    <span v-if="ceilingOn" class="muted">腰卷有效长度 {{ out?.ceiling?.usable_len_m ?? 10 }} m/卷</span>
  </fieldset>
  <button @click="run(false)">试算</button><button @click="run(true)">保存</button>
  <p v-if="err" class="warn">保存被拒绝：{{ err }}</p>
  <div v-if="out">
    <p><strong>墙面 {{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m</p>
    <p v-if="ceilingOn && out.ceiling && out.ceiling.rolls != null">
      <strong>顶线 {{ out.ceiling.rolls }} 卷</strong>
      · {{ out.ceiling.corners }} 角 × {{ out.ceiling.segment_len_m }}m
      ＝ {{ out.ceiling.total_len_m }}m
    </p>
    <p v-else-if="ceilingOn && out.ceiling?.error" class="warn">顶线参数非法：{{ out.ceiling.error }}（仅预览，未落库）</p>
    <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" />
  </div>
  </div>
</template>
