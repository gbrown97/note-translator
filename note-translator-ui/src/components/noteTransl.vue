<template>
  <div >

    <img src="noteTrans.png" alt="Note Translator">
    <h1>Welcome to Note Translation</h1>
    <br>
    <form>
    <input type="text" placeholder="Username" v-model="username">
    <br>
    <br>
    <input type="password" placeholder="Password" v-model="password">
    <br>
    <br>

      <button @click="onLogin()">Login</button>

      <button @click="$router.push('/signup')">Signup</button>

    </form>

  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data(){
    return {

      username: "",
      password: "",
    };
  },
  methods:{
    onLogin() {

      axios
          .post("", {

            username: this.username,
            password: this.password,
          })
          .then((response) => {
            console.log(response.data)
          });

    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div{

}
input {
color: #2c3e50;
  font-size: x-large;
  padding: 15px;
  border-radius: 25px;
  width: 300px;
  height: 20px
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
