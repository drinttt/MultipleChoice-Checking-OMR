import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useloginStore = defineStore('login', () => {
  const Username = ref('')
  const isLogin = computed(() => {
    return Username.value === ''
  })

  // const login = (userName) => {
  //   Username.value = userName
  //   localStorage.setItem("Username", userName)
  // }
  const login = async (username, password) => {
    try {
      const response = await axios.post('http://localhost/api/login.php', {
        username,
        password
      })
      if (response.data.success) {
        Username.value = username
        localStorage.setItem('Username', username)
        // คุณอาจจะต้องการเก็บ token ไว้ใช้งานต่อไป
        localStorage.setItem('Token', response.data.token)
      } else {
        throw new Error(response.data.message)
      }
    } catch (error) {
      console.error('Login failed:', error)
      throw error // ส่งต่อ error ไปยัง component ที่เรียกใช้
    }
  }

  const logout = () => {
    Username.value = ''
    localStorage.removeItem('Username')
    localStorage.removeItem("Token");
  }

  const loadData = () => {
    Username.value = localStorage.getItem('Username') || ''
  }

  return { Username, isLogin, login, logout, loadData }
})
