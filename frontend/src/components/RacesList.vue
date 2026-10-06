<template>
  <div class="races-container">
    <h1>Corridas Disponíveis</h1>
    
    <!-- Mensagem se a lista estiver vazia ou carregando -->
    <p v-if="loading">Carregando corridas...</p>
    <p v-else-if="races.length === 0">Nenhuma corrida encontrada.</p>

    <!-- Lista de corridas (Diretiva v-for do Vue) -->
    <ul v-else class="race-list">
      <li v-for="race in races" :key="race.id" class="race-item">
        <h2>{{ race.name }}</h2>
        <p><strong>Data:</strong> {{ race.date }}</p>
        <p><strong>Local:</strong> {{ race.location }}</p>
        <p><strong>Distância:</strong> {{ race.distance }} km</p>
        <p v-if="race.description"><em>{{ race.description }}</em></p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RacesList',
  data() {
    return {
      races: [],
      loading: true
    };
  },
  // O hook 'created' é executado assim que o componente é criado na memória
  created() {
    this.fetchRaces();
  },
  methods: {
    async fetchRaces() {
      try {
        // Requisição GET para a NOSSA API (porta 8000, não 8080 do PDF)
        const response = await axios.get('http://localhost:8000/api/v1/races/');
        this.races = response.data;
      } catch (error) {
        console.error('Erro ao buscar corridas:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.races-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: Arial, sans-serif;
}
h1 {
  color: #42b983; /* Verde do Vue */
  text-align: center;
}
.race-list {
  list-style-type: none;
  padding: 0;
}
.race-item {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.race-item h2 {
  margin-top: 0;
  color: #2c3e50;
}
</style>
