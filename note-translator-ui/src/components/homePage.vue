<template>
  <navMenu></navMenu>
  <h1>Upload a file !</h1><br>
  <input id="fl" type="file"><br><br>
  <button id="btn">Upload</button>
  <br>
  <br>
  <table>
    <tr>
      <th>FileName</th>
      <th id="header">Actions</th>
    </tr>
    <tr v-for="item in items" >

      <td><a href="www.google.com">{{ item.fileName }}</a></td>
      <td>
        <button id="btnn">View</button>
        <button id="btnn">Share</button>
        <button id="btnn">Delete</button>
      </td>

    </tr>
  </table>
</template>
<script>
import navMenu from './navMenu.vue'
export default {

  components: {
    navMenu: navMenu
  },
  data(){
    return{
      items: [
        { fileName: "heelow.c"},
        { fileName: "dgd.png"},
        { fileName: "error.jpg"}

      ]
    }
  }
}
</script>
<style>
#fl{
  background-color: #dddddd;
  padding: 30px;
}
#btn{

  background-color: steelblue;
  border-radius: 25px;
  width: 100px;
  height: 50px;

}
table {
  margin-left: 700px;
  border-collapse: collapse;
  width: 30%;
  border: 1px solid black;


}
#header{
  text-align: center;
}
th, td {
  padding: 8px;
  text-align: left;
  border: 1px solid black;

  border-bottom: 1px solid #DDD;
  background-color: #D6EEEE;
}
th:nth-child(odd) {
  width:44%;
}
tr:hover {background-color: brown;}
#btnn{

  color: #2c3e50;
  margin-right: 25px;
  font-size: medium;
  font-weight: bold;
  background-color: aquamarine;
  border-radius: 25px;
  width: 80px;
  height: 20px
}
</style>