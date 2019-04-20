<template>
  <div class="wifi-select">
    <h2 class=text-md-center><v-icon>wifi</v-icon> Select a WiFi interface</h2>
    <p> Select a wifi interface (Currently: <span>{{iface}}</span>) </p>

    <v-data-table
      :headers="wifi_keys"
      :items="wifis"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <td>
          <v-icon @click="setupMonitor(props.item.interface)">wifi</v-icon>
          <v-icon @click="select(props.item.interface)">check</v-icon>
        </td>
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
      iface: '',
      wifis: [],
      wifi_keys: [
        { text: 'Actions', value: 'actions'},
        { text: 'Interface', value: 'interface'},
        { text: 'Driver', value: 'driver' },
        { text: 'Chipset', value: 'chipset' },
        { text: 'Physical interface', value: 'phy' },
      ]
    }
  },
  methods: {
    setupMonitor(iface) {
      this.$axios({
        'method': 'POST',
        'url': `${config.api_url}interface/monitor`,
        'data': {interface: iface}
      }).then((response) => {
        this.$axios.get(`${config.api_url}interface/list`).then((response) => {
          this.wifis = response.data
        })
      })
    },
    select(iface) {
      localStorage.iface = iface;
      this.iface = iface;
      this.$router.push('targets')
    }
  },
  mounted () {
    this.iface = window.localStorage.iface
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
