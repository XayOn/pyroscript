<template>
  <div class="wifi-select">
    <h2 class="text-md-center"><v-icon>wifi</v-icon> Scan for targets</h2>
    <p>Select a target (Currently {{ target.name }} on {{ iface }})</p>
    <v-layout row wrap>
      <v-flex xs6>
        <v-select
          :items="items"
          v-model="select"
          label="Select scan method"
          single-line
          item-text="report"
          item-value="src"
          return-object
          persistent-hint
          v-on:change="selected = select.src"
        ></v-select>
      </v-flex>

      <v-flex xs6>
        <v-btn @click="scan"><v-icon>search</v-icon></v-btn>
        <v-btn @click="update"><v-icon>update</v-icon></v-btn>
      </v-flex>
    </v-layout>

    <div id="airodump" v-if="selected == 'airodump'">Airo</div>
    <div id="wash" v-if="selected == 'wash'">wash</div>

    <v-data-table :headers="target_keys" :items="targets" class="elevation-1">
      <template v-slot:items="props">
        <td>
          <v-icon @click="attack(selected, props.item.interface)">wifi</v-icon>
        </td>
        <td>{{ props.item.essid }}</td>
        <td>{{ props.item.bssid }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import config from "../config.js";

export default {
  name: "ListTargets",
  data() {
    return {
      selected: "airodump",
      select: { name: "Scan with aircrack-ng", src: "airodump" },
      items: [
        { report: "Scan with aircrack-ng", src: "airodump" },
        { report: "Scan with reaver", src: "wash" }
      ],
      target: { name: "None" },
      targets: [],
      target_keys: [
        { text: "Actions", value: "actions" },
        { text: "BSSID", value: "bssid" },
        { text: "ESSID", value: "essid" }
      ],
      sessionId: localStorage.sessionId,
      iface: localStorage.iface
    };
  },
  methods: {
    scan() {
      this.$axios({
        method: "POST",
        url: `${config.api_url}scan/${this.selected}`,
        data: {
          args: [this.iface],
          session_id: this.sessionId,
          kwargs: {}
        }
      });
    },
    update() {
      this.$axios({
        method: "POST",
        url: `${config.api_url}results`,
        data: { session_id: this.sessionId }
      }).then(response => {
        this.targets = Object.values(response.data.scan.results);
      });
    }
  },
  mounted() {
    this.$axios({
      method: "POST",
      url: `${config.api_url}results`,
      data: { session_id: this.sessionId }
    })
      .then(response => {
        this.targets = Object.values(response.data.scan.results);
      })
      .catch(() => {
        this.$axios.get(`${config.api_url}start_session`).then(response => {
          window.localStorage.sessionId = response.data.session_id;
          this.sessionId = response.data.session_id;
        });
      });
  }
};
</script>

<style scoped>
.wifi-select {
  margin-top: 10px;
}
</style>
