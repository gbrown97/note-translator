<template>
  <div>
    <img src="noteTrans.png" alt="Note Translator">
    <h1>Create an account</h1>
    <br>
    <form>
      <input id="fln" type="text" placeholder="FirstName" v-model="fname">
      <input id="fln" type="text" placeholder="LastName" v-model="lname">
      <br>
      <br>
      <select class="form-control" v-model="languagesel">
        <option  value="">Select preferred language</option>
        <option :value="language.name"  v-for="(language) in languagesList" :key="language.name">{{language.name}}</option>

      </select>
      <h4 style="color:red;">{{err1}}</h4>

      <br><br>
      <input type="text" placeholder="Email/Username" v-model="username"><h4 style="color:red;">{{err3}}</h4>
      <br>
      <br>
      <div>
        <input type="password" placeholder="password" v-model="password"><h4 style="color:red;">{{err2}}</h4></div>
      <br>

      <input type="password" placeholder="Retype-password" v-model="rpassword">
      <br>
      <br>
      <button @submit.prevent @click.prevent="onSignup()">Signup</button>



    </form>

  </div>
</template>

<script>
import axios from "axios";

let languages = require('./languages.json');
export default {
  mounted () {
  console.log ('Sineup component mounted.')
  },
  name: 'signup-component',
  data(){
    return{
      err1:'',
      err2:'',
      err3:'',
      languagesList: languages,
      fname:"",
      lname:"",
      languagesel:"",
      username: "",
      password: "",
      rpassword:""
    }
  },
  methods: {
    onSignup() {
      if(this.languagesel==""){
        this.err1="select a language *";
      }else{
        this.err1="";
      }
      if(this.password!=this.rpassword||this.password==""||this.rpassword==""){
              this.err2="Incorrect/password mismatch !! *";
      }
      else{
        this.err2="";
      }
      if(this.languagesel!=""&&this.password!=""&&this.rpassword!=""&&this.password==this.rpassword){

              axios
                  .post('http://note-translator-backend-env.eba-nunmcyk7.us-east-2.elasticbeanstalk.com/signup', {
                    username: this.username,
                    password: this.password,
                    fname: this.fname,
                    lname: this.lname,
                    setLang: this.languagesel

                  })
                  .then((response) => {
                    console.log(response.data)
                   alert("Account created successfully !!!")
                    this.$router.push('/')
                  }).catch((error) => {

                       if(error.message=="Request failed with status code 406"){
                          this.err3="Username already exists !!"
                       }
              });
            }
    }

  }
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h4{display: block;
margin-left: 1320px;
  margin-top: -35px;
  position: fixed;
}

#fln{
  color: #2c3e50;
  margin-left: 2px;
  font-size: x-large;
  padding: 15px;
  border-radius: 25px;
  width: 130px;
  height: 20px
}
input {
  color: #2c3e50;
  font-size: x-large;
  padding: 15px;
  border-radius: 25px;
  width: 300px;
  height: 20px;
}
select {
  color: #2c3e50;

  font-size: larger;
  padding: 15px;
  border-radius: 25px;
  width: 330px;
  height: 55px;



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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
