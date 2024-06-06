<script>
import axios from 'axios'

export default {
  name: 'CreateExamView',
  data() {
    return {
      exam: {
        code_subject: '',
        name_exam: '',
        qty_exam: null,
        // points: null,
      },
      userSubject: []
    };
  },
  mounted() {
    this.fetchUserSubject();
  },
  methods: {
    async submitExam() {
      try {

        if (this.exam.qty_exam > 100) {
          alert('The number of questions must not exceed 100.');
          return;
        }
        const formData = new FormData();
        formData.append('code_subject', this.exam.code_subject);
        formData.append('name_exam', this.exam.name_exam);
        formData.append('qty_exam', this.exam.qty_exam);
        // formData.append('points', this.exam.points);

        const response = await axios.post('http://localhost/api/createExam.php', formData);
        console.log(response.data);

        if (response.data.success) {
          // แสดงข้อความคำตอบจาก API ในรูปแบบของ pop-up
          alert('Exam created successfully');
        } else {
          alert('An error occurred while submitting the exam. Please try again later.');
        }
      } catch (error) {
        console.error('There was an error submitting the exam:', error);
        alert('An error occurred while submitting the exam. Please try again later.');
      }
    },
    async fetchUserSubject() {
      const username = localStorage.getItem('Username');
      try {
        const response = await axios.get(`http://localhost/api/subject.php?username=${username}`);
        this.userSubject = response.data;
      } catch (error) {
        console.error('Error fetching user subjects:', error);
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

.form-group input[type="text"],
.form-group input[type="number"],
.form-group select {
  /* เพิ่มเลือกเข้ามาในการปรับแต่ง */
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  background-color: #007bff;
  /* เปลี่ยนเป็นสีฟ้า */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3;
  /* เปลี่ยนสีเมื่อโฮเวอร์ */
}
</style>

<template>
  <div class="create-exam-view">
    <h1>Create Exam</h1>
    <form @submit.prevent="submitExam">

      <!-- <div class="form-group">
          <label for="codeSubject">Subject:</label>
          <select id="codeSubject" v-model="exam.code_subject" required>
            <option value="">Please select</option>
            <option v-for="subject in subjectStore.userSubject" :key="subject.code_subject" :value="subject.code_subject">{{ subject.name_subject }}</option>
          </select>
        </div> -->

      <div class="form-group">
        <label for="codeSubject">Subject:</label>
        <select id="codeSubject" v-model="exam.code_subject" required>
          <option value="">Please select</option>
          <option v-for="subject in userSubject" :key="subject.code_subject" :value="subject.code_subject">{{
            subject.name_subject }}</option>
        </select>
      </div>


      <div class="form-group">
        <label for="nameExam">Exam Name:</label>
        <input type="text" id="nameExam" v-model="exam.name_exam" required>
      </div>

      <div class="form-group">
        <label for="qtyExam"> No. of questions:</label>
        <input type="number" id="qtyExam" v-model.number="exam.qty_exam" required min="1">
      </div>

      <div class="form-group">
        <a href="\src\template\answer_sheet_100.pdf" download="answer_sheet_100.pdf"
          style="color: blue; font-weight: bold; font-size: smaller; font-style: italic;">
          กดดาวน์โหลดเทมเพลตกระดาษคำตอบ</a>
      </div>

      <button type="submit">Submit</button>
    </form>
  </div>
</template>