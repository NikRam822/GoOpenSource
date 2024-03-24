<template>
  <v-data-iterator :items="repositories[0]" :items-per-page="itemsPerPage">
    <template v-slot:header="{ page, pageCount, prevPage, nextPage }">
      <h1 class="text-h4 font-weight-bold d-flex justify-space-between mb-4 align-center">
        <div class="text-truncate">Most popular repositories</div>

        <div class="d-flex align-center">
          <v-btn class="me-8" variant="text" @click="onClickSeeAll">
            <span class="text-decoration-underline text-none">{{ text1 }}</span>
          </v-btn>

          <div class="d-inline-flex">
            <v-btn :disabled="page === 1" class="me-2" icon="mdi-arrow-left" size="small" variant="tonal"
              @click="prevPage"></v-btn>

            <v-btn :disabled="page === pageCount" icon="mdi-arrow-right" size="small" variant="tonal"
              @click="nextPage"></v-btn>
          </div>
        </div>
      </h1>
    </template>

    <template v-slot:default="{ items }">
      <v-row>
        <v-col v-for="(item, i) in items" :key="i" cols="12" sm="6" xl="3">
          <v-card border>
            <v-card-text :title="item" density="comfortable" lines="two" subtitle="Name">
              <p>Name:</p>
              <strong class="text-h6"> {{ item.raw.name }} </strong>
            </v-card-text>
            <v-card-title :title="item" density="comfortable" lines="two" subtitle="Repository URL">
              <p class="text-subtitle-1">repoURL:</p>
              <v-btn flat class="text-subtitle-1" :href="item.raw.link" target="_blank"> {{ item.raw.link }} </v-btn>
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <template v-slot:footer="{ page, pageCount }">
      <v-footer class="justify-space-between text-body-2 mt-4" color="surface-variant">
        Total repositories: {{ repositories.length }}

        <div>Page {{ page }} of {{ pageCount }}</div>
      </v-footer>
    </template>
  </v-data-iterator>
</template>

<script>
export default {
  props: {
    repositories: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      text1: "See all",
      switchwbool: false,
      showHide: { true: [1000, 'Hide all'], false: [6, 'See all'] },
      itemsPerPage: 6,
    };
  },
  methods: {
    onClickSeeAll() {
      this.switchwbool = !this.switchwbool
      this.text1 = this.showHide[this.switchwbool][1]
      this.itemsPerPage = this.showHide[this.switchwbool][0]
    }
  }
}
</script>
