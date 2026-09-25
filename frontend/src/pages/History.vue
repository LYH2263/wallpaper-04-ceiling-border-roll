<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page"><h1>记录</h1>
  <table>
    <tr><th>墙面</th><th>墙面卷数</th><th>顶线卷数</th><th>顶线参数（写入时）</th></tr>
    <tr v-for="r in items" :key="r.id">
      <td>{{ r.wall_name }}</td>
      <td>{{ r.result?.rolls }} 卷</td>
      <td>{{ r.result?.ceiling?.on ? `${r.result.ceiling.rolls} 卷` : '—' }}</td>
      <td v-if="r.result?.ceiling?.on">{{ r.result.ceiling.corners }} 角 × {{ r.result.ceiling.segment_len_m }}m</td>
      <td v-else class="muted">{{ r.result?.ceiling ? '关' : '旧单无顶线列' }}</td>
    </tr>
  </table>
  <p class="muted">顶线列钉住下单时的角数/段长/卷数，事后改默认段长不重算旧单。</p></div>
</template>
