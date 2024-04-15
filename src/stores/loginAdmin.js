import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAdminLoginStore = defineStore('adminLogin', () => {
  const adminUsername = ref('')
  const isAdminLoggedIn = computed(() => {
    return adminUsername.value === ''
  })

  // const adminToken = ref(localStorage.getItem('adminToken') || '');

  const adminLogin = async (username_ad, password_ad) => {
    try {
      const response = await axios.post('http://localhost/api/adminLogin.php', {
        username_ad,
        password_ad
      });

      if (response.data.success) {
        adminUsername.value = username_ad;
        // adminToken.value = response.data.token;
        localStorage.setItem('adminUsername', username_ad);
        localStorage.setItem('adminToken', response.data.token);
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
    // adminToken.value = '';
    localStorage.removeItem('adminUsername');
    localStorage.removeItem('adminToken');
  };

  const loadAdminData = () => {
    adminUsername.value = localStorage.getItem('adminUsername') || '';
    // adminToken.value = localStorage.getItem('adminToken') || '';
  };

  return {
    adminUsername,
    isAdminLoggedIn,
    // adminToken,
    adminLogin,
    adminLogout,
    loadAdminData
  };
});
