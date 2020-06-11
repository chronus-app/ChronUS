<template>
  <div id="app">
    <Navbar></Navbar>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar';

export default {
  name: 'app',
  data () {
    return {

    };
  },
  components: {
    Navbar
  }
}
</script>