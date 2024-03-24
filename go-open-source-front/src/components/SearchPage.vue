<template>
  <v-container>
    <v-row>
      <v-col>
        <v-container>
          <SearchRepos @getRepositories="getRepositories"></SearchRepos>
          <v-col align="center">
            <v-progress-circular v-if="switch" indeterminate size="50" width="10"
              color="grey-darken-3"></v-progress-circular>
          </v-col>
        </v-container>
        <ReposCards :repositories=" repositories "></ReposCards>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import axios from 'axios'
export default {
  data() {
    return {
      switch: false,
      repositories: [],
    };
  },
  methods: {
    async getRepositories(queryForProject) {
      this.switch = true
      try {
        const response = await axios.post('http://127.0.0.1:8000/getRepositories', {
          queryForProject: queryForProject
        }, {
          withCredentials: true,
        })
        this.switch = false
        this.repositories = response.data.repositories;
      } catch (error) {
        console.error('Error fetching repositories:', error);
      }
    }
  }
}
</script>
