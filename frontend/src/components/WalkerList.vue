<template>
  <div>
    <h2>🚶 Dogwalkers List</h2>

    <button @click="showAddForm = !showAddForm">
      {{ showAddForm ? 'Cancel' : 'Add Walker' }}
    </button>

    <!-- Add Walker Form -->
    <form v-if="showAddForm" @submit.prevent="addWalker">
      <input v-model="newWalker.name" placeholder="Name" required />
      <input v-model="newWalker.phone" placeholder="Phone Number" required />
      <button type="submit">Submit</button>
    </form>

    <ul v-if="walkers.length">
      <li v-for="walker in walkers" :key="walker.id">
        <span v-if="editWalkerId !== walker.id">
          {{ walker.name }} — {{ walker.phone }}
          <button @click="startEditing(walker)">Edit</button>
          <button @click="deleteWalker(walker.id)">❌</button>
        </span>

        <!-- Edit Walker Form -->
        <form v-else @submit.prevent="updateWalker">
          <input v-model="editWalker.name" required />
          <input v-model="editWalker.phone" required />
          <button type="submit">💾 Save</button>
          <button type="button" @click="cancelEditing">Cancel</button>
        </form>
      </li>
    </ul>

    <p v-else>Loading dogwalkers...</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WalkerList',
  data() {
    return {
      walkers: [],
      showAddForm: false,
      newWalker: { name: '', phone: '' },
      editWalkerId: null,
      editWalker: { name: '', phone: '' }
    };
  },
  methods: {
    fetchWalkers() {
      axios.get('http://localhost:5000/dogwalkers')
        .then(res => this.walkers = res.data)
        .catch(err => console.error('Error fetching walkers:', err));
    },
    addWalker() {
      axios.post('http://localhost:5000/dogwalkers', this.newWalker)
        .then(() => {
          this.newWalker = { name: '', phone: '' };
          this.showAddForm = false;
          this.fetchWalkers();
        })
        .catch(err => console.error('Error adding walker:', err));
    },
    startEditing(walker) {
      this.editWalkerId = walker.id;
      this.editWalker = { ...walker };
    },
    cancelEditing() {
      this.editWalkerId = null;
      this.editWalker = { name: '', phone: '' };
    },
    updateWalker() {
      axios.patch(`http://localhost:5000/dogwalkers/${this.editWalkerId}`, this.editWalker)
        .then(() => {
          this.cancelEditing();
          this.fetchWalkers();
        })
        .catch(err => console.error('Error updating walker:', err));
    },
    deleteWalker(id) {
      axios.delete(`http://localhost:5000/dogwalkers/${id}`)
        .then(() => this.fetchWalkers())
        .catch(err => console.error('Error deleting walker:', err));
    }
  },
  mounted() {
    this.fetchWalkers();
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
  margin-right: 0.5rem;
}
</style>
