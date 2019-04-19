<template>
  <div class="wifi-select">
    <h2 class=text-md-center>Select a WiFi interface</h2>

    <v-data-table
      :headers="wifi_keys"
      :items="wifis"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <td>{{ props.item.interface }}</td>
        <td>{{ props.item.driver }}</td>
        <td>{{ props.item.chipset }}</td>
        <td>{{ props.item.phy }}</td>
      </template>
    </v-data-table>

  </div>
</template>

<script>
import config from '../config.js'

export default {
  name: 'ListWifis',
  data () {
    return {
      wifis: [],
      wifi_keys: [
        { text: 'Interface', value: 'interface'},
        { text: 'Driver', value: 'driver' },
        { text: 'Chipset', value: 'chipset' },
        { text: 'Physical interface', value: 'phy' },
      ]
    }
  },
  mounted () {
    this.$axios.get(`${config.api_url}interface/list`).then((response) => {
      this.wifis = response.data
    })
  }
}
</script>

<style scoped>
.wifi-select{
margin-top:10px;
}

</style>
