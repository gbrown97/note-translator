<template>

  <div class="popup">
    <div class="popup-inner">

      <form @submit.prevent="onUpload">
        <h1 style="color:red;">{{sts}}</h1>
        <upload id="updl" v-if="upld">

        </upload><br><br>
      <input type="file" @change="uploadFile" ref="file">
      <input type="text" placeholder="username" v-model="username">&nbsp
      <input type="text" placeholder="language" v-model="language">&nbsp
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
      sts:''

    };
  },
  methods:{
    uploadFile() {

      this.file = this.$refs.file.files[0];
    },
    async  onUpload() {
      this.upld = true;
      this.sts="";
      let formData = new FormData();


      formData.append('file',this.file);
      formData.append('username',this.username);


        try{
        const response = await axios
            .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/upload", formData);

        const response1 = await axios
              .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/translate", {
                username: localStorage.username,
                file: this.file.name,
                srcLang: "en",
                destLang:this.language

              });
          const response2 = await axios
              .post("http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/share", {
                username: localStorage.username,
                file: this.file.name,
                recName: this.username

              });

        if(response.data.message == "Notes upload successful"){
          this.$router.go(0);
        }
      }
      catch (err) {
        this.upld = false;
        console.log(err)
        this.sts=" Error uploading file !!";

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
</style>