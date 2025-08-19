<template>
  <div>
    <h2>🚶 Dogwalkers List</h2>

    <!-- MESSAGE DISPLAY -->
    <div v-if="message" class="message-box">
      {{ message }}
    </div>

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
          {{ walker.name }}, {{ walker.phone }}
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
      editWalker: { name: '', phone: '' },
      message: '',          // for user messages
      messageTimeoutId: null // to clear timeout
    };
  },
  methods: {
    fetchWalkers() {
      axios.get('http://localhost:5000/dogwalkers')
        .then(res => {
          this.walkers = res.data;
        })
        .catch(err => {
          this.setMessage('Error fetching dogwalkers.');
          console.error('Error fetching dogwalkers:', err);
        });
    },
    addWalker() {
      axios.post('http://localhost:5000/dogwalkers', this.newWalker)
        .then(res => {
          this.newWalker = { name: '', phone: '' };
          this.showAddForm = false;
          this.fetchWalkers();
          this.setMessage(res.data.message || 'Walker added successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error adding walker.');
          console.error('Error adding walker:', err);
        });
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
        .then(res => {
          this.cancelEditing();
          this.fetchWalkers();
          this.setMessage(res.data.message || 'Walker updated successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error updating walker.');
          console.error('Error updating walker:', err);
        });
    },
    deleteWalker(id) {
      axios.delete(`http://localhost:5000/dogwalkers/${id}`)
        .then(res => {
          this.fetchWalkers();
          this.setMessage(res.data.message || 'Walker deleted successfully!');
        })
        .catch(err => {
          this.setMessage(err.response?.data?.message || 'Error deleting walker.');
          console.error('Error deleting walker:', err);
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
    this.fetchWalkers();
  }
};
</script>

<style scoped>
button {
  margin: 4px;
}
form {
  margin: 0.5rem 0;
}
input {
  margin-right: 0.5rem;
}
</style>
