<template>
  <div id="app">
    <nav class="tabs">
      <button 
        :class="{ active: activeTab === 'dogs' }" 
        @click="activeTab = 'dogs'">🐶 Dogs</button>
      <button 
        :class="{ active: activeTab === 'walkers' }" 
        @click="activeTab = 'walkers'">🚶 Dogwalkers</button>
      <button 
        :class="{ active: activeTab === 'walks' }" 
        @click="activeTab = 'walks'">📅 Walks</button>
    </nav>

    <section class="content">
      <DogList v-if="activeTab === 'dogs'" />
      <WalkerList v-if="activeTab === 'walkers'" />
      <WalksList v-if="activeTab === 'walks'" />
    </section>
  </div>
</template>

<script>
import DogList from './components/DogList.vue'
import WalkerList from './components/WalkerList.vue'
import WalksList from './components/WalksList.vue'

export default {
  name: 'App',
  components: {
    DogList,
    WalkerList,
    WalksList
  },
  data() {
    return {
      activeTab: 'dogs'  // default tab
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 600px;
  margin: 2rem auto;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #ccc;
}

.tabs button {
  flex: 1;
  padding: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: bold;
  border-bottom: 3px solid transparent;
  transition: border-color 0.3s ease;
}

.tabs button:hover {
  background-color: #f5f5f5;
}

.tabs button.active {
  border-color: #42b983;
  color: #42b983;
}

.content {
  padding: 1rem;
}
</style>
