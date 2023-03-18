<template>
  <div>
    <img src="noteTrans.png" alt="Note Translator">
    <h1>Create an account</h1>
    <br>
    <form>
      <input id="fln" type="text" placeholder="FirstName">
      <input id="fln" type="text" placeholder="LastName">
      <br>
      <br>
      <select class="form-control">
        <option :value="language.name" v-for="(language) in languagesList" :key="language.name">{{language.name}}</option>
        <option :value="null" disabled></option>
      </select>
      <br>
      <br>
      <input type="text" placeholder="Email/Username">
      <br>
      <br>
      <input type="password" placeholder="password">
      <br>
      <br>
      <input type="password" placeholder="Retype-password">
      <br>
      <br>
      <button>Signup</button>



    </form>

  </div>
</template>

<script>
let languages = require('./languages.json');
export default {
  name: 'signup-component',
  data(){
    return{
      languagesList: languages,
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
  width: 320px;
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
