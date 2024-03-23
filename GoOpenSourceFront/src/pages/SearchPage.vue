<template>
  <SearchRepos @getRepositories="getRepositories"></SearchRepos>
  <ReposCards :repositories="repositories"></ReposCards>
</template>
<script>
import SearchRepos from '@/components/SearchRepos.vue';
import ReposCards from '@/components/ReposCards.vue';

export default {
  components: {
    SearchRepos,
    ReposCards
  },
  data() {
    return {
      repositories: [],
    };
  },
  methods: {
    async getRepositories(queryForProject) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/getRepositories', {
          queryForProject: queryForProject
        });
        this.repositories = response.data.repositories;
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    }
  }
}
</script>