<template>
  <div>
    <h2>🐶 Dog List</h2>

    <!-- MESSAGE DISPLAY -->
    <div v-if="message" class="message-box">
      {{ message }}
    </div>

    <button @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancel' : 'Add Dog' }}
    </button>

    <!-- Add Dog Form -->
    <form v-if="showAddForm" @submit.prevent="addDog">
      <input v-model="newDog.name" placeholder="Name" required />
      <input v-model="newDog.breed" placeholder="Breed" required />
      <input v-model="newDog.age" type="number" placeholder="Age" required />
      <button type="submit">Submit</button>
    </form>

    <ul v-if="dogs.length">
      <li v-for="dog in dogs" :key="dog.id">
        <span v-if="editDogId !== dog.id">
          {{ dog.name }}, {{ dog.breed }}, {{ dog.age }} years old
          <button @click="startEditing(dog)">Edit</button>
          <button @click="deleteDog(dog.id)">❌</button>
        </span>

        <!-- Edit Dog Form -->
        <form v-else @submit.prevent="updateDog">
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
      editDogId: null,
      editDog: { name: '', breed: '', age: '' },
      message: '',  // <-- message state
      messageTimeoutId: null,  // for clearing message timeout
    };
  },
  methods: {
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
    addDog() {
      axios.post('http://localhost:5000/dogs', this.newDog)
        .then(res => {
          this.newDog = { name: '', breed: '', age: '' };
          this.showAddForm = false;
          this.fetchDogs();
          this.setMessage(res.data.message || 'Dog added successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error adding dog.');
          console.error('Error adding dog:', err);
        });
    },
    startEditing(dog) {
      this.editDogId = dog.id;
      this.editDog = { ...dog };
    },
    cancelEditing() {
      this.editDogId = null;
      this.editDog = { name: '', breed: '', age: '' };
    },
    updateDog() {
      axios.patch(`http://localhost:5000/dogs/${this.editDogId}`, this.editDog)
        .then(res => {
          this.cancelEditing();
          this.fetchDogs();
          this.setMessage(res.data.message || 'Dog updated successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error updating dog.');
          console.error('Error updating dog:', err);
        });
    },
    deleteDog(id) {
      axios.delete(`http://localhost:5000/dogs/${id}`)
        .then(res => {
          this.fetchDogs();
          this.setMessage(res.data.message || 'Dog deleted successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error deleting dog.');
          console.error('Error deleting dog:', err);
        });
    },
    setMessage(msg) {
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

.message-box {
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  border-radius: 5px;
  background-color: #e0f7fa;
  color: #006064;
  font-weight: 600;
  border: 1px solid #4dd0e1;
}
</style>
