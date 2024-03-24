<template>
  <v-form class="h-300" ref="form">
    <v-row>
      <v-textarea variant="outlined"
      v-model="queryForProject"
      :rules="rules"
      label="Enter your querry"
      auto-grow="true"
      rows="1">
        <template v-slot:append-inner>
          <v-btn @click="sendQuerry"><v-icon icon="mdi-magnify" size="x-large"></v-icon></v-btn>
        </template>
      </v-textarea>
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
