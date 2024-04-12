<script setup>
import '@mdi/font/css/materialdesignicons.css'

import MainView from "./views/MainView.vue"
import loginView from "./views/loginView.vue"
import RegisterView from "./views/RegisterView.vue"
import { onMounted, ref } from 'vue';
import { useloginStore } from '@/stores/login'
// import AdminView from './views/AdminView.vue';

const loginStore = useloginStore();
const tab = ref(null)

onMounted(() => {
  console.log("on mouse")
  loginStore.loadData();
})

</script>

<template>
  <div v-if="loginStore.isLogin">
    <v-card>
      <v-tabs v-model="tab" background-color="transparent">
        <v-tab value="login">Login</v-tab>
        <v-tab value="register">Register</v-tab>
      </v-tabs>
      
      <v-tab-item value="login" v-if="tab === 'login'">
        <loginView />
      </v-tab-item>
      
      <v-tab-item value="register" v-if="tab === 'register'">
        <RegisterView />
      </v-tab-item>
    </v-card>
  </div>
  
  <div v-else-if="!loginStore.isLogin">
    <MainView @logout="loginStore.logout" :Username="loginStore.Username"/>
  </div>
  <!-- <div v-else="!loginStore.isAdminLogin">
    <AdminView @logout="loginStore.logout" :Username="loginStore.Username"/>
  </div> -->
</template>

<!-- <template>
  <div v-if="loginStore.isAdminLogin">
    <AdminView @logout="loginStore.logout" :Username="loginStore.Username"/>
  </div>
  <div v-else-if="loginStore.isLogin">
    <MainView @logout="loginStore.logout" :Username="loginStore.Username"/>
  </div>
  <div v-else>
    <v-card>
      <v-tabs v-model="tab" background-color="transparent">
        <v-tab value="login">Login</v-tab>
        <v-tab value="register">Register</v-tab>
      </v-tabs>
      
      <v-tab-item value="login" v-if="tab === 'login'">
        <loginView />
      </v-tab-item>
      
      <v-tab-item value="register" v-if="tab === 'register'">
        <RegisterView />
      </v-tab-item>
    </v-card>
  </div>
</template> -->

