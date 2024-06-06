<template>
    <div class="upload-students-view">
        <h1>Import List of Students</h1>
        <form @submit.prevent="submitList">
            <div class="form-group">
                <label for="idexam">Exam:</label>
                <select id="idexam" v-model="exam.id_exam" required>
                    <option value="">Please select</option>
                    <option v-for="exam in idexams" :key="exam.id_exam" :value="exam.id_exam">
                        {{ exam.name_subject }} - {{ exam.name_exam }}
                    </option>
                </select>
            </div>

            <!-- <div class="form-group">
                <label for="section">Section:</label>
                <input type="text" id="section" v-model="section" required>
            </div> -->

            <div class="form-group">
                <label for="excelFile">Upload Excel File:</label>
                <input type="file" id="excelFile" ref="file" accept=".xls,.xlsx" required>
                <a href="\src\template\template_listOfStd.xlsx" download="template_addAnswer.xlsx"
                    style="color: blue; font-weight: bold; font-size: smaller; font-style: italic;">
                    ดาวน์โหลดเทมเพลตในการอัปโหลดรายชื่อนักศึกษา</a>
            </div>

            <!-- <button type="submit">Upload</button> -->
            <button type="submit" :disabled="isLoading">
                <span v-if="isLoading">
                    <span class="mr-2">Upload</span><v-icon>mdi-loading mdi-spin</v-icon>
                </span>
                <span v-else>
                    <span class="mr-2">Upload</span>
                    <span v-if="isLoading">
                        <v-icon>mdi-loading mdi-spin</v-icon>
                    </span>
                </span>
            </button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import * as XLSX from 'xlsx';

export default {
    name: 'UploadStudentsView',
    data() {
        return {
            selectedSubject: '',
            // section: '',
            file: null,
            codeSubjects: [],
            exam: {
                id_exam: '',
            },
            idexams: [],
            isLoading: false,

        };
    },
    mounted() {
        this.fetchidexams();
    },
    methods: {
        // async fetchidexams() {
        //     try {
        //         const response = await axios.get('http://localhost/api/getCodeExam.php');
        //         this.idexams = response.data;
        //     } catch (error) {
        //         console.error('Error fetching code exams:', error);
        //     }
        // },
        async fetchidexams() {
            const username = localStorage.getItem('Username');
            try {
                const response = await axios.get(`http://localhost/api/getCodeExam.php?username=${username}`);
                this.idexams = response.data;
            } catch (error) {
                console.error('Error fetching code exams:', error);
            }
        },
        // async submitList() {
        //     try {
        //         const file = this.$refs.file.files[0];
        //         if (!file) {
        //             alert("Please select a file.");
        //             return;
        //         }

        //         console.log(this.selectedSubject); // Debug: Log the selectedSubject to confirm it's set

        //         // const vueInstance = this; // Ensure vueInstance is defined in the correct scope

        //         const reader = new FileReader();
        //         reader.onload = async (e) => {
        //             const data = e.target.result;
        //             const workbook = XLSX.read(data, { type: 'array' });
        //             const sheetName = workbook.SheetNames[0];
        //             const worksheet = workbook.Sheets[sheetName];
        //             const json = XLSX.utils.sheet_to_json(worksheet);

        //             for (const row of json) {
        //                 const dataToSend = {
        //                     id_exam: this.exam.id_exam, // Correctly use vueInstance here
        //                     no_student: row['ลำดับ'],
        //                     id_student: row['เลขประจำตัวนักศึกษา'],
        //                     st_name: row['ชื่อ'],
        //                     section: this.section
        //                 };

        //                 try {
        //                     const response = await axios.post("http://localhost/api/uploadStudentList.php", dataToSend, {
        //                         headers: {
        //                             "Content-Type": "application/json"
        //                         }
        //                     });

        //                     if (!response.data.success) {
        //                         alert(`Failed to import data for row: id_student=${row['id_student']}, st_name=${row['st_name']}`);
        //                     }
        //                 } catch (error) {
        //                     console.error(`Error sending data for row: ${JSON.stringify(row)} - `, error);
        //                     alert(`Failed to send data for row: id_student=${row['id_student']}, st_name=${row['st_name']}`);
        //                 }
        //             }

        //             alert("Data import process completed. Please check for any errors in the console.");
        //         };
        //         reader.readAsArrayBuffer(file);
        //     } catch (error) {
        //         console.error("Error processing file:", error);
        //         alert("An error occurred while processing the file. Please try again later.");
        //     }
        // }
        async submitList() {
            this.isLoading = true;

            try {
                const file = this.$refs.file.files[0];
                if (!file) {
                    alert("Please select a file.");
                    return;
                }

                // ลบข้อมูลนักศึกษาเก่าจากตาราง student_answer
                await axios.post("http://localhost/api/deleteStudentAnswersByExam.php", { id_exam: this.exam.id_exam });

                // ลบข้อมูลนักศึกษาเก่าจากตาราง student
                await axios.post("http://localhost/api/deleteStudentsByExam.php", { id_exam: this.exam.id_exam });

                const reader = new FileReader();
                reader.onload = async (e) => {
                    const data = e.target.result;
                    const workbook = XLSX.read(data, { type: 'array' });
                    const sheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[sheetName];
                    const json = XLSX.utils.sheet_to_json(worksheet);


                    const expectedColumnNames = ['ลำดับ', 'เลขประจำตัวนักศึกษา', 'ชื่อ'];
                    const excelColumnNames = Object.keys(json[0]);
                    for (const columnName of expectedColumnNames) {
                        if (!excelColumnNames.includes(columnName)) {
                            alert(`Failed, Please select a file to upload list of student.`);
                            return;
                        }
                    }

                    for (const row of json) {
                        const dataToSend = {
                            id_exam: this.exam.id_exam,
                            no_student: row['ลำดับ'],
                            id_student: row['เลขประจำตัวนักศึกษา'],
                            st_name: row['ชื่อ'],
                            // section: this.section
                        };

                        await axios.post("http://localhost/api/uploadStudentList.php", dataToSend, {
                            headers: {
                                "Content-Type": "application/json"
                            }
                        });
                    }

                    alert("Data import process completed. Please check for any errors in the console.");
                    this.isLoading = false;
                };
                
                reader.readAsArrayBuffer(file);
            } catch (error) {
                console.error("Error processing file:", error);
                alert("An error occurred while processing the file. Please try again later.");
            } finally {
                this.isLoading = false; // ปิดตัวแสดงโหลด
            }
        }



    },
};
</script>

<style scoped>
.upload-students-view {
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

.form-group input,
.form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
</style>
