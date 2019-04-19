<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Pyroscript</span>
        <span class="font-weight-light">Wifi pentesting swiss-knife</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        flat
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
      >
        <span class="mr-2">Latest Release</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <ListWifis/>
    </v-content>
  </v-app>
</template>

<script>
import ListWifis from './components/ListWifis'

export default {
  name: 'App',
  components: {
    ListWifis
  },
  data () {
    return {
      //
    }
  }
}
</script>
