<template>
    <div class="create-exam-view">
        <h1>Import Answer</h1>
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

            <div class="form-group">
                <label for="excelFile">Upload Excel File:</label>
                <input type="file" id="excelFile" ref="file" accept=".xls,.xlsx" required>
                <a href="\src\template\template_addAnswer.xlsx" download="template_addAnswer.xlsx" 
                    style="color: blue; font-weight: bold; font-size: smaller; font-style: italic;">
                    ดาวน์โหลดเทมเพลตในการอัปโหลดเฉลย</a>
            </div>

            <button type="submit">Submit</button>
        </form>
    </div>
</template>


<script>
import axios from 'axios';
import * as XLSX from 'xlsx';

export default {
    name: 'ImportAnswerView',
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
                const response = await axios.get(`http://localhost/api/getCodeExam.php?username=${username}`);
                this.idexams = response.data;
            } catch (error) {
                console.error('Error fetching code exams:', error);
            }
        },
        async submitExam() {
            try {
                const file = this.$refs.file.files[0];
                if (!file) {
                        alert("Please select a file.");
                        return;
                }

                await axios.post("http://localhost/api/deleteOldAnsKey.php", { id_exam: this.exam.id_exam });

                const reader = new FileReader();
                reader.onload = async (e) => {
                    const data = e.target.result;
                    const workbook = XLSX.read(data, { type: 'array' });
                    const sheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[sheetName];
                    const json = XLSX.utils.sheet_to_json(worksheet);
                    console.log(json); // Log the Excel data in JSON format
                    for (const row of json) {
                        const dataToSend = {
                            id_exam: this.exam.id_exam,
                            no_answer_key: row['no_answer_key'],
                            answer_key: row['answer_key']
                        };

                        try {
                            const response = await axios.post("http://localhost/api/importExcel.php", dataToSend, {
                                headers: {
                                    "Content-Type": "application/json"
                                }
                            });

                            if (response.data.success) {
                                // alert(`Data imported successfully for row: no_answer_key=${row['no_answer_key']}, answer_key=${row['answer_key']}`);
                            } 
                        } catch (error) {
                            console.error(`Error sending data for row: ${JSON.stringify(row)} - `, error);
                            // alert(`id_exam=${this.exam.id_exam}, no_answer_key=${row['no_answer_key']}, answer_key=${row['answer_key']}`);
                        }
                    }

                    alert("import answer completed.");

                    };
                    reader.readAsArrayBuffer(file);
            }catch (error) {
                    console.error("Error processing file:", error);
                    alert("An error occurred while processing the file. Please try again later.");
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
    color: black; /* เปลี่ยนสีของข้อความใน drop-down เป็นสีดำ */
}

button[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button[type="submit"]:hover {
    background-color: #0056b3;
}
</style>
