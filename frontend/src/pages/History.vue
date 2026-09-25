<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">{{ r.wall_name }} → {{ r.result?.rolls }} 卷<span v-if="r.result?.border?.enabled"> · 顶线 {{ r.result.border.rolls }} 卷（{{ r.result.border.corners }} 角 × {{ r.result.border.segment_len_m }}m）</span></li></ul></div>
</template>
