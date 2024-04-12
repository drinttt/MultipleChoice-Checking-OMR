<template>
    <div class="create-exam-view">
        <h1>result Answer</h1>
        <form @submit.prevent="submitExam">
            <div class="form-group">
                <label for="idexam">Exam:</label>
                <select id="idexam" v-model="exam.id_exam" required>
                    <option value="">Please select</option>
                    <option v-for="exam in idexams" :key="exam.id_exam" :value="exam.id_exam">
                        {{ exam.name_subject }} - {{ exam.name_exam }}
                    </option>
                </select>
            </div>
        </form>
        <div v-if="imageUrls.length">
            <div v-for="(url, index) in imageUrls" :key="index" class="image-container">
                <img :src="url" :alt="'Fetched Image ' + url" class="thumbnail"/>
                <p>{{ getImageFileName(url) }}</p> 
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'ImportAnswerView',
    data() {
        return {
            exam: {
                id_exam: '',
            },
            idexams: [],
            imageUrls: [] // Updated to hold multiple image URLs
        };
    },
    mounted() {
        this.fetchidexams();
    },
    watch: {
        'exam.id_exam': {
            handler: 'fetchImages', // When this.exam.id_exam changes, call fetchImages()
            immediate: true // Call the function immediately after the component is mounted
        }
    },
    methods: {
        async fetchidexams() {
            const username = localStorage.getItem('Username');
            try {
                const response = await axios.get(`http://localhost/api/getCodeExam.php?username=${username}`);
                this.idexams = response.data;
            } catch (error) {
                console.error('Error fetching code exams:', error);
            }
        },
        async fetchImages() {
            try {
                // Check if this.exam.id_exam is not empty before fetching images
                if (this.exam.id_exam) {
                    // Construct API URL with id_exam parameter
                    const apiUrl = `http://localhost/api/showImg.php?id_exam=${this.exam.id_exam}`;
                    const response = await fetch(apiUrl);
                    const imageUrls = await response.json(); // Assuming the response is a JSON array of URLs

                    // Remove backslashes from image URLs
                    const sanitizedUrls = imageUrls.map(url => url.replace(/\\/g, ''));

                    this.imageUrls = sanitizedUrls; // Set the image URLs array for use in the template
                }
            } catch (error) {
                console.error('Error fetching images:', error);
            }
        },

        getImageFileName(url) {
            // Extracts file name from URL and trims unwanted parts
            let fileName = url.substring(url.lastIndexOf('/') + 1);
            // Remove "res_" prefix and file extension, assuming format is always like "res_XXXX-XXXX-XXXX-XXXX-X.png"
            return fileName.replace('res_', '').replace('.png', '');
        },

        // Your existing methods...
    }
};
</script>

<style scoped>
.create-exam-view {
    max-width: 500px;
    margin: auto;
    padding: 20px;
}

.thumbnail {
    width: 500px; /* Set thumbnail width */
    height: 600px; /* Set thumbnail height */
    object-fit: cover; /* Cover the container without losing aspect ratio */
    object-position: top; /* Align the top of the image with the top of the container */
    margin-right: 10px; /* Add some margin between thumbnails */

}

.image-container {
    display: flex;
    align-items: center;
}


/* Your existing styles... */
</style>

<style scoped>
.create-exam-view {
    max-width: 500px;
    margin: auto;
    padding: 20px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input[type="file"],
.form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    color: black; /* Change the color of the text in the drop-down to black */
}

button[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button[type="submit"]:hover {
    background-color: #0056b3;
}
</style>
