import { defineStore } from 'pinia'
import axios from 'axios'

export const useSubjectStore = defineStore('userSubject', {
    state: () => ({
        userSubject: []
    }),
    actions: {
        async fetchUserSubject() {
            const username = localStorage.getItem('Username');
            try {
                const response = await axios.get(`http://localhost/api/subject.php?username=${username}`);
                // console.log(response.data);
                this.userSubject = response.data;
              } catch (error) {
                console.error('Error fetching user profile:', error);
              }
        },
        async addSubject(subjectData) {
            try {
                const response = await axios.post('http://localhost/api/add_subject.php', subjectData);
                if (response.data.success) {
                    this.fetchUserSubject(); // รีเฟรชข้อมูลวิชา
                } else {
                    console.error('Error adding subject:', response.data.message);
                }
            } catch (error) {
                console.error('Error adding subject:', error);
            }
        },
        // async updateSubject(subjectData) {
        //     try {
        //     //   const response = await axios.post('http://localhost/api/update_subject.php', subjectData);
        //       const response = await axios.post(`http://localhost/api/update_subject.php?code_subject=${subjectData.code_subject}`, subjectData);
        //       console.log(subjectData.code_subject)
        //       console.log("hii")
        //       console.log(subjectData.year)
        //       console.log(subjectData.term)
        //       console.log(subjectData.name_subject)
        //       if (response.data.success) {
        //         this.fetchUserSubject(); // รีเฟรชข้อมูลวิชาเพื่อแสดงผลลัพธ์ล่าสุด
        //       } else {
        //         console.error('Error updating subject:', response.data.message);
        //       }
        //     } catch (error) {
        //       console.error('Error updating subject:', error);
        //     }
        // },
        async fetchSubjectByCode(code_subject) {
            try {
                const response = await axios.get(`http://localhost/api/code_subject.php?code_subject=${code_subject}`);
                if (response.data) {
                    // กลับข้อมูลวิชา
                    return response.data;
                }
            } catch (error) {
                console.error('Error fetching subject by code:', error);
            }
        },
        async uploadStudentList(code_subject, section, students) {
            try {
              const response = await axios.post('http://localhost/api/uploadStudentList.php', {
                code_subject,
                section,
                students
              })
              if (response.data.success) {
                alert('Student list uploaded successfully')
              } else {
                alert('An error occurred: ' + response.data.message)
              }
            } catch (error) {
              alert('An error occurred while uploading the student list.')
            }
        }
    }
})