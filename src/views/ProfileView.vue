<script setup>
import { ref, onMounted } from 'vue';
import { useUserProfileStore } from '@/stores/profile'
import axios from 'axios';

const userStore = useUserProfileStore()


const form = ref({
    name: '',
    surname: '',
    email: '',
    password: '',
    username: userStore.userProfile.username,
});

onMounted(async () => {
    const userData = await userStore.fetchUserByCode(form.value.username);
    if (userData && userData.length > 0) {
        form.value = { ...userData[0] };
    }
    console.log(form.value)
});

const saveChanges = async () => {
    if (
        form.value.name &&
        form.value.surname &&
        form.value.email &&
        form.value.password &&
        form.value.username
    ) {
        const formData = new FormData();
        formData.append('name', form.value.name);
        formData.append('surname', form.value.surname);
        formData.append('email', form.value.email);
        formData.append('password', form.value.password);
        formData.append('username', form.value.username);

        console.log(form.value.name)
        console.log(formData)
        // console.log(formData.entries())

        // const data = {
        //     name: form.value.name,
        //     surname: form.value.surname,
        //     email: form.value.email,
        //     password: form.value.password,
        //     username: form.value.username
        // };
        // console.log(data)

        try {

            const response = await axios.post('http://localhost/api/update_user.php', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    // 'Content-Type': 'application/json',
                },
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error updating subject:', error);
        }

        alert("แก้ไขเรียบร้อย")
    } else {
        console.error('Incomplete Data.');
    }
}
// else {
//     console.error('Incomplete Data.');
//     }
// };

function goBack() {
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