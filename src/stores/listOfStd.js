import { defineStore } from 'pinia'
import axios from 'axios'

export const useListOfStdStore = defineStore('listOfStd', {
  actions: {
    async uploadStudentList(code_subject, section, students) {
      try {
        const response = await axios.post('http://localhost/api/uploadStudentList.php', {
          code_subject,
          section,
          students
        })
        console.log(response)
        if (response.data.success) {
          console.log('Student list uploaded successfully')
        } else {
          console.error('An error occurred: ' + response.data.message)
        }
      } catch (error) {
        console.error('An error occurred while uploading the student list.', error)
      }
    }
  }
})
