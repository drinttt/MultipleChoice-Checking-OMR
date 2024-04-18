<script setup>
import { ref } from 'vue'
import { useAdminLoginStore } from '@/stores/loginAdmin'
import { useRouter } from 'vue-router';

const router = useRouter();
const AdminloginStore = useAdminLoginStore()

const theme = ref('light')

function onClick() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

const logout = () => {
  // emit("logout")
  AdminloginStore.adminLogout()
  router.push({ path: '/' });
}

</script>
<template>
  <v-app :theme="theme">
    <v-app-bar>
      <h1 class="ml-8">Admin</h1>
      <v-spacer></v-spacer>

      <v-btn @click="onClick">
        <v-icon>
          {{ theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night' }}
        </v-icon>
      </v-btn>
      <v-btn @click="logout" color="error">Log out</v-btn>
    </v-app-bar>

    <v-layout class="rounded rounded-md">
      <v-app-bar title="Application bar"></v-app-bar>

      <v-navigation-drawer>
        <v-list>
          <v-list-item
            prepend-avatar="https://as1.ftcdn.net/v2/jpg/05/53/79/60/1000_F_553796090_XHrE6R9jwmBJUMo9HKl41hyHJ5gqt9oz.jpg"
            :title="AdminloginStore.adminUsername">
          </v-list-item>
        </v-list>
        <v-divider></v-divider>

        <v-list dense nav>

          <v-list-item prepend-icon="mdi-account-box-edit-outline" title="จัดการบัญชีผู้ใช้งาน" to="/manageUser"></v-list-item>
          <!-- <v-list-item prepend-icon="mdi-account-plus" title="เพิ่มผู้ดูแล" value="starred" to="/addAdmin"></v-list-item> -->
        </v-list>

      </v-navigation-drawer>
      <v-main>
        <v-container grid-list-xs>
          <router-view></router-view>
        </v-container>
      </v-main>
    </v-layout>
  </v-app>
</template>