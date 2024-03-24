<template>
  <v-container>
    <v-row>
      <v-col>
        <v-container>
          <SearchRepos @getRepositories="getRepositories"></SearchRepos>
          <ReposCards :repositories="repositories"></ReposCards>
        </v-container>
      </v-col>
      <v-col cols='3'>
        <Filter></Filter>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from 'axios'
export default {
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
        }, {
        withCredentials: true,
      })
        this.repositories = response.data.repositories;
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    }
  }
}
</script>
