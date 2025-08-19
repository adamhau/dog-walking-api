<template>
  <div>
    <h2>🐶 Dog List</h2>

    <!-- MESSAGE DISPLAY -->
    <div v-if="message" class="message-box">
      {{ message }} <!-- display message if exists -->
    </div>

    <button @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancel' : 'Add Dog' }} <!-- if we show form, change button to say cancel -->
    </button>

    <!-- Add Dog Form -->
    <form v-if="showAddForm" @submit.prevent="addDog">
      <input v-model="newDog.name" placeholder="Name" required />
      <input v-model="newDog.breed" placeholder="Breed" required />
      <input v-model="newDog.age" type="number" placeholder="Age" required />
      <button type="submit">Submit</button>
    </form>

    <!-- list dogs with edit and delete buttons -->
    <ul v-if="dogs.length">
      <li v-for="dog in dogs" :key="dog.id">
        <span v-if="editDogId !== dog.id"> <!-- show dog details if not editing -->
          {{ dog.name }}, {{ dog.breed }}, {{ dog.age }} years old
          <button @click="startEditing(dog)">Edit</button>
          <button @click="deleteDog(dog.id)">❌</button>
        </span>

        <!-- Edit Dog Form -->
        <form v-else @submit.prevent="updateDog"> <!-- Show this form if editing -->
          <input v-model="editDog.name" required />
          <input v-model="editDog.breed" required />
          <input v-model="editDog.age" type="number" required />
          <button type="submit">💾 Save</button>
          <button type="button" @click="cancelEditing">Cancel</button>
        </form>
      </li>
    </ul>

    <p v-else>Loading dogs...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DogList',
  data() {
    return {
      dogs: [],
      showAddForm: false,
      newDog: { name: '', breed: '', age: '' },
      editDogId: null, // id of dog being edited
      editDog: { name: '', breed: '', age: '' }, // temp storage for edits
      message: '',  // <-- message state
      messageTimeoutId: null,  // for clearing message timeout
    };
  },
  methods: {
    // get dogs from the backend
    fetchDogs() {
      axios.get('http://localhost:5000/dogs')
        .then(res => {
          this.dogs = res.data;
        })
        .catch(err => {
          this.setMessage('Error fetching dogs.');
          console.error('Error fetching dogs:', err);
        });
    },
    // add a new dog
    addDog() {
      axios.post('http://localhost:5000/dogs', this.newDog) //sends newDog JSON to the backend
        .then(res => {
          this.newDog = { name: '', breed: '', age: '' }; //clear form
          this.showAddForm = false; //hide form
          this.fetchDogs(); //refresh dog list
          this.setMessage(res.data.message || 'Dog added successfully!'); // success message (uses backend response if available)
        })
        .catch(err => { // handle error if any
          this.setMessage(err.response?.data?.message || 'Error adding dog.');
          console.error('Error adding dog:', err);
        });
    },
    startEditing(dog) {
      this.editDogId = dog.id; //set which dog is being edited
      this.editDog = { ...dog }; //copy current dog data to editDog
    },
    cancelEditing() {
      this.editDogId = null; //clear edit mode
      this.editDog = { name: '', breed: '', age: '' };
    },
    updateDog() {
      axios.patch(`http://localhost:5000/dogs/${this.editDogId}`, this.editDog) // sends edited dog data to the backend
        .then(res => {
          this.cancelEditing(); // exit edit mode
          this.fetchDogs(); // refresh dog list
          this.setMessage(res.data.message || 'Dog updated successfully!'); // success message (uses backend response if available)
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error updating dog.');  // handle error if any
          console.error('Error updating dog:', err);
        });
    },
    deleteDog(id) {
      axios.delete(`http://localhost:5000/dogs/${id}`) // sends delete request to the backend
        .then(res => {
          this.fetchDogs(); 
          this.setMessage(res.data.message || 'Dog deleted successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error deleting dog.');
          console.error('Error deleting dog:', err);
        });
    },
    setMessage(msg) { // set and display message, clear after 5 seconds
      this.message = msg;
      if (this.messageTimeoutId) clearTimeout(this.messageTimeoutId);
      this.messageTimeoutId = setTimeout(() => {
        this.message = '';
      }, 5000);
    }
  },
  mounted() {
    this.fetchDogs();
  }
};
</script>

<!-- misc css -->
<style scoped>
button {
  margin: 0 4px;
}
form {
  margin: 0.5rem 0;
}
input {
  margin: 0.25rem;
  margin-right: 0.25rem;
}
</style>
