<template>
  <div class="topnav">
    <button class="act" @click="$router.push('/home')" >Home</button>
    <button class="pro" @click="$router.push('/profile')">Profile</button>
    <slot/>
    <button class="inact" @click="logout">Logout</button>
  </div>
</template>
<script>
export default {
  methods:{
    logout(){
      localStorage.username="";
      this.$router.push('/')
    }
  },
   data()
{
return{

}
}
}
</script>
<style>
.topnav {
  overflow: hidden;
  background-color: darkgray;
 margin-top:-60px;

}

.topnav button {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
  border-radius: 0px;
}


p{
  font-size: larger;
  font-weight: bold;
  color:brown;
 position: absolute;
  margin-left: 900px;
}
.topnav button.act {
  background-color: #04AA6D;
  color: white;
  margin-left: 0px;
}
.topnav button.pro {
  background-color: cadetblue;
  color: white;
  margin-left: -20px;
}
.topnav button.inact {
  background-color: crimson;
  color: white;
  right:-30px;
  position: fixed;
}

</style>