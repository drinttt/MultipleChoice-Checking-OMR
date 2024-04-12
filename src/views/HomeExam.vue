<script setup>
import { ref, onMounted, } from 'vue';
import { useSubjectStore } from '@/stores/subject';
import { useExamStore } from '@/stores/exam';
import { useUserProfileStore } from '@/stores/profile';
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios';
;

const router = useRouter();

const route = useRoute();
const code_subject = route.params.code_subject;

const userStore = useUserProfileStore();
const examStore = useExamStore();
const subjectStore = useSubjectStore();

onMounted(() => {
    userStore.fetchUserProfile();
    // subjectStore.fetchUserSubject();
    subjectStore.fetchSubjectByCode(code_subject);

    examStore.fetchUserExam(code_subject);
});

const color = ref('yellow')



// edit

const editSubject = (exam) => {
    // Object.assign(selectedSubject, {...subject});
    // dialogEditSubj.value = true;
    // console.log(subject.code_subject)
    router.push({ name: 'EditExam', params: { id_exam: exam.id_exam } });
};

function goBack() {
    // คำสั่งนี้จะทำให้ browser ย้อนกลับไปยังหน้าก่อนหน้า
    window.location.href = document.referrer;
}

const deleteExam = async (id_exam) => {
    if (confirm('Are you sure you want to delete this exam?')) {
        try {
            // // ลบข้อมูลนักศึกษาเก่าจากตาราง student_answer
            // await axios.post("http://localhost/api/deleteStudentAnswersByExam.php", { id_exam: id_exam });

            // // ลบข้อมูลนักศึกษาเก่าจากตาราง student
            // await axios.post("http://localhost/api/deleteStudentsByExam.php", { id_exam: id_exam });
            // ลบข้อสอบ
            // await axios.post("http://localhost/api/deleteExam.php", { id_exam: id_exam });

            axios.post("http://localhost/api/deleteExam.php", { id_exam: id_exam })
                .then(response => {
                    console.log('Exam deleted successfully:', response.data);
                    // ทำสิ่งที่คุณต้องการหลังจากลบข้อมูลอย่างสำเร็จ
                })
                .catch(error => {
                    console.error('Error deleting exam:', error);
                    // จัดการข้อผิดพลาดที่เกิดขึ้น
                });

            // subjectStore.fetchUserSubject()
        } catch (error) {
            console.error('Error deleting exam:', error);
        }
    }
    goBack()
};


const toExamDetail = (id_exam) => {
    router.push({ name: 'DetailOverall', params: { id_exam } });
};

</script>


<template>
    <v-container>
        <!-- ข้อสอบของวิชา {{ useSubjectStore.year }} -->
        <div v-if="examStore.userExam.length > 0">

            <v-row align="center" class="mx-0">
                <!-- ใช้ v-for วนลูปข้อมูลวิชาทั้งหมดจาก store -->
                <!-- <div v-if="examStore.userExam.length > 0"> -->
                <v-col v-for="exam in examStore.userExam" :key="exam.id" cols="3">
                    <v-card :color="color" @click="toExamDetail(exam.id_exam)" class="mx-auto" max-width="250">
                        <v-card-item>
                            <div>
                                <div class="text-h6 mb-1">
                                    {{ exam.name_exam }}
                                </div>
                                <div class="text-caption">จำนวน {{ exam.qty_exam }} ข้อ</div>
                                <!-- {{ subject.code_subject }} -->
                            </div>
                        </v-card-item>

                        <v-card-actions>
                            <v-btn @click.stop="editSubject(exam)">
                                <v-icon>mdi-pen</v-icon>
                                Edit
                            </v-btn>
                            <v-btn @click="deleteExam(exam.id_exam)">
                                <v-icon>mdi-trash-can-outline</v-icon>
                                Delete
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <!-- </div> -->

                <!-- <v-card :color="color" class="mx-0" max-width="400" height="130"> -->
                <!-- <v-card-actions> -->

                <!-- </v-card-actions> -->
                <!-- </v-card> -->

            </v-row>
        </div>
    </v-container>
</template>