<template>
  <v-form class="h-300" ref="form">
    <v-row>
      <v-text-field class="h-200" v-model="queryForProject" :rules="rules" label="Enter your querry">
        <template v-slot:append-inner>
          <v-btn @click="sendQuerry">Search</v-btn>
        </template>
      </v-text-field>
    </v-row>
  </v-form>
</template>
<script>
export default {
  data() {
    return {
      queryForProject: '',
      rules: [
        value => {
          if (value) return true
          return 'You must enter.'
        },
      ],
    };
  },
  methods: {
    async sendQuerry() {
      const { valid } = await this.$refs.form.validate()
      if (valid) {
        this.$emit('getRepositories', this.queryForProject);
      }
    }
  }
}
</script>
