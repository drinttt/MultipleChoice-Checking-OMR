<script setup>
import { onMounted, ref, computed } from 'vue';
import { useUserProfileStore } from '@/stores/profile'
import axios from 'axios';

const userStore = useUserProfileStore();

const form = ref({
    name: '',
    surname: '',
    email: '',
    password: '',
    username: '',
});

const username = computed(() => userStore.userProfile.username);

onMounted(async () => {
    await userStore.fetchUserByCode(username.value);
    form.value = { ...userStore.userProfile };
});

const saveChanges = async () => {
    // ตรวจสอบข้อมูลว่างเปล่าก่อนส่งไปยัง API
    if (
        !form.value.name ||
        !form.value.surname ||
        !form.value.email ||
        !form.value.password ||
        !form.value.username
    ) {
        console.error('Incomplete Data.');
        return; // หยุดการทำงานหากข้อมูลไม่สมบูรณ์
    }

    const data = {
        ...form.value,
        username: username.value,
    };
    console.log(data);

    try {
        const response = await axios.post('http://localhost/api/editUserData.php', data);
        console.log(response.data);
        alert('แก้ไขข้อมูลเรียบร้อยแล้ว');
    } catch (error) {
        console.error('Error updating user profile:', error);
    }
}


function goBack() {
    history.back();
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
                <h1>Edit Profile</h1>
                <v-row class="mt-6 mx-8">
                    <v-col cols="8">
                        <v-form @submit.prevent="saveChanges">
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.username" name="username" label="ID Exam"
                                        readonly></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.name" name="name" label="Name"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field v-model="form.surname" name="surname" label="Surname"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field v-model="form.email" name="email" label="Email"></v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field v-model="form.password" name="password"
                                        label="Password"></v-text-field>
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
