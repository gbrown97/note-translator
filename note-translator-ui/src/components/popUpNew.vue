<template>

  <div class="popup">
    <div class="popup-inner">
      <h1 style="color:red;">{{sts}}</h1>
      <upload id="updl" v-if="upld">

      </upload><br><br>
      <form @submit.prevent="onUpload">

      <input type="file" accept="image/png, image/gif, image/jpeg, .txt, .pdf" @change="uploadFile" ref="file">
        <select class="form-control" v-model="recUsername">
          <option  value="">Send to</option>
          <option :value="user.username"  v-for="(user) in usersList" :key="user.username">{{user.name}}</option>
        </select>&nbsp
        <button>Upload</button><br><br>
      <button class="popup-close" @click="TogglePopup()">
        Cancel
      </button>
      </form>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import upload from './uploading.vue'
export default {
  mounted() {
    this.onLoad();
  },
  components:{
    upload
  },
  props: ['TogglePopup'],
  data(){
    return {

      username: "",
      language: "",
      file:null,
      upld:false,
      sts:'',
      usersList:null,
      recUsername:''

    };
  },
  methods:{
    async onLoad(){
    try{
      const response = await axios
          .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/users", {

          });

      if(response.data != null){
  this.usersList=response.data;

}
}catch (err) {
  console.log(err);
}
},
uploadFile() {

      this.file = this.$refs.file.files[0];
    },
    async  onUpload() {
      if(this.recUsername==""){
        alert("Select a user !!")
      }
      this.upld = true;
      this.sts="";
      let formData = new FormData();
      let response1;


      formData.append('file',this.file);
      formData.append('username',this.recUsername);


        try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/upload", formData);

          if(response.data.message == "Notes upload successful") {
             this.response1 = await axios
                .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/share", {
                  username: localStorage.username,
                  file: this.file.name,
                  recName: this.recUsername

                });
          }
        if(this.response1.data.message == "Notes shared successful"){
          this.$router.go(0);
        }
      }
      catch (err) {
        this.upld = false;
        console.log(err)
        this.sts=" Error sharing file !!";

      }
    }
    }
}
</script>

<style scoped>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99;
  background-color: rgba(0, 0, 0, 0.2);

  display: flex;
  align-items: center;
  justify-content: center;
}
  .popup-inner {
    background: #FFF;
    padding: 32px;
  }
#updl{
  align: center;
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