<template>
  <h1 class="app-title">Paw🐕Walk</h1>
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

.content {
  padding: 1rem;
}

.app-title {
  font-family: 'Trebuchet MS', Helvetica, sans-serif;
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: #1abc9c;
  margin: 1rem 0;
}
</style>