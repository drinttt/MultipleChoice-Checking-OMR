<script>
import axios from 'axios';

export default {
    data() {
        return {
            user: {
                username: '',
                password: '',
                name: '',
                surname: '',
                email: ''
            },
            usernameExists: false, 
        }
    },
    watch: {
        // Watch for changes in the username and call checkUsername method
        'user.username'(newUsername) {
            this.usernameExists = false;
            if (newUsername) {
                this.checkUsername(newUsername);
            }
        }
    },
    methods: {
        async checkUsername(username) {
            try {
                const response = await axios.get(`http://localhost/api/checkUsername.php?username=${username}`);
                this.usernameExists = response.data.exists; // Set based on API response
            } catch (error) {
                console.error('Error checking username:', error);
                this.usernameExists = false; // Assume username does not exist if there is an error
            }
        },
        async submitForm() {
            // if (this.usernameExists) {
            //     alert('Username already taken. Please choose a different one.');
            //     return; // Prevent form submission if username exists
            // }
            if (!this.user.username || !this.user.password || !this.user.name || !this.user.surname || !this.user.email) {
                alert('Please fill in all required fields.');
                return;
            }

            if (this.usernameExists) {
                alert('Username already taken. Please choose a different one.');
                return; // หยุดการส่งข้อมูลหาก username ซ้ำกับที่มีอยู่แล้ว
            }

            try {
                const formData = new FormData();
                formData.append('username', this.user.username);
                formData.append('password', this.user.password);
                formData.append('name', this.user.name);
                formData.append('surname', this.user.surname);
                formData.append('email', this.user.email);

                const response = await axios.post('http://localhost/api/Register.php', formData);
                console.log(response.data);

                if (response.data.success) {
                    alert('Registration successful');
                    this.$router.push('/login');
                } else {
                    alert('This Username is already in use.');
                }
            } catch (error) {
                console.error('Error registering:', error);
                alert('An error occurred while registering. Please try again later1.');
            }
        }
    }
}
</script>


<template>
    <v-app>
        <v-container class="my=0 py-0">
            <v-row justify="center" class="no-gutters setFont" style="padding-top: 0vh">
                <v-col cols="6">
                    <img alt="Vue logo" class="logo" src="@/assets/logo.png" width="590" height="600" />
                </v-col>

                <v-col cols="6" class="mt-7">
                    <v-card width="500px" class="mx-auto" id="rounded-card">
                        <br /><br />
                        <v-card-title primary-title class="text-center text-h4 mb-1">
                            <b class="headlogin">Register</b>
                        </v-card-title>
                        <form @submit.prevent="submitForm">
                            <v-card-text class="justify-center">
                                <v-form class="justify-center">
                                    <v-col cols="12" class="justify-center">

                                        <v-text-field type="text" label="Username" v-model="user.username"
                                            prepend-inner-icon="mdi-account" variant="outlined" required
                                            class="headlogin"
                                            :rules="[v => !!v || 'Username is required', v => !usernameExists || 'Username นี้มีคนใช้แล้ว',
                                            // v => /[a-z]/.test(v) || 'ต้องมีอย่างน้อยหนึ่งตัวอักษรเล็ก',
                                            // v => /\d/.test(v) || 'ต้องมีอย่างน้อยหนึ่งตัวเลข'
                                            ]">
                                        </v-text-field>

                                        <v-text-field type="password" label="Password" v-model="user.password"
                                            prepend-inner-icon="mdi-lock" variant="outlined" required class="headlogin"
                                            :rules="[v => !!v || 'Password is required']">
                                        </v-text-field>

                                        <v-row>
                                            <v-col cols="6">
                                                <v-text-field type="text" label="Name" v-model="user.name"
                                                    variant="outlined" required class="headlogin"
                                                    :rules="[v => !!v || 'Name is required']">
                                                </v-text-field>
                                            </v-col>
                                            <v-col cols="6">
                                                <v-text-field type="text" label="Surname" v-model="user.surname"
                                                    variant="outlined" required class="headlogin"
                                                    :rules="[v => !!v || 'Surname is required']">
                                                </v-text-field>
                                            </v-col>
                                        </v-row>
                                        <v-text-field type="email" label="Email" v-model="user.email" variant="outlined"
                                            required class="headlogin" :rules="[v => !!v || 'Email is required']">
                                        </v-text-field>
                                    </v-col>
                                </v-form>
                            </v-card-text>
                            <v-card-actions class="align-content-xl-center justify-center">
                                <v-btn type="submit" class="text-none mb-3" color="#82B1FF" size="x-large"
                                    variant="flat" rounded="xl" width="150px">
                                    <b class="buttlogin">REGISTER</b>
                                </v-btn>
                            </v-card-actions>
                            <br />
                        </form>

                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-app>
</template>

<style>
#rounded-card {
    border-radius: 25px;
    -webkit-box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
    box-shadow: 0 -1px 10px rgba(0, 0, 0, 0.2) !important;
}

.headlogin {
    color: #0d47a1;
}

.buttlogin {
    color: white;
}

.linkregis {
    color: #0d47a1;
    text-decoration: none;
}

.grey {
    color: gray;
}
</style>