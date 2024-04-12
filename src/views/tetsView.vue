<!-- <template>
  <div>
    <input v-model.number="num1" type="number" placeholder="Number 1">
    <input v-model.number="num2" type="number" placeholder="Number 2">
    <v-btn @click="addNumbers">Add</v-btn>
    <div v-if="result !== null">Result: {{ result }}</div>
    <div v-if="errorMsg">{{ errorMsg }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const num1 = ref(0);
const num2 = ref(0);
const result = ref(null);
const errorMsg = ref('');

const addNumbers = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/add', {
      num1: num1.value,
      num2: num2.value
    });
    result.value = response.data.result;
    errorMsg.value = '';  // ล้างข้อความแจ้งเตือนหากการคำนวณสำเร็จ
  } catch (error) {
    console.error('Error adding numbers:', error);
    result.value = null;  // ล้างผลลัพธ์หากเกิดข้อผิดพลาด
    errorMsg.value = 'Error adding numbers. Please try again.';  // แสดงข้อความแจ้งเตือนเมื่อเกิดข้อผิดพลาด
  }
};
</script>

<style>
/* สามารถเพิ่มสไตล์ที่นี่หากจำเป็น */
</style> -->


<!-- <template>
  <div>
    <input type="file" @change="onFileChange">
    <v-btn @click="uploadImage">Upload Image</v-btn>
    <div v-if="imageInfo">
      <p>Width: {{ imageInfo.width }}</p>
      <p>Height: {{ imageInfo.height }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      imageInfo: null
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    uploadImage() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      axios.post('http://localhost:5000/upload-image', formData)
        .then(response => {
          this.imageInfo = response.data;
        })
        .catch(error => {
          console.error('Error uploading image:', error);
        });
    }
  }
};
</script> -->

<template>
  <div>
    <input type="file" @change="onFileChange">
    <button @click="uploadAndConvert">Upload and Convert</button>
    <div v-if="convertedImageUrl">
      <img :src="convertedImageUrl" alt="Converted Image">
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      convertedImageUrl: null,
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    uploadAndConvert() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      
      axios.post('http://localhost:5000/upload-and-convert', formData, {
        responseType: 'blob', // สำคัญเพื่อรับไฟล์ภาพกลับมา
      })
      .then(response => {
        // สร้าง URL จาก blob เพื่อแสดงภาพ
        const url = window.URL.createObjectURL(new Blob([response.data]));
        this.convertedImageUrl = url;
      })
      .catch(error => {
        console.error('Error uploading and converting image:', error);
      });
    },
  },
};
</script>



