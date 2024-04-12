import { defineStore } from 'pinia';
import axios from 'axios';

export const useExamStore = defineStore('userExam', {
  state: () => ({
    userExam: []
  }),
  actions: {
    async fetchUserExam(code_subject) {
      try {
        const response = await axios.get(`http://localhost/api/exam.php?code_subject=${code_subject}`);
        this.userExam = response.data;
      } catch (error) {
        console.error('Error fetching exams:', error);
      }
    },
    async fetchUserExamByCode(id_exam) {
      try {
        const response = await axios.get(`http://localhost/api/id_exam.php?id_exam=${id_exam}`);
        if (response.data) {
          return response.data;
        }
      } catch (error) {
        console.error('Error fetching exam by code:', error);
      }
    },
  }
});
