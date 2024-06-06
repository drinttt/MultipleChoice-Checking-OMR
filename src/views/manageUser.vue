<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const editDialog = ref(false);
const editedItem = ref({});
// const editedAns = ref(0);


const users = ref([]);
const selected = ref("All");
// const studentImage = ref('');

const headers = ref([
  { title: 'Username', value: 'username' },
  { title: 'Name', value: 'name' },
  { title: 'Surname', value: 'surname' },
  { title: 'Email', value: 'email' },
  { title: 'Password', value: 'password' },
  { text: 'Actions', value: 'action', sortable: false },
]);

const fetchData = async () => {
  try {
    const response = await axios.get(`http://localhost/api/getUserData.php`);
    users.value = response.data;
  } catch (error) {
    console.error('เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้งาน:', error);
  }
};

onMounted(() => {
  fetchData(); // เรียกใช้ fetchData เพื่อโหลดข้อมูลแรกเริ่ม
});

const openEditDialog = (item) => {
  editedItem.value = { ...item };
  // editedAns.username.value = item.username; // ตั้งค่าคะแนนเริ่มต้นให้กับแบบฟอร์ม
  editDialog.value = true; // เปิดไดอะล็อก
};

const saveAns = async () => {
  // const updatedItem = { ...editedItem.value, student_answer: editedAns.value };
  try {
    await axios.post('http://localhost/api/editUserData.php', editedItem.value);
    editDialog.value = false;
    fetchData();
  } catch (error) {
    console.error("Error updating score:", error);
  }
};

const filteredDetails = computed(() => {
  return selected.value === "All"
    ? users.value
    : users.value.filter((detail) => detail.section === selected.value);
});


const deleteItem = async (item) => {
  // ถามผู้ใช้เพื่อยืนยันการลบ
  if (confirm(`คุณต้องการลบข้อมูลนักศึกษา ${item.username} หรือไม่?`)) {
    try {
      await axios.post('http://localhost/api/deleteUser.php', { username: item.username });
      // ลบรายการนั้นออกจาก examDetails
      users.value = users.value.filter(d => d.username !== item.username);
      // แสดง alert หลังจากลบข้อมูลสำเร็จ
      alert('นักศึกษาถูกลบเรียบร้อยแล้ว');
      console.log(item.username)
    } catch (error) {
      console.error('เกิดข้อผิดพลาดในการลบนักศึกษา:', error);
      // แสดง alert หากมีข้อผิดพลาด
      alert('เกิดข้อผิดพลาดในการลบนักศึกษา');
    }
  }
};

</script>



<template>
  <v-container>
    <v-row class="mb-5">
      <v-col>
        <h1>จัดการบัญชีผู้ใช้งาน</h1>
      </v-col>
    </v-row>
    <v-data-table :headers="headers" :items="filteredDetails" :items-per-page="10" class="elevation-1">

      <template v-slot:[`item.action`]="{ item }">
        <v-container>
          <v-icon small class="mr-2" @click="openEditDialog(item)">
            mdi-pencil
          </v-icon>
          <v-icon small class="mr-2" @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </v-container>
      </template>

    </v-data-table>

    <v-dialog v-model="editDialog" persistent max-width="500">
      <v-card>
        <v-card-title class="text-h5">แก้ไขข้อมูลบัญชีผู้ใช้งาน</v-card-title>
        <v-card-text>
          <v-row>
            <v-col>
              <v-text-field v-model="editedItem.username" label="Username" type="text" readonly></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field v-model="editedItem.name" label="Name" type="text"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field v-model="editedItem.surname" label="Surname" type="text"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field v-model="editedItem.email" label="Email" type="text"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field v-model="editedItem.password" label="Password" type="text"></v-text-field>
            </v-col>
          </v-row>
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