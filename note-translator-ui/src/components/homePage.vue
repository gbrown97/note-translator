<template>
  <navMenu>
    <p>welcome {{user}}</p>
  </navMenu>
  <h1>Share a file !</h1>
  <br>
  <button id="btn" @click="() => TogglePopup('buttonTrigger')">New</button>
  <Popup
      v-if="popupTriggers.buttonTrigger"
      :TogglePopup="() => TogglePopup('buttonTrigger')">

  </Popup>
  <PopView v-if=open>
    <h3>{{cont}}</h3>
    <button class="popup-close"  @click="close()">
      Cancel
    </button>
  </PopView>

  <PopView v-if=trans>
    <h3 style="color: red">{{errMsg}}</h3>
    <upload id="updl" v-if="upld">

    </upload><br><br>
    <form @submit.prevent="transContent">
      <select class="form-control" v-model="languagesel">
        <option  value="">Select preferred language</option>
        <option :value="language.name"  v-for="(language) in languagesList" :key="language.name">{{language.name}}</option>
      </select>&nbsp
      <button>Translate</button><br><br>
    </form>
    <button class="popup-close"  @click="tClose()">
      Cancel
    </button>
  </PopView>

  <PopView v-if=share>
    <h3 style="color: red">{{errMsg}}</h3>
    <upload id="updl" v-if="upld">

    </upload><br><br>
    <form @submit.prevent="send">
    <select class="form-control" v-model="recUsername">
      <option  value="">Send to</option>
      <option :value="user.username"  v-for="(user) in usersList" :key="user.username">{{user.name}}</option>
    </select>&nbsp
    <button>Send</button><br><br>
    <button class="popup-close"  @click="cloShare()">
      Cancel
    </button>
      </form>
  </PopView>
  <br>
  <br>
  <br>
  <table>
    <tr>
      <th>FileName</th>
      <th id="header">Actions</th>
    </tr>
    <tr v-for="item in items" >

      <td><a href="">{{ item }}</a></td>
      <td>
        <button id="btnn" @click="viewContent(item)">View</button>
        <button id="btnn" @click="transFile(item)">Translate</button>
        <button id="btnn" @click="shareFile(item)">Share</button>
        <button id="btnn" @click="deleteFile(item)">Delete</button>
      </td>

    </tr>
  </table>
</template>
<script>
import navMenu from './navMenu.vue'
import Popup from './popUpNew.vue'
import axios from "axios";
import { ref } from 'vue';
import popView from './popView.vue'
import upload from './uploading.vue'

let languages = require('./languages.json');
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
      TogglePopup,

    }
  },
  components: {
    navMenu: navMenu,
    Popup: Popup,
    PopView: popView,
    upload
  },
  data(){
    return{
      languagesList: languages,
      languagesel:'',
      trans:false,
      upld:false,
      recUsername:'',
      share:false,
      open:false,
      cont:'',
      items:null,
      usersList:null,
      user:'',
      shareFileName:'',
      transFileName:'',
      errMsg:'',
      userLan:''
    }
  },
  methods: {
    close(){
      this.open=!this.open
    },
    cloShare(){
      this.share=!this.share
    },
    tClose(){
      this.trans=!this.trans
    },
   async viewContent(fileName) {
      this.cont=''
     this.open=true
     try{
       const response = await axios
           .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/view", {
             username: localStorage.username,
             recName:this.recUsername,
             file: fileName
           });
       if(response.data != null){
         this.cont=response.data;
         this.$router.push('/home');
       }
     }catch (err) {
       console.log(err);
     }

    },
    transFile(fileName) {
      this.trans=true
       this.transFileName=fileName
    },
    async transContent() {
      this.upld = true;
      this.errMsg="";
      try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/translate", {
              username: localStorage.username,
              recName:localStorage.username,
              file: this.transFileName,
              destLang: this.languagesel,
              srcLang: this.userLan
            });
        if(response.data != null){

          this.$router.go(0);
        }
      }catch (err) {
        this.upld = false;
        this.errMsg="Error translating the file !!"
        console.log(err);
      }

    },
    async shareFile(fileName) {

      try {
        this.shareFileName=fileName
        const res = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/users", {});
        if (res.data != null) {
          this.usersList = res.data;
        }
        this.share = true
      }
      catch(err){
        console.log(err)
      }
    },
    async send(){
      this.upld = true;
      this.errMsg="";
      try{
      const response = await axios
          .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/share", {
            username: localStorage.username,
            recName:this.recUsername,
            file: this.shareFileName
          });
      if(response.data.message == "Notes shared successful"){

        this.$router.go(0);
      }
    }catch (err) {
        this.upld = false;
        this.errMsg="Error sharing the file !!"
      console.log(err);
    }

  },
    async deleteFile(fileName) {
      try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/delete", {
              username: localStorage.username,
              file: fileName
            });
        if(response.data.message == "Notes deleted successful"){
          this.$router.go(0);
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
        if(response.data != null){
          this.user=response.data.userDetails[1]+" "+response.data.userDetails[2];
          this.userLan=response.data.userDetails[3];
        }
      }catch (err) {
        console.log(err);
      }
      try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/list", {
              username: localStorage.username
            });

        if(response.data != null){
          this.items=response.data.files
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
  width: 39%;
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
select {
  color: #2c3e50;
  font-size: medium;
  border-radius: 25px;
  width: 300px;
  height: 40px;
  font-weight: bold;

}

</style>