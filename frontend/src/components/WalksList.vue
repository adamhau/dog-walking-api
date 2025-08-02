<template>
  <div>
    <h2>📅 Walks List</h2>

    <button @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancel' : 'Add Walk' }}
    </button>

    <!-- Add Walk Form -->
    <form v-if="showAddForm" @submit.prevent="addWalk">
      <select v-model="newWalk.dog_id" required>
        <option disabled value="">Select Dog</option>
        <option v-for="dog in dogs" :key="dog.id" :value="dog.id">
          {{ dog.name }}
        </option>
      </select>

      <select v-model="newWalk.walker_id" required>
        <option disabled value="">Select Walker</option>
        <option v-for="walker in walkers" :key="walker.id" :value="walker.id">
          {{ walker.name }}
        </option>
      </select>

      <input v-model="newWalk.date" type="date" required />
      <button type="submit">Submit</button>
    </form>

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
            <option disabled value="">Select Dog</option>
            <option v-for="dog in dogs" :key="dog.id" :value="dog.id">
              {{ dog.name }}
            </option>
          </select>

          <select v-model="editWalk.walker_id" required>
            <option disabled value="">Select Walker</option>
            <option v-for="walker in walkers" :key="walker.id" :value="walker.id">
              {{ walker.name }}
            </option>
          </select>

          <input v-model="editWalk.date" type="date" required />
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
      walks: [],
      dogs: [],
      walkers: [],
      showAddForm: false,
      newWalk: { dog_id: '', walker_id: '', date: '' },
      editWalkId: null,
      editWalk: { dog_id: '', walker_id: '', date: '' }
    };
  },
  methods: {
    fetchAll() {
      axios.get('http://localhost:5000/walks')
        .then(res => this.walks = res.data)
        .catch(err => console.error('Error fetching walks:', err));

      axios.get('http://localhost:5000/dogs')
        .then(res => this.dogs = res.data)
        .catch(err => console.error('Error fetching dogs:', err));

      axios.get('http://localhost:5000/dogwalkers')
        .then(res => this.walkers = res.data)
        .catch(err => console.error('Error fetching walkers:', err));
    },
    getDogName(id) {
      const dog = this.dogs.find(d => d.id === id);
      return dog ? dog.name : '(Unknown Dog)';
    },
    getWalkerName(id) {
      const walker = this.walkers.find(w => w.id === id);
      return walker ? walker.name : '(Unknown Walker)';
    },
    addWalk() {
      axios.post('http://localhost:5000/walks', this.newWalk)
        .then(() => {
          this.newWalk = { dog_id: '', walker_id: '', date: '' };
          this.showAddForm = false;
          this.fetchAll();
        })
        .catch(err => console.error('Error adding walk:', err));
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
      axios.patch(`http://localhost:5000/walks/${this.editWalkId}`, this.editWalk)
        .then(() => {
          this.cancelEditing();
          this.fetchAll();
        })
        .catch(err => console.error('Error updating walk:', err));
    },
    deleteWalk(id) {
      axios.delete(`http://localhost:5000/walks/${id}`)
        .then(() => this.fetchAll())
        .catch(err => console.error('Error deleting walk:', err));
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
