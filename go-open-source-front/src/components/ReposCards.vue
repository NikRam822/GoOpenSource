<template>
  <div style="margin-top: 5;">
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
            <v-card border @click="showOverlay(item)">
              <v-list-item :title="item.raw.name" density="comfortable" lines="two" subtitle="Name">
                <template v-slot:title>
                  <strong class="text-h6"> {{ item.raw.name }} </strong>
                </template>
              </v-list-item>
              <v-list-item :title="item.raw.link" density="comfortable" lines="two" subtitle="Repository URL">
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

    <!-- Всплывающее окно -->
    <v-overlay v-model="overlay" :absolute="true" class="overlay-custom">
      <v-card class="overlay-card">
        <v-list-item :title="selectedItem" density="comfortable" lines="two" subtitle="Name">
          <template v-slot:title>
            <strong class="text-h6"> {{ selectedItem.raw.name }} </strong>
          </template>
        </v-list-item>
        <v-list-item :title="selectedItem" density="comfortable" lines="two" subtitle="Repository URL">
          <template v-slot:title>
            <strong class="text-subtitle-1"> {{ selectedItem.raw.link }} </strong>
          </template>
        </v-list-item>
        <v-list-item :title="selectedItem" density="comfortable" lines="two" subtitle="Description">
          <template v-slot:title>
            <div class="description-text">
              <p class="text-subtitle-1 description-text w-100"> {{ selectedItem.raw.out_description }} </p>
            </div>
          </template>
        </v-list-item>
        <v-list-item density="comfortable" lines="two" subtitle="Rating">
          <template v-slot:title>
            <p class="text-subtitle-1 rating-text"> {{ selectedItem.raw.out_rating }} </p>
          </template>
        </v-list-item>
        <v-btn color="surface-variant" class="close-button" @click="hideOverlay">Close</v-btn>
      </v-card>
    </v-overlay>
  </div>
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
      overlay: false,
      selectedItem: null
    };
  },
  methods: {
    onClickSeeAll() {
      this.switchwbool = !this.switchwbool
      this.text1 = this.showHide[this.switchwbool][1]
      this.itemsPerPage = this.showHide[this.switchwbool][0]
    },
    showOverlay(item) {
      this.selectedItem = item;
      this.overlay = true;
    },
    hideOverlay() {
      this.overlay = false;
    },
    nextPage() {
      // Ваша логика для перехода на следующую страницу
    },
    prevPage() {
      // Ваша логика для перехода на предыдущую страницу
    }
  }
}
</script>

<style scoped>
.description-text {
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.rating-text {
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.overlay-custom {
  z-index: 9999;
  /* Устанавливаем высокий z-index, чтобы overlay был поверх других элементов */
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.5);
  /* Добавляем немного прозрачности для подложки */
}

.overlay-card {
  min-width: 60vw;
  /* Минимальная ширина в 60% от ширины экрана */
  min-height: 30vh;
  /* Минимальная высота в 30% от высоты экрана */
  width: 60%;
  /* Увеличиваем ширину карточки всплывающего окна */
  max-width: 80vw;
  /* Максимальная ширина в 80% от ширины экрана */
  max-height: 80vh;
  /* Максимальная высота в 80% от высоты экрана */
  margin: 0 auto;
  /* Центрируем карточку по горизонтали */
}

.close-button {
  position: absolute;
  /* Абсолютное позиционирование для кнопки */
  bottom: 5px;
  /* Отступ от нижнего края */
  right: 5px;
  /* Отступ от правого края */

}
</style>
