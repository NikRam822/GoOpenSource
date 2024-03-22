<template>
    <div>
        <v-form @submit.prevent="sendQuerry">
            <v-text-field v-model="queryForProject" :rules="rules" label="Enter your querry"></v-text-field>
            <v-btn type="submit" block>Search</v-btn>
        </v-form>
    </div>
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
        sendQuerry() {
            this.$emit('getRepositories', this.queryForProject);
        }
    }
}
</script>
<style></style>