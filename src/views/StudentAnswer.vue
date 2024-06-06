<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute, } from 'vue-router';
// import * as XLSX from 'xlsx';


const route = useRoute();

const editDialog = ref(false);
// const editDialogKey = ref(false);
const editedItem = ref({});
// const editedItemKey = ref({});
const editedAns = ref(0);
// const editedAnsKey = ref(0);


// const router = useRouter();
const id_exam = route.params.id_exam;
const id_student = route.params.id_student;

const AnsDetails = ref([]);
const keys = ref([]);

const selectedSection = ref("All");
const selectedKey = ref("All");
const studentImage = ref('');

const headers = ref([
    { title: 'No.', value: 'no_student_answer' },
    { title: 'Student Answer', value: 'student_answer' },
    { text: 'Actions', value: 'action', sortable: false },
]);

const headersKey = ref([
    { title: 'No.', value: 'no_answer_key' },
    { title: 'Answer Key', value: 'answer_key' },
    // { text: 'Actions', value: 'action', sortable: false },
]);

const fetchData = async () => {
    try {
        const response = await axios.get(`http://localhost/api/getStdAnsTable.php?id_exam=${id_exam}&id_student=${id_student}`);
        AnsDetails.value = response.data;
        // console.log(AnsDetails.value)

        const imgResponse = await axios.get(`http://localhost/api/showImgStd.php?id_exam=${id_exam}&id_student=${id_student}`);
        // studentImage.value = imgResponse.data; // สมมติว่า API ส่งกลับ URL รูปภาพ
        if (imgResponse.data && imgResponse.data.url) {
            studentImage.value = imgResponse.data.url; // กำหนด URL รูปภาพ
        }

        const responseKey = await axios.get(`http://localhost/api/getAnsKey.php?id_exam=${id_exam}`);
        keys.value = responseKey.data;
    } catch (error) {
        filteredDetails
        console.error('เกิดข้อผิดพลาดในการดึงข้อมูลรายละเอียดการสอบ:', error);
    }
};

onMounted(() => {
    fetchData(); // เรียกใช้ fetchData เพื่อโหลดข้อมูลแรกเริ่ม
});

const openEditDialog = (item) => {
    editedItem.value = { ...item };
    editedAns.value = item.student_answer; // ตั้งค่าคะแนนเริ่มต้นให้กับแบบฟอร์ม
    editDialog.value = true; // เปิดไดอะล็อก
};
// const openEditDialogKey = (item) => {
//     editedItemKey.value = { ...item };
//     editedAnsKey.value = item.answer_key; // ตั้งค่าคะแนนเริ่มต้นให้กับแบบฟอร์ม
//     editDialogKey.value = true; // เปิดไดอะล็อก
// };


const saveAns = async () => {
    const updatedItem = { ...editedItem.value, student_answer: editedAns.value };
    try {
        await axios.post('http://localhost/api/editStudentAns.php', updatedItem);
        editDialog.value = false;
        fetchData();
    } catch (error) {
        console.error("Error updating score:", error);
    }
};

// const saveAnsKey = async () => {
//     const updatedItemKey = { ...editedItemKey.value, answer_key: editedAnsKey.value };
//     try {
//         await axios.post('http://localhost/api/editAnsKey.php', updatedItemKey);
//         editDialogKey.value = false; 
//         fetchData();
//     } catch (error) {
//         console.error("Error updating score:", error);
//     }
// };

const filteredDetails = computed(() => {
    return selectedSection.value === "All"
        ? AnsDetails.value
        : AnsDetails.value.filter((detail) => detail.section === selectedSection.value);
});

const filteredKey = computed(() => {
    return selectedKey.value === "All"
        ? keys.value
        : keys.value.filter((detail) => detail.section === selectedKey.value);
});




</script>



<template>
    <v-container>
        <v-row>
            <v-col>
                <!-- <h1>ชื่อ: -->
                <h1 v-if="AnsDetails.length > 0">{{ AnsDetails[0].st_name }} ( {{ AnsDetails[0].id_student }} )
                </h1>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="7">
                <img v-if="studentImage" :src="studentImage" alt="Student Image" style="width: 600px; height: auto;" />
            </v-col>
            <!-- <v-col cols="2"></v-col> -->
            <v-col cols="2" class="mt-14">
                <v-row class="mt-14 mr-0">
                    <v-data-table :headers="headersKey" :items="filteredKey" :items-per-page="10" class="elevation-1">
                        <template v-slot:[`item.action`]="{ item }">
                            <v-icon small class="mr-2" @click="openEditDialogKey(item)">
                                mdi-pencil
                            </v-icon>
                        </template>
                    </v-data-table>
                </v-row>
            </v-col>
            <v-col cols="1.5" class="mt-14">
                <v-row class="mt-14">
                    <v-data-table :headers="headers" :items="filteredDetails" :items-per-page="10" class="elevation-1">
                        <template v-slot:[`item.action`]="{ item }">
                            <v-icon small class="mr-2" @click="openEditDialog(item)">
                                mdi-pencil
                            </v-icon>
                        </template>
                    </v-data-table>
                </v-row>
            </v-col>
        </v-row>

        <!-- Dialog for editing score -->
        <v-dialog v-model="editDialog" persistent max-width="290">
            <v-card>
                <v-card-title class="text-h5">แก้ไขคำตอบ</v-card-title>
                <v-card-text>
                    <v-text-field v-model="editedAns" label="คำตอบ" type="text"></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="saveAns(item)">บันทึก</v-btn>
                    <v-btn color="red darken-1" text @click="editDialog = false">ยกเลิก</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- <v-dialog v-model="editDialogKey" persistent max-width="290">
            <v-card>
                <v-card-title class="text-h5">แก้ไขเฉลย</v-card-title>
                <v-card-text>
                    <v-text-field v-model="editedAnsKey" label="คำตอบ" type="text"></v-text-field>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" text @click="saveAnsKey(item)">บันทึก</v-btn>
                    <v-btn color="red darken-1" text @click="editDialogKey = false">ยกเลิก</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog> -->
    </v-container>
</template>