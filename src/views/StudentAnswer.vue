<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute, } from 'vue-router';
// import * as XLSX from 'xlsx';


const route = useRoute();

const editDialog = ref(false);
const editedItem = ref({});
const editedAns = ref(0);


// const router = useRouter();
const id_exam = route.params.id_exam; // รับค่า id_exam จาก route parameters
const id_student = route.params.id_student;

const AnsDetails = ref([]);
const selectedSection = ref("All"); // ตัวแปรสำหรับเก็บ Section ที่เลือก
const studentImage = ref('');

const headers = ref([
    { title: 'No.', value: 'no_student_answer' },
    { title: 'Answer', value: 'student_answer' },
    { text: 'Actions', value: 'action', sortable: false },
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

const saveAns = async () => {
  const updatedItem = { ...editedItem.value, student_answer: editedAns.value };
  try {
    await axios.post('http://localhost/api/editStudentAns.php', updatedItem);
    editDialog.value = false; // ปิดไดอะล็อกหลังจากแก้ไขสำเร็จ
    // รีโหลดข้อมูลตารางหรืออัพเดท UI หากจำเป็น
    fetchData();
  } catch (error) {
    console.error("Error updating score:", error);
  }
};

const filteredDetails = computed(() => {
    return selectedSection.value === "All"
        ? AnsDetails.value
        : AnsDetails.value.filter((detail) => detail.section === selectedSection.value);
});


// const exportToExcel = () => {
//   const ws = XLSX.utils.json_to_sheet(filteredDetails.value.map(item => ({
//     'no': item.id_student,
//     'answer': item.st_name,
//     'Section': item.section,
//     'Total Score': item.total_score,
//     // คุณสามารถเพิ่มหรือลบฟิลด์ได้ตามต้องการ
//   })));
//   const wb = XLSX.utils.book_new();
//   XLSX.utils.book_append_sheet(wb, ws, "Exam Details");
//   XLSX.writeFile(wb, "exam_details.xlsx");
// };


// const openEditDialog = (item) => {
//   editedItem.value = { ...item };
//   editedScore.value = item.total_score; // ตั้งค่าคะแนนเริ่มต้นให้กับแบบฟอร์ม
//   editDialog.value = true; // เปิดไดอะล็อก
// };



// const deleteItem = async (item) => {
//   // ถามผู้ใช้เพื่อยืนยันการลบ
//   if (confirm(`คุณต้องการลบข้อมูลนักศึกษา ${item.id_student} หรือไม่?`)) {
//     try {
//       await axios.post('http://localhost/api/deleteStudent.php', { id_exam: item.id_exam, id_student: item.id_student });
//       // ลบรายการนั้นออกจาก examDetails
//       examDetails.value = examDetails.value.filter(d => d.id_student !== item.id_student);
//       // แสดง alert หลังจากลบข้อมูลสำเร็จ
//       alert('นักศึกษาถูกลบเรียบร้อยแล้ว');
//       console.log(item.id_student)
//     } catch (error) {
//       console.error('เกิดข้อผิดพลาดในการลบนักศึกษา:', error);
//       // แสดง alert หากมีข้อผิดพลาด
//       alert('เกิดข้อผิดพลาดในการลบนักศึกษา');
//     }
//   }
// };




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
            <!-- <v-col cols="4">
        <v-select v-model="selectedSection" :items="sections" label="Select Section"
          @change="filterBySection"></v-select>
      </v-col> -->
            <!-- <v-col cols="2">
        <v-btn color="blue" @click="exportToExcel">Export Excel</v-btn>
      </v-col> -->

            <!-- <v-col cols="4">
        <v-select v-model="selectedSection" :items="sections" label="Select Section"
          @change="filterBySection"></v-select>
      </v-col> -->
        </v-row>


        <v-row>
            <v-col cols="7">
                <img v-if="studentImage" :src="studentImage" alt="Student Image"  style="width: 600px; height: auto;" />
            </v-col>
            <!-- <v-col cols="2"></v-col> -->
            <v-col cols="4" class="mt-14">
                <v-row class="mt-14">
                <v-data-table :headers="headers" :items="filteredDetails" :items-per-page="10" class="elevation-1">

                    <template v-slot:[`item.action`]="{ item }">
                        <v-container>
                            <v-icon small class="mr-2" @click="openEditDialog(item)">
                                mdi-pencil
                            </v-icon>
                        </v-container>
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
    </v-container>
</template>