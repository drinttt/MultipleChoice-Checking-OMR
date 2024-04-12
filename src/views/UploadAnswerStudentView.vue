<script>
import axios from 'axios';

export default {
    name: 'UploadAnswerStudentView',
    data() {
        return {
            exam: {
                id_exam: '',
            },
            idexams: [],
            selectedFiles: null, // Store selected files
        };
    },
    mounted() {
        this.fetchidexams();
    },
    methods: {
        async fetchidexams() {
            const username = localStorage.getItem('Username');
            try {
                const response = await axios.get(`http://localhost/api/getCodeExam.php?username=${username}`);
                this.idexams = response.data;
            } catch (error) {
                console.error('Error fetching code exams:', error);
            }
        },
        handleFilesUpload(event) {
            this.selectedFiles = event.target.files; // Store selected files
        },
        async submitFiles() {
            if (!this.selectedFiles || this.selectedFiles.length === 0 || !this.exam.id_exam) {
                alert('Please select files and choose an exam.');
                return;
            }
            const formData = new FormData();
            for (let i = 0; i < this.selectedFiles.length; i++) {
                formData.append('files[]', this.selectedFiles[i]);
            }
            formData.append('id_exam', this.exam.id_exam);
            try {
                const response = await axios.post('http://localhost/api/uploadFiles.php', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.log(response.data); // Handle response
                alert('Files uploaded successfully!'); // Alert message after successful upload
            } catch (error) {
                console.error('Error uploading files:', error);
                alert('E'); // Alert message after successful upload
            }
        }

    }
};
</script>

<template>
    <div class='check-body'>
        <h1>อัปโหลดรูปกระดาษคำตอบ</h1>
        <form @submit.prevent="submitFiles">
            <div class="form-group">
                <label for="idexam">Subject - Exam:</label>
                <select id="idexam" v-model="exam.id_exam" required>
                    <option value="">Please select</option>
                    <option v-for="exam in idexams" :key="exam.id_exam" :value="exam.id_exam">
                        {{ exam.name_subject }} - {{ exam.name_exam }}
                    </option>
                </select>
            </div>
            <div class="form-group">
                <label for="images">Upload Images:</label>
                <input type="file" id="images" @change="handleFilesUpload" multiple>
            </div>
            <div>
                <a style="color: red; font-weight: bold; font-size: smaller; font-style: italic;">
                    หมายเหตุ: ชื่อไฟล์รูปภาพต้องเป็นเลขลำดับตามใบรายชื่อ ตัวอย่างเช่น ลำดับที่ 1 นายใจดี ดีใจ รหัสนักศึกษา 6304062630077 ชื่อไฟล์รูปคือ 1.jpg</a>
            </div>
            <button type="submit">Upload</button>
        </form>
    </div>
</template>

<style>
    .check-body {
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
        color: black; /* เปลี่ยนสีของข้อความใน drop-down เป็นสีดำ */
    }

button[type="submit"] {
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