<template>
  <navMenu></navMenu>
  <h1>Share a file !</h1>
  <br>
  <button id="btn" @click="() => TogglePopup('buttonTrigger')">New</button>
  <Popup
      v-if="popupTriggers.buttonTrigger"
      :TogglePopup="() => TogglePopup('buttonTrigger')">

  </Popup>
  <br>
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
        <button id="btnn" @click="view(item.fileName)">View</button>
        <button id="btnn">Share</button>
        <button id="btnn">Delete</button>
      </td>

    </tr>
  </table>
</template>
<script>
import navMenu from './navMenu.vue'
import Popup from './popUpNew.vue'
import axios from "axios";
import { ref } from 'vue';
export default {
  mounted() {
    this.onLoad();
  },
  setup () {
    const popupTriggers = ref({
      buttonTrigger: false,

    });
    const TogglePopup = (trigger) => {
      popupTriggers.value[trigger] = !popupTriggers.value[trigger]
    }
    return {
      Popup,
      popupTriggers,
      TogglePopup
    }
  },
  components: {
    navMenu: navMenu,
    Popup: Popup
  },
  data(){
    return{
      items: [
        { fileName: "sample.txt"},
        { fileName: "dgd.png"},
        { fileName: "error.jpg"}

      ]
    }
  },
  methods: {
   async view(obj) {
     try{
       const response = await axios
           .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/view", {
             username: localStorage.username,
             file: obj
           });
       if(response.data.message != null){
         this.$router.push('/home');
       }
     }catch (err) {
       console.log(err);
     }

    },
    async  onLoad() {
      try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/send", {
              username: localStorage.username
            });
        if(response.data.message != null){
          this.$router.push('/home');
        }
      }catch (err) {
        console.log(err);
      }
      try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/list", {
              username: localStorage.username
            });
        if(response.data.message != null){
          this.$router.push('/home');
        }
      }catch (err) {
        console.log(err);
      }
      },
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