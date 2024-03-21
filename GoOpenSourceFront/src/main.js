const app = Vue.createApp({
  data() {
    return {
      queryForProject: '',
      repositories: []
    };
  },
  methods: {
    async getRepositories() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/getRepositories', {
          queryForProject: this.queryForProject
        });
        this.repositories = response.data.repositories;
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    }
  }
})

app.mount('#app')
