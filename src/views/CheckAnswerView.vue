<template>
  <div class="create-exam-view">
    <h1>Check Answer</h1>
    <form @submit.prevent="submitExam">
      <div class="form-group">
        <label for="idexam">Exam:</label>
        <select id="idexam" v-model="exam.id_exam" required>
          <option value="">Please select</option>
          <option v-for="exam in idexams" :key="exam.id_exam" :value="exam.id_exam">
            {{ exam.name_subject }} - {{ exam.name_exam }}
          </option>
        </select>
      </div>
      <div>
        <button type="button" @click="runPythonScript">ตรวจคำตอบ (กระดาษคำตอบ 50 ข้อ)</button>
      </div>
      <br>
      <div>
        <button type="button" @click="runPythonScript_100">ตรวจคำตอบ (กระดาษคำตอบ 100 ข้อ)</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';


export default {
  name: 'CheckAnswerView',
  data() {
    return {
      exam: {
        id_exam: '',
      },
      idexams: [],
    };
  },
  mounted() {
    this.fetchidexams();
  },
  methods: {
    async fetchidexams() {
      const username = localStorage.getItem('Username');
      try {
        const response = await axios.get(`http://localhost/api/getCodeExamForCheck.php?username=${username}`);
        this.idexams = response.data;
      } catch (error) {
        console.error('Error fetching code exams:', error);
      }
    },
    async runPythonScript() {
      try {
        // Include the id_exam in the data object being sent
        const postData = {
              // scriptPath: 'C:\\OMR_WebApp-main\\omr_process.py',
              scriptPath: 'D:\\Dear\\IV\\Project\\OMR_WebApp\\pages\\omr_process.py',
              id_exam: this.exam.id_exam // This line sends the id_exam value to the API
            };

        const response = await axios.post('http://localhost/api/runPythonScript.php', postData, {
          headers: {
            "Content-Type": "application/json"
          }
        });

            if (response.data.success) {
              alert('Python script executed successfully with exam ID: ' + this.exam.id_exam);
            } else {
              alert('Failed to execute Python script with exam ID: ' + this.exam.id_exam);
            }
      } catch (error) {
        console.error('Error executing Python script:', error);
        alert('An error occurred while executing the Python script. Exam ID: ' + this.exam.id_exam);
      }
    },
    async runPythonScript_100() {
      try {
        // Include the id_exam in the data object being sent
        const postData = {
              // scriptPath: 'C:\\OMR_WebApp-main\\omr_process_100.py',
              scriptPath: 'D:\\Dear\\IV\\Project\\OMR_WebApp\\pages\\omr_process_100.py',
              id_exam: this.exam.id_exam // This line sends the id_exam value to the API
            };

        const response = await axios.post('http://localhost/api/runPythonScript.php', postData, {
          headers: {
            "Content-Type": "application/json"
          }
        });

            if (response.data.success) {
              alert('Python script executed successfully with exam ID: ' + this.exam.id_exam);
            } else {
              alert('Failed to execute Python script with exam ID: ' + this.exam.id_exam);
            }
      } catch (error) {
        console.error('Error executing Python script:', error);
        alert('An error occurred while executing the Python script. Exam ID: ' + this.exam.id_exam);
      }
    }

  }      
};
</script>

<style scoped>
.create-exam-view {
  max-width: 500px;
  margin: auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input[type="file"],
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: black;
}

button[type="submit"],
button[type="button"] {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button[type="submit"]:hover,
button[type="button"]:hover {
  background-color: #0056b3;
}
</style>