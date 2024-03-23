<template>
    <v-toolbar app>
        <v-form ref="form">
            <v-text-field v-model="queryForProject" :rules="rules" label="Enter your querry"></v-text-field>
            <v-btn @click="sendQuerry">Search</v-btn>
        </v-form>
    </v-toolbar>
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
<style></style>