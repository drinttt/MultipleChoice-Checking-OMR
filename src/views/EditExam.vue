<script setup>
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useExamStore } from '@/stores/exam';
import axios from 'axios';

const route = useRoute();
const examStore = useExamStore();

// const id_exam = route.params.id_exam

const form = ref({
    id_exam: route.params.id_exam,
    name_exam: '',
    qty_exam: null,
});


// onMounted(async () => {
//     const examData = await examStore.fetchSubjectByCode(form.value.id_exam);
//     if (examData && examData.length > 0) {
//         form.value = { ...examData[0] };
//     }
// });
onMounted(async () => {
    const examData = await examStore.fetchUserExamByCode(form.value.id_exam);
    if (examData && examData.length > 0) {
        form.value = { ...examData[0] };
    }
});




const saveChanges = async () => {
    // ตรวจสอบว่าค่าที่จำเป็นสำหรับการอัพเดทรายวิชาถูกกำหนดค่าหรือไม่
    if (
        form.value.name_exam &&
        form.value.qty_exam &&
        form.value.id_exam
    ) {
        const formData = new FormData();
        formData.append('name_exam', form.value.name_exam);
        formData.append('qty_exam', form.value.qty_exam);
        formData.append('id_exam', form.value.id_exam);

        try {
            const response = await axios.post('http://localhost/api/update_exam.php', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response.data);
            // ดำเนินการต่อเช่น เปลี่ยนเส้นทางผู้ใช้หรือแสดงข้อความยืนยัน
        } catch (error) {
            console.error('Error updating subject:', error);
            // แสดงข้อความแจ้งเตือนให้ผู้ใช้ทราบว่ามีข้อผิดพลาด
        }

    alert("แก้ไขเรียบร้อย")
    } else {
        console.error('Incomplete Data.');
    }
};

function goBack() {
    // คำสั่งนี้จะทำให้ browser ย้อนกลับไปยังหน้าก่อนหน้า
    history.back()
}

</script>

<template>
    <v-container>
        <v-row class="mt-4 mb-6">
            <v-col cols="1">
                <v-btn @click="goBack">
                    <v-icon>mdi-arrow-left</v-icon>
                </v-btn>
            </v-col>
            <v-col class="mt-10">
                <h1>Edit Exam</h1>
                <v-row class="mt-6 mx-8">
                    <v-col cols="8">
                        <v-form @submit.prevent="saveChanges">
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.id_exam" name="id_exam" label="ID Exam"
                                        readonly></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.name_exam" name="name_exam"
                                        label="Exam Name"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field v-model="form.qty_exam" name="qty_exam"
                                        label="Number of exam questions"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-btn color="primary" type="submit">Save</v-btn>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>
<!-- 
<template>
    <div>
        {{ id_exam }}
      <h1>Exam Details</h1>
      <div v-if="exam">
        <p>ID: {{ exam.id_exam }}</p>
        <p>Name: {{ exam.name_exam }}</p>
        <p>Number of Questions: {{ exam.qty_exam }}</p>
      </div>
      <div v-else>
        <p>Loading exam details...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import axios from 'axios';
  
  const exam = ref(null);
  const route = useRoute();
  const id_exam = route.params.id_exam;
  
  onMounted(async () => {
    // const id_exam = route.params.id_exam;
    if (id_exam) {
      try {
        const response = await axios.get(`http://localhost/api/id_exam.php?id_exam=${id_exam}`);
        exam.value = response.data;
      } catch (error) {
        console.error('Error fetching exam:', error);
      }
    }
  });
  </script> -->
  