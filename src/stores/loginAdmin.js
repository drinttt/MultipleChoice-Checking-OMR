import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAdminLoginStore = defineStore('adminLogin', () => {
  const adminUsername = ref('');
  const isAdminLoggedIn = computed(() => adminUsername.value !== '');
  const adminToken = ref(localStorage.getItem('AdminToken') || '');

  const adminLogin = async (username_ad, password_ad) => {
    try {
      const response = await axios.post('http://localhost/api/adminLogin.php', {
        username_ad,
        password_ad
      });

      if (response.data.success) {
        adminUsername.value = username_ad;
        adminToken.value = response.data.token;
        localStorage.setItem('AdminUsername', username_ad);
        localStorage.setItem('AdminToken', response.data.token);
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
    adminToken.value = '';
    localStorage.removeItem('AdminUsername');
    localStorage.removeItem('AdminToken');
  };

  const loadAdminData = () => {
    adminUsername.value = localStorage.getItem('AdminUsername') || '';
    adminToken.value = localStorage.getItem('AdminToken') || '';
  };

  return {
    adminUsername,
    isAdminLoggedIn,
    adminToken,
    adminLogin,
    adminLogout,
    loadAdminData
  };
});
