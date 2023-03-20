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
      <br>
      <br>
      <input type="text" placeholder="Email/Username" v-model="username">
      <br>
      <br>
      <input type="password" placeholder="password" v-model="password">
      <br>
      <br>
      <input type="password" placeholder="Retype-password" v-model="rpassword">
      <br>
      <br>
      <button @click="onSignup()">Signup</button>



    </form>

  </div>
</template>

<script>
import axios from "axios";

let languages = require('./languages.json');
export default {
  name: 'signup-component',
  data(){
    return{
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
            if(this.password!=this.rpassword){
              alert("password mismatch !!");
            }
            else if(this.languagesel==""){
              alert("select a language");
            }
            else{
              axios
                  .post("", {
                    fName: this.fname,
                    lName: this.lname,
                    selLan: this.languagesel,
                    username: this.username,
                    password: this.password,
                  })
                  .then((response) => {
                    console.log(response.data)
                  });
            }
    }

  }
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
  height: 20px
}
select {
  color: #2c3e50;
  font-size: larger;
  padding: 15px;
  border-radius: 25px;
  width: 330px;
  height: 55px
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
