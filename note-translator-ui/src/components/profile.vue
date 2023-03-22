<template>
  <navMenu></navMenu>
  <h1>Change Password</h1>
  <div>
    <form>
      <input type="password" placeholder="Enter Current Password ">
      <br>
      <br>
      <input type="password" placeholder="Enter New Password ">
      <br>
      <br>
      <input type="password" placeholder="Re-enter New Password ">
      <br>
      <br>
      <button>Submit</button>
    </form>
  </div>
</template>
<style>
h1{
  margin-top: 100px;
}
button{

  color: #2c3e50;
  margin-right: 25px;
  font-size: x-large;
  font-weight: bold;
  background-color: aquamarine;
  border-radius: 25px;
  width: 120px;
  height: 50px
}
input{
  color: #2c3e50;
  font-size: x-large;
  padding: 15px;
  border-radius: 25px;
  width: 300px;
  height: 20px;
}
</style>
<script>
import navMenu from './navMenu.vue'

export default {

  components: {
    navMenu: navMenu
  }
}
</script>