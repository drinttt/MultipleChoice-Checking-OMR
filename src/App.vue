<script setup>
import '@mdi/font/css/materialdesignicons.css'

import MainView from "./views/MainView.vue"
import loginView from "./views/loginView.vue"
import RegisterView from "./views/RegisterView.vue"
import loginAdmin from './views/loginAdmin.vue';
import AdminView from './views/AdminView.vue';

import { onMounted, ref } from 'vue';
import { useloginStore } from '@/stores/login'
import { useAdminLoginStore } from '@/stores/loginAdmin'
// import AdminView from './views/AdminView.vue';

const loginStore = useloginStore();
const AdminloginStore = useAdminLoginStore()

const tab = ref(null)

onMounted(() => {
  console.log("on mouse")
  loginStore.loadData();
})

</script>

<template>
  <div v-if="loginStore.isLogin && AdminloginStore.isAdminLoggedIn">
    <!-- <div v-if="loginStore.isLogin"> -->
    <v-card>
      <v-tabs v-model="tab" background-color="transparent">
        <v-tab value="login">Login</v-tab>
        <v-tab value="register">Register</v-tab>
        <v-tab value="adminLogin">Admin</v-tab>
      </v-tabs>

      <v-tab-item value="login" v-if="tab === 'login'">
        <loginView />
      </v-tab-item>

      <v-tab-item value="register" v-if="tab === 'register'">
        <RegisterView />
      </v-tab-item>

      <v-tab-item value="adminLogin" v-if="tab === 'adminLogin'">
        <loginAdmin />
      </v-tab-item>
    </v-card>
  </div>

  <div v-else-if="!loginStore.isLogin && AdminloginStore.isAdminLoggedIn">
    <MainView @logout="loginStore.logout" :Username="loginStore.Username" />
  </div>

  <!-- <div v-else-if="loginStore.isLogin && !AdminloginStore.isAdminLoggedIn">
    <AdminView @logout="AdminloginStore.adminLogout" :adminUsername="AdminloginStore.adminUsername" />
  </div> -->


  <div v-else>
    <AdminView @logout="AdminloginStore.adminLogout" :Username="AdminloginStore.adminUsername" />
  </div>

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
