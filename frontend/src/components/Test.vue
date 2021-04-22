<template>
<div id="welcome">
  <h2>Hello</h2>
  <input v-model="name">
  <button v-on:click='sayhello'>Send</button>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Test',
  methods:{
    sayhello:function(){
      axios({
        method: 'GET',
        url:'http://localhost:80/test',
        params:{
          name: this.name
        }
      }).then(response=>{
        alert(response['data']['data']);
      });

    }
  }
}
</script>


<style>

</style>
