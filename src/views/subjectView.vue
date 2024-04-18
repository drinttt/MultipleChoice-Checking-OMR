<!-- <script setup>
import { ref, onMounted, } from 'vue'
import { useSubjectStore } from '@/stores/subject';
import { useUserProfileStore } from '@/stores/profile';

const userStore = useUserProfileStore();
const subjectStore = useSubjectStore();

onMounted(() => {
    userStore.fetchUserProfile(),
    subjectStore.fetchUserSubject();
});

const color = ref('indigo-lighten-2')

const year = ref("")
const term = ref("")
const id_subject = ref("")
const subjectName = ref("")

const resetFormData = () => {
    year.value = '';
    term.value = '';
    id_subject.value = '';
    subjectName.value = '';
};

const add_subject = async () => {
    try {
        const subjectData = {
            username: userStore.userProfile.username,
            year: year.value,
            term: term.value,
            id_subject: id_subject.value, // ตรวจสอบว่าต้องการ id_subject จริงหรือไม่
            name_subject: subjectName.value,
        }
        await subjectStore.addSubject(subjectData)
        dialogCreateSubj.value = false // ปิด dialog หลังจากเพิ่มข้อมูลสำเร็จ
        resetFormData();
    } catch (error) {
        console.error('Error saving subject:', error)
    }
}
const cancel = () => {
    resetFormData(); // รีเซ็ตฟอร์ม
    dialogCreateSubj.value = false; // ปิด dialog
};

// edit
const selectedSubject = ref(null);

const editSubject = (subject) => {
    selectedSubject.value = subject; // กำหนดข้อมูลวิชาที่เลือก
    year.value = subject.year;
    term.value = subject.term;
    id_subject.value = subject.id_subject;
    subjectName.value = subject.name_subject;
    dialogEditSubj.value = true; // เปิด dialog การแก้ไข
};

const cancelEdit = () => {
    // resetFormData();
    dialogEditSubj.value = false; // ปิด dialog
};

const dialogCreateSubj = ref(false)
const dialogEditSubj = ref(false)
</script>

<template>
    <v-container>
        <v-row align="center" class="mx-0">
            <v-col v-for="subject in subjectStore.userSubject" :key="subject.id" cols="3">
                <v-card :color="color" class="mx-auto" max-width="250">
                    <v-card-item>
                        <div>
                            <div class="text-h6 mb-1">
                                {{ subject.name_subject }} | {{ subject.term }}/{{ subject.year }}
                            </div>
                            <div class="text-caption">{{ subject.id_subject }}</div>
                        </div>
                    </v-card-item>

                    <v-card-actions>
                        <v-btn @click="editSubject">
                            <v-icon>mdi-pen</v-icon>
                            Edit
                        </v-btn>
                        <v-btn>
                            <v-icon>mdi-trash-can-outline</v-icon>
                            Delete
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
            <div class="mx-4">
                <v-btn height="130" color="indigo-lighten-4" @click="dialogCreateSubj = true">
                    <v-icon>mdi-plus-circle-outline</v-icon>
                </v-btn>


                <v-dialog v-model="dialogCreateSubj" width="auto">
                    <v-card width="600" prepend-icon="mdi-folder-plus-outline" title="Create Subject">
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col>
                                        <v-text-field label="Year" v-model="year"></v-text-field>
                                    </v-col>
                                    <v-col>
                                        <v-text-field label="Term" v-model="term"></v-text-field>
                                    </v-col>

                                </v-row>
                                <v-row>
                                    <v-col>
                                        <v-text-field label="ID Subject" v-model="id_subject"></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <v-col>
                                        <v-text-field label="Subject" v-model="subjectName"></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="error" variant="text" @click="cancel"> Cancel </v-btn>
                            <v-btn color="blue-darken-1" variant="text" @click="add_subject"> Save </v-btn>
                        </v-card-actions>
                    </v-card>

                </v-dialog>

                <v-dialog v-model="dialogEditSubj" width="auto">
                    <v-card width="600" prepend-icon="mdi-folder-plus-outline" title="Edit Subject">
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col>
                                        <v-text-field label="Year" v-model="year" :placeholder="selectedSubject.year"></v-text-field>
                                    </v-col>
                                    <v-col>
                                        <v-text-field label="Term" v-model="term" :placeholder="selectedSubject.term"></v-text-field>
                                    </v-col>

                                </v-row>
                                <v-row>
                                    <v-col>
                                        <v-text-field label="ID Subject" v-model="id_subject" :placeholder="selectedSubject.id_subject"></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-row>
                                    <v-col>
                                        <v-text-field label="Subject" v-model="subjectName" :placeholder="selectedSubject.subjectName"></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="error" variant="text" @click="cancelEdit"> Cancel </v-btn>
                            <v-btn color="blue-darken-1" variant="text" @click="add_subject"> Save </v-btn>
                        </v-card-actions>
                    </v-card>

                </v-dialog>
            </div>

        </v-row>
    </v-container>
</template> -->

<script>
  import axios from 'axios'

  export default {
  name: 'subjectView',
  data() {
    return {
      subject: {
        name_subject: '',
        id_subject: '',
        year: '',
        term: null,
      }
    };
  },
    methods: {
      async submitSubject() {
        const username = localStorage.getItem('Username');
        try {
            const formData = new FormData();
            formData.append('name_subject', this.subject.name_subject);
            formData.append('id_subject', this.subject.id_subject);
            formData.append('year', this.subject.year);
            formData.append('term', this.subject.term);
            const response = await axios.post(`http://localhost/api/createSubject.php?username=${username}`, formData);
            console.log("data:");
            console.log(response.data);

            if (response.data.success) {
                // แสดงข้อความคำตอบจาก API ในรูปแบบของ pop-up
                alert('subject created successfully');
            } else {
                alert('An error occurred while submitting the subject. Please try again later.');
            }
        } catch (error) {
            console.error('There was an error submitting the subject:', error);
            alert('An error occurred while submitting the subject. Please try again later.');
        }
      }  
    }
};
</script>

<style scoped>
.create-subject-view {
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
.form-group select { /* เพิ่มเลือกเข้ามาในการปรับแต่ง */
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button[type="submit"] {
  background-color: #007bff; /* เปลี่ยนเป็นสีฟ้า */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0056b3; /* เปลี่ยนสีเมื่อโฮเวอร์ */
}
</style>

<template>
    <div class="create-subject-view">
      <h1>Create subject</h1>
      <form @submit.prevent="submitSubject">
  
        <div class="form-group">
          <label for="nameSubject">Subject Name:</label>
          <input type="text" id="nameSubject" v-model="subject.name_subject" required>
        </div>
  
        <div class="form-group">
          <label for="idSubject">ID Subject:</label>
          <input type="text" id="idSubject" v-model.number="subject.id_subject" required>
        </div>

        <div class="form-group">
          <label for="year">Year:</label>
          <input type="text" id="year" v-model.number="subject.year" required>
        </div>

        <div class="form-group">
          <label for="term">Term:</label>
          <input type="text" id="term" v-model.number="subject.term" required>
        </div>
  
        <button type="submit">Submit</button>
      </form>
    </div>
</template>