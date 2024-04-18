<script setup>
// import { ref,defineEmits} from 'vue'
import { ref } from 'vue'

import { useloginStore } from '@/stores/login'
import { useUserProfileStore } from '@/stores/profile'
import { useRouter } from 'vue-router';

const router = useRouter();

const loginStore = useloginStore()
const userStore = useUserProfileStore()

const theme = ref('light')

function onClick() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

// const emit = defineEmits(['logout'])

// const props = defineProps({
//   Username: String,
// });

const logout = () => {
  // emit("logout")
  loginStore.logout()
  router.push({ path: '/' });
}
</script>

<template>
  <v-app :theme="theme">
    <v-app-bar>
      <v-spacer></v-spacer>

      <v-btn @click="onClick">
        <v-icon>
          {{ theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night' }}
        </v-icon>
      </v-btn>
      <v-btn @click="logout" color="error">Log out</v-btn>
    </v-app-bar>

    <!-- <v-navigation-drawer expand-on-hover rail permanent>
      <v-list>
        <v-list-item prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg" subtitle="sandra_a88@gmailcom"
          :title="loginStore.Username"></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-folder" title="My Files" value="myfiles"></v-list-item>

        <v-list-item>
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <router-link to="/about" class="text-decoration-none">
              <v-list-item-title>Shared with me</v-list-item-title>
            </router-link>
          </v-list-item-content>
        </v-list-item>

        <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>
      </v-list>
    </v-navigation-drawer> -->

    <!-- # 2 -->
    <v-layout class="rounded rounded-md">
      <v-app-bar title="Application bar"></v-app-bar>

      <v-navigation-drawer>
        <v-list>
          <v-list-item prepend-avatar="https://as1.ftcdn.net/v2/jpg/05/53/79/60/1000_F_553796090_XHrE6R9jwmBJUMo9HKl41hyHJ5gqt9oz.jpg"
            :subtitle="userStore.userProfile.email" :title="loginStore.Username" to="/Profile"></v-list-item>
        </v-list>
        <v-divider></v-divider>

        <v-list dense nav>
          <!-- <div>{{ loginStore.role }}</div> -->
          <v-list-item prepend-icon="mdi-home" title="หน้าหลัก" value="starred" to="/"></v-list-item>
          <v-list-item prepend-icon="mdi-folder" title="1: สร้างวิชา"  to="/subject"></v-list-item>
          <v-list-item prepend-icon="mdi-folder-plus" title="2: สร้างชุดข้อสอบ" to="/createExam"></v-list-item>
          <v-list-item prepend-icon="mdi-format-list-bulleted" title="3: นำเข้ารายชื่อนักศึกษา"  to="/listOfStu"></v-list-item>

          <v-list-item prepend-icon="mdi-folder-key-outline" title="4: นำเข้าเฉลย" to="/importAnswer"></v-list-item>
          <v-list-item prepend-icon="mdi-file-upload-outline" title="5: นำเข้ากระดาษคำตอบ" to="/UploadExam"></v-list-item>
          <v-list-item prepend-icon="mdi-magnify-scan" title="6: ตรวจข้อสอบ" to="/CheckAnswer"></v-list-item>
          <v-list-item prepend-icon="mdi-image" title="7: ผลลัพธ์" to="/InsertStudent"></v-list-item>
          
          
          <!-- <v-list-item prepend-icon="mdi-home" title="Home" value="starred" to="/"></v-list-item> -->
        
          <!-- <v-list-item prepend-icon="mdi-folder" title="Subject"  to="/subject"></v-list-item> -->
        
          <!-- <v-list-item prepend-icon="mdi-note-text" title="Exam" to="/test"></v-list-item> -->

          <!-- <v-list-item prepend-icon="mdi-note-text" title=" Create Exam" to="/createExam"></v-list-item> -->

  

          <!-- <v-list-item prepend-icon="mdi-magnify-scan" title="Check the exam" to="/login"></v-list-item> -->

        <!-- <v-list-item prepend-icon="mdi-note-text" title="Exam" to="/test"></v-list-item>
          
          <v-list-item prepend-icon="mdi-magnify-scan" title="Check the exam" to="/login"></v-list-item> -->
        </v-list>


      </v-navigation-drawer>

      <v-main>
        <v-container grid-list-xs>
          <router-view></router-view>
        </v-container>
      </v-main>
    </v-layout>

    <!-- <v-main>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main> -->
  </v-app>
</template>
