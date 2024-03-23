<template>
    <div>
        <v-container v-for = "repos in repositories" >
            <v-card v-for="rep in repos" variant="tonal" class = "my-5" hover :href = 'rep'>
                <v-card-item> {{ rep }}</v-card-item>
            </v-card>
        </v-container>
    </div>
</template>
<script>
export default {
    props: {
        repositories: {
            type: Array,
            default: () => []
        }
    }
}
</script>