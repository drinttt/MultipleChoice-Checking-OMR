<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import * as XLSX from 'xlsx';


const route = useRoute();
const router = useRouter();
const id_exam = route.params.id_exam;


const selectedSection = ref("All"); // ตัวแปรสำหรับเก็บ Section ที่เลือก
const sections = ref(["All"]); // ตัวแปรสำหรับเก็บรายการ Sections


const editedItem = ref({});
const editDialog = ref(false);
const editedScore = ref(0);

const examDetails = ref([]);
const headers = ref([
  { title: 'No.', value: 'no_student' },
  { title: 'Student ID', value: 'id_student' },
  { title: 'Student Name', value: 'st_name' },
  // { title: 'Section', value: 'section' },
  { title: 'Totol Score', value: 'total_score' },
  { text: 'Actions', value: 'action', sortable: false },

]);

const fetchData = async () => {
  try {
    const response = await axios.get(`http://localhost/api/getExamDetailTable.php?id_exam=${id_exam}`);
    examDetails.value = response.data;
    // กำหนด sections โดยไม่ต้องใช้ forEach
    sections.value = ["All", ...new Set(response.data.map(item => item.section))];
  } catch (error) {
    console.error('เกิดข้อผิดพลาดในการดึงข้อมูลรายละเอียดการสอบ:', error);
  }
};

onMounted(() => {
  fetchData(); 
});


const filteredDetails = computed(() => {
  return selectedSection.value === "All"
    ? examDetails.value
    : examDetails.value.filter((detail) => detail.section === selectedSection.value);
});

// eslint-disable-next-line no-unused-vars
const filterBySection = () => {
  if (!selectedSection.value) {
    return examDetails.value;
  }
  return examDetails.value.filter(detail => detail.section === selectedSection.value);
};



const MoreItem = (item) => {
  console.log('More options for:', item.id_exam, item.id_student);
  router.push({ name: 'StudentAnswer', params: { id_exam: item.id_exam, id_student: item.id_student } });
};

const exportToExcel = () => {
  const ws = XLSX.utils.json_to_sheet(filteredDetails.value.map(item => ({
    'No.': item.no_student,
    'Student ID': item.id_student,
    'Student Name': item.st_name,
    'Total Score': item.total_score,
  })));
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Exam Details");
  XLSX.writeFile(wb, "exam_details.xlsx");
};


const openEditDialog = (item) => {
  editedItem.value = { ...item };
  editedScore.value = item.total_score; 
  editDialog.value = true;
};

const saveScore = async () => {
  const updatedItem = { ...editedItem.value, total_score: editedScore.value };
  try {
    await axios.post('http://localhost/api/editStudentScore.php', updatedItem);
    editDialog.value = false;
    
    fetchData();
  } catch (error) {
    console.error("Error updating score:", error);
  }
};
</script>



<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 v-if="examDetails.length > 0">รายวิชา: {{ examDetails[0].name_subject }} - {{ examDetails[0].name_exam }}
        </h1>
      </v-col>
      <!-- <v-col>
        <h1 v-if="examDetails.length > 0">ชุดข้อสอบ: {{ examDetails[0].name_exam }}</h1>
      </v-col> -->
    </v-row>

    <v-row>
      <v-col cols="4">
        <!-- <v-select v-model="selectedSection" :items="sections" label="Select Section"
          @change="filterBySection"></v-select> -->
      </v-col>
      <v-col cols="6">

      </v-col>
      <v-col cols="2">
        <v-btn color="blue" @click="exportToExcel">Export Excel</v-btn>
      </v-col>

      <!-- <v-col cols="4">
        <v-select v-model="selectedSection" :items="sections" label="Select Section"
          @change="filterBySection"></v-select>
      </v-col> -->
    </v-row>

    <!-- <h1>Exam Detail: {{ id_exam }}</h1> -->
    <v-data-table :headers="headers" :items="filteredDetails" :items-per-page="10" class="elevation-1">

      <template v-slot:[`item.action`]="{ item }">
        <v-container>
          <v-icon small class="mr-2" @click="openEditDialog(item)">
            mdi-pencil
          </v-icon>
          <!-- <v-icon small class="mr-2" @click="deleteItem(item)">
            mdi-delete
          </v-icon> -->
          <v-icon small class="ml-2" @click="MoreItem(item)">
            mdi-dots-vertical
          </v-icon>
        </v-container>
      </template>

    </v-data-table>

    <!-- Dialog for editing score -->
    <v-dialog v-model="editDialog" persistent max-width="290">
      <v-card>
        <v-card-title class="text-h5">แก้ไขคะแนน</v-card-title>
        <v-card-text>
          <v-text-field v-model="editedScore" label="คะแนน" type="number"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="saveScore(item)">บันทึก</v-btn>
          <v-btn color="red darken-1" text @click="editDialog = false">ยกเลิก</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>