import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAdminLoginStore = defineStore('adminLogin', () => {
  // const adminUsername = ref('')
  const isAdminLoggedIn = computed(() => {
    return adminUsername.value === ''
  })

  // const adminToken = ref(localStorage.getItem('adminToken') || '');

  // ใช้ sessionStorage แทน localStorage
const adminUsername = ref(sessionStorage.getItem('adminUsername') || '');

const adminLogin = async (username_ad, password_ad) => {
  try {
    const response = await axios.post('http://localhost/api/adminLogin.php', {
      username_ad,
      password_ad
    });

    if (response.data.success) {
      adminUsername.value = username_ad;
      sessionStorage.setItem('adminUsername', username_ad); // ใช้ sessionStorage เก็บข้อมูล
      sessionStorage.setItem('adminToken', response.data.token); // ใช้ sessionStorage เก็บข้อมูล
      console.log("Admin login success:");
    } else {
      throw new Error(response.data.message);
    }
  } catch (error) {
    console.error('Admin login failed:', error);
    throw error; // Propagate the error to the caller
  }
};

const adminLogout = () => {
  adminUsername.value = '';
  sessionStorage.removeItem('adminUsername'); // ใช้ sessionStorage เก็บข้อมูล
  sessionStorage.removeItem('adminToken'); // ใช้ sessionStorage เก็บข้อมูล
};

const loadAdminData = () => {
  adminUsername.value = sessionStorage.getItem('adminUsername') || ''; // ใช้ sessionStorage เก็บข้อมูล
};

return {
  adminUsername,
  isAdminLoggedIn,
  adminLogin,
  adminLogout,
  loadAdminData
};

});
