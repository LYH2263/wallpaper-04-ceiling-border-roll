<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const props = defineProps({ id: String })
const wall = ref(null); const corners = ref(0); const msg = ref('')
onMounted(async () => {
  wall.value = await getJSON(`/api/walls/${props.id}`)
  corners.value = wall.value.corners ?? 0
})
async function save() {
  msg.value = ''
  try {
    wall.value = await postJSON(`/api/walls/${props.id}`, { corners: corners.value })
    msg.value = '已保存'
  } catch (e) { msg.value = e.message }
}
</script>
<template>
  <div class="page" v-if="wall"><h1>{{ wall.name }}</h1>
  <p v-if="wall.data_quality==='dirty'" class="warn">{{ wall.note }}</p>
  <p>周长 {{ wall.perimeter }} m，墙高 {{ wall.height }} m</p>
  <p>默认墙角数 <input type="number" v-model.number="corners" min="0" step="1" style="width:4em" />
  <button @click="save">保存</button> {{ msg }}</p></div>
</template>
