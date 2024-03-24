<template>
  <v-data-iterator :items="repositories[0]" :items-per-page="itemsPerPage">
    <template v-slot:header="{ page, pageCount, prevPage, nextPage }">
      <h1 class="text-h4 font-weight-bold d-flex justify-space-between mb-4 align-center">
        <div class="text-truncate">Most popular repositories</div>

        <div class="d-flex align-center">
          <v-btn class="me-8" variant="text" @click="onClickSeeAll">
            <span class="text-decoration-underline text-none">See all</span>
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
          <v-card url=item.raw.link border>
            <v-list-item :title="item" density="comfortable" lines="two" subtitle="Name">
              <template v-slot:title>
                <strong class="text-h6"> {{ item.raw.name }} </strong>
              </template>
            </v-list-item>
            <v-list-item :title="item" density="comfortable" lines="two" subtitle="Repository URL">
              <template v-slot:title>
                <strong class="text-subtitle-1"> {{ item.raw.link }} </strong>
              </template>
            </v-list-item>
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
      itemsPerPage: 10,
    };
  },
  methods: {
    onClickSeeAll() {
      // Здесь ваш код для обработки события "See all"
    },
    prevPage() {
      // Здесь ваш код для обработки события "Previous page"
    },
    nextPage() {
      // Здесь ваш код для обработки события "Next page"
    }
  }
}
</script>
