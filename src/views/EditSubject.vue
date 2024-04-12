<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useSubjectStore } from '@/stores/subject';
import axios from 'axios';

const route = useRoute();
const subjectStore = useSubjectStore();
const form = ref({
    name_subject: '',
    code_subject: route.params.code_subject, // เข้าถึงตัวแปร route โดยตรง
    year: null,
    term: null,
    id_subject: null,
});

onMounted(async () => {
    const subjectData = await subjectStore.fetchSubjectByCode(form.value.code_subject);
    if (subjectData && subjectData.length > 0) {
        form.value = { ...subjectData[0] };
    }
});

const saveChanges = async () => {
    // ตรวจสอบว่าค่าที่จำเป็นสำหรับการอัพเดทรายวิชาถูกกำหนดค่าหรือไม่
    if (
        form.value.name_subject &&
        form.value.year &&
        form.value.term &&
        form.value.id_subject &&
        form.value.code_subject
    ) {
        const formData = new FormData();
        formData.append('name_subject', form.value.name_subject);
        formData.append('year', form.value.year);
        formData.append('term', form.value.term);
        formData.append('id_subject', form.value.id_subject);
        formData.append('code_subject', form.value.code_subject);

        try {
            const response = await axios.post('http://localhost/api/update_subject.php', formData, {
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
                <h1>Edit Subject</h1>
                <v-row class="mt-6 mx-8">
                    <v-col cols="8">
                        <v-form @submit.prevent="saveChanges">

                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.code_subject" name="code_subject" label="code_subject" readonly></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.year" name="year" label="Year"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field v-model="form.term" name="term" label="Term"></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row class="mt-0">
                                <v-col>
                                        <v-text-field v-model="form.id_subject" name="id_subject" label="ID Subject"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row class="mt-0">
                                <v-col>
                                        <v-text-field v-model="form.name_subject" name="name_subject"
                                            label="Subject Name" id="id"></v-text-field>
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