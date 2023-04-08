<template>
  <div class="topnav">
    <a class="act" @click="$router.push('/home')" >Home</a>
    <a class="pro" @click="$router.push('/profile')">Profile</a>
    <slot/>
    <a class="inact" @click="logout">Logout</a>
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
  margin-top: -60px;
  margin-left: -8px;

}

.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

.topnav a:hover {
  background-color: #ddd;
  color: black;

}
p{
  font-size: larger;
  font-weight: bold;
  color:brown;
 position: absolute;
  margin-left: 900px;
}
.topnav a.act {
  background-color: #04AA6D;
  color: white;
}
.topnav a.pro {
  background-color: cadetblue;
  color: white;
}
.topnav a.inact {
  background-color: crimson;
  color: white;
 margin-left: 865px;
  position: absolute;
}
</style>