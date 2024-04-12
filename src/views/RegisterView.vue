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
            usernameExists: false, // Flag to check if username exists
        }
    },
    watch: {
        // Watch for changes in the username and call checkUsername method
        'user.username'(newUsername) {
            this.usernameExists = false; // Reset the flag
            if (newUsername) {
                this.checkUsername(newUsername);
            }
        }
    },
    methods: {
        async checkUsername(username) {
            try {
                const response = await axios.get(`http://localhost/api/checkUsername.php?username=${username}`);
                if (response.data.exists) {
                    // If username exists, set flag to true
                    this.usernameExists = true;
                }
            } catch (error) {
                console.error('Error checking username:', error);
            }
        },
        async submitForm() {
            if (this.usernameExists) {
                alert('Username already taken. Please choose a different one.');
                return; // Prevent form submission if username exists
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
                    alert('An error occurred while registering. Please try again later.');
                }
            } catch (error) {
                console.error('Error registering:', error);
                alert('An error occurred while registering. Please try again later.');
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
                                        <!-- <div class="form-group">
                                            <label>Username:</label>
                                            <input type="text" id="username" v-model="user.username" required>
                                        </div> -->

                                        <div class="form-group">
                                            <label>Username:</label>
                                            <input type="text" id="username" v-model="user.username"
                                                @input="usernameExists = false" required>
                                            <!-- Alert Text -->
                                            <div v-if="usernameExists" class="alert-box">
                                                Username นี้มีคนใช้แล้ว
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <label>Password:</label>
                                            <input type="password" id="password" v-model="user.password" required>
                                        </div>
                                        <v-row>
                                            <v-col cols="6">
                                                <div class="form-group">
                                                    <label>Name:</label>
                                                    <input type="text" id="name" v-model="user.name" required>
                                                </div>
                                            </v-col>
                                            <v-col cols="6">
                                                <div class="form-group">
                                                    <label>Surname:</label>
                                                    <input type="text" id="surname" v-model="user.surname" required>
                                                </div>
                                            </v-col>
                                        </v-row>

                                        <div class="form-group">
                                            <label>Email:</label>
                                            <input type="email" id="email" v-model="user.email" required>
                                        </div>
                                    </v-col>
                                    <div class="text-caption text-center">
                                        <p class="grey">
                                            Already have an account? <router-link to="/login"
                                                class="linkregis">Login</router-link>
                                        </p>
                                    </div>
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
.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.alert-box {
    display: block;
    /* Make the box appear on a new line */
    color: red;
    /* Text color */
    font-size: 14px;
    /* Text size */
    margin-top: 5px;
    /* Space between input and box */
    border: 1px solid red;
    /* Border color */
    padding: 5px;
    /* Padding inside the box */
    border-radius: 5px;
    /* Rounded corners */
    background-color: #ffe6e6;
    /* Light red background */
    box-shadow: 0px 0px 5px red;
    /* Shadow effect */
}

.input-group {
    display: flex;
    align-items: center;
    /* Aligns icon vertically with the input field */
}

.form-group input[type="text"],
.form-group input[type="password"],
.form-group input[type="email"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

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
