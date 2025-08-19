<template>
  <div>
    <h2>📅 Walks List</h2>

    <!-- MESSAGE DISPLAY -->
    <div v-if="message" class="message-box">
      {{ message }}
    </div>

    <button @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancel' : 'Add Walk' }}
    </button>

    <!-- Add Walk Form -->
    <form v-if="showAddForm" @submit.prevent="addWalk"> <!-- if showAddForm is true, show form -->
      <select v-model="newWalk.dog_id" required>
        <option disabled value="">Select Dog</option> 
        <option v-for="dog in dogs" :key="dog.id" :value="dog.id"> <!-- display all of the dogs avail -->
          {{ dog.name }}
        </option>
      </select>

      <select v-model="newWalk.walker_id" required>
        <option disabled value="">Select Walker</option>
        <option v-for="walker in walkers" :key="walker.id" :value="walker.id"> <!-- display all of the walkers avail -->
          {{ walker.name }}
        </option>
      </select>

      <input v-model="newWalk.date" type="date" required /> <!-- date input -->
      <button type="submit">Submit</button>
    </form>

    <!-- list walks with edit and delete buttons -->
    <ul v-if="walks.length"> 
      <li v-for="walk in walks" :key="walk.id">
        <span v-if="editWalkId !== walk.id">
          Dog: {{ getDogName(walk.dog_id) }} — Walker: {{ getWalkerName(walk.walker_id) }} — Date: {{ walk.date }}
          <button @click="startEditing(walk)">Edit</button>
          <button @click="deleteWalk(walk.id)">❌</button>
        </span>

        <!-- Edit Walk Form -->
        <form v-else @submit.prevent="updateWalk">
          <select v-model="editWalk.dog_id" required>
            <option disabled value="">Select Dog</option> <!-- choose avail dog -->
            <option v-for="dog in dogs" :key="dog.id" :value="dog.id">
              {{ dog.name }}
            </option>
          </select>

          <select v-model="editWalk.walker_id" required>
            <option disabled value="">Select Walker</option> <!-- choose avail walker -->
            <option v-for="walker in walkers" :key="walker.id" :value="walker.id">
              {{ walker.name }}
            </option>
          </select>

          <input v-model="editWalk.date" type="date" required /> <!-- change date -->
          <button type="submit">💾 Save</button>
          <button type="button" @click="cancelEditing">Cancel</button>
        </form>
      </li>
    </ul>

    <p v-else>Loading walks...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WalkList',
  data() {
    return {
      walks: [], // list of walks
      dogs: [], // list of dogs
      walkers: [], // list of walkers
      showAddForm: false, // toggle for add form
      newWalk: { dog_id: '', walker_id: '', date: '' }, // new walk data
      editWalkId: null, // id of walk being edited
      editWalk: { dog_id: '', walker_id: '', date: '' }, // temp storage for edits
      message: '',            // <-- message state
      messageTimeoutId: null, // for clearing message timeout
    };
  },
  methods: {
    fetchAll() { // fetch all walk data from backend
      axios.get('http://localhost:5000/walks')
        .then(res => this.walks = res.data)
        .catch(err => {
          this.setMessage('Error fetching walks.');
          console.error('Error fetching walks:', err);
        });
        // fetch all dogs data from backend
      axios.get('http://localhost:5000/dogs')
        .then(res => this.dogs = res.data)
        .catch(err => {
          this.setMessage('Error fetching dogs.');
          console.error('Error fetching dogs:', err);
        });
        // fetch all walkers data from backend
      axios.get('http://localhost:5000/dogwalkers')
        .then(res => this.walkers = res.data)
        .catch(err => {
          this.setMessage('Error fetching dogwalkers.');
          console.error('Error fetching dogwalkers:', err);
        });
    },
    getDogName(id) {
      const dog = this.dogs.find(d => d.id === id); //if valid dog
      return dog ? dog.name : '(Unknown Dog)'; //display its name
    },
    getWalkerName(id) {
      const walker = this.walkers.find(w => w.id === id); //if valid walker
      return walker ? walker.name : '(Unknown Walker)'; //display its name
    },
    addWalk() {
      axios.post('http://localhost:5000/walks', this.newWalk) // sends newWalk JSON to the backend
        .then(res => {
          this.newWalk = { dog_id: '', walker_id: '', date: '' }; // clear form
          this.showAddForm = false; // hide form
          this.fetchAll(); // refresh walk list
          this.setMessage(res.data.message || 'Walk added successfully!'); // success message (uses backend response if available)
        })
        .catch(err => { // handle error if any
          this.setMessage(err.response?.data?.message || 'Error adding walk.');
          console.error('Error adding walk:', err);
        });
    },
    startEditing(walk) {
      this.editWalkId = walk.id;
      this.editWalk = { ...walk };
    },
    cancelEditing() {
      this.editWalkId = null;
      this.editWalk = { dog_id: '', walker_id: '', date: '' };
    },
    updateWalk() {
      axios.patch(`http://localhost:5000/walks/${this.editWalkId}`, this.editWalk) // sends edited walk data to the backend
        .then(res => {
          this.cancelEditing(); // exit edit mode
          this.fetchAll(); // refresh walk list
          this.setMessage(res.data.message || 'Walk updated successfully!'); // success message (uses backend response if available)
        })
        .catch(err => { // handle error if any
          this.setMessage(err.response?.data?.message || 'Error updating walk.');
          console.error('Error updating walk:', err);
        });
    },
    deleteWalk(id) {
      axios.delete(`http://localhost:5000/walks/${id}`) // sends delete request to the backend
        .then(res => {
          this.fetchAll(); // refresh walk list
          this.setMessage(res.data.message || 'Walk deleted successfully!'); // success message (uses backend response if available) 
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error deleting walk.');
          console.error('Error deleting walk:', err);
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
    this.fetchAll();
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
input,
select {
  margin-right: 0.5rem;
}
</style>
