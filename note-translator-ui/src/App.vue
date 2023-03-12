<template>
  <img alt="Vue logo" src="../public/noteTrans.jpg">
  <noteTransl msg="Welcome to Note Translation"/>
</template>

<script>
import noteTransl from './components/noteTransl.vue'

export default {
  name: 'App',
  components: {
    noteTransl
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#Helloworld {
  text-align: right;
}
</style>
