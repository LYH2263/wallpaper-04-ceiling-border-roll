<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const props = defineProps({ id: String })
const wall = ref(null)
const corners = ref(null)
const msg = ref('')
onMounted(async () => {
  wall.value = await getJSON(`/api/walls/${props.id}`)
  corners.value = wall.value.corner_count ?? null
})
async function saveCorners() {
  msg.value = ''
  try {
    wall.value = await postJSON(`/api/walls/${props.id}/corners`, { corners: Number(corners.value) })
    msg.value = '已保存默认角数'
  } catch (e) { msg.value = String(e.message || e) }
}
</script>
<template>
  <div class="page" v-if="wall"><h1>{{ wall.name }}</h1>
  <p v-if="wall.data_quality==='dirty'" class="warn">{{ wall.note }}</p>
  <p>周长 {{ wall.perimeter }} m，墙高 {{ wall.height }} m</p>
  <p>默认墙角数 <input type="number" min="1" step="1" v-model.number="corners" style="width:5rem" />
    <button @click="saveCorners">存默认角数</button></p>
  <p v-if="msg" :class="msg.startsWith('已') ? 'muted' : 'warn'">{{ msg }}</p></div>
</template>
