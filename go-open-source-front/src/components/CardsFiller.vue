<template>
    <div style="margin-top: 5rem">
      <v-data-iterator :items="currentPageItems" :items-per-page="itemsPerPage">
        <!-- Заголовок таблицы с пагинацией -->
        <template v-slot:header="{ page, pageCount, prevPage, nextPage }">
          <h1 class="text-h4 font-weight-bold d-flex justify-space-between mb-4 align-center">
            <div class="text-truncate">Most popular repositories</div>
  
            <!-- Кнопки управления пагинацией -->
            <div class="d-flex align-center">
              <v-btn class="me-8" variant="text" @click="onClickSeeAll">
                <span class="text-decoration-underline text-none">{{ buttonText }}</span>
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
  
        <!-- Отображение репозиториев на текущей странице -->
        <template v-slot:default="{ items }">
          <v-row>
            <v-col v-for="(item, i) in items" :key="i" cols="12" sm="6" xl="3">
              <v-card border @click="showOverlay(item)">
                <v-list-item :title="item.name" density="comfortable" lines="two" subtitle="Name">
                  <template v-slot:title>
                    <strong class="text-h6"> {{ item.name }} </strong>
                  </template>
                </v-list-item>
                <v-list-item :title="item.link" density="comfortable" lines="two" subtitle="Repository URL">
                  <template v-slot:title>
                    <strong class="text-subtitle-1"> {{ item.link }} </strong>
                  </template>
                </v-list-item>
              </v-card>
            </v-col>
          </v-row>
        </template>
  
        <!-- Футер с информацией о странице и количестве репозиториев -->
        <template v-slot:footer="{ page, pageCount }">
          <v-footer class="justify-space-between text-body-2 mt-4" color="surface-variant">
            Total repositories: {{ totalRepositories }}
            <div>Page {{ page }} of {{ pageCount }}</div>
          </v-footer>
        </template>
      </v-data-iterator>
  
      <!-- Всплывающее окно с подробной информацией о репозитории -->
      <v-overlay v-model="overlay" :absolute="true" class="overlay-custom">
        <v-card class="overlay-card">
          <v-list-item :title="selectedItem.name" density="comfortable" lines="two" subtitle="Name">
            <template v-slot:title>
              <strong class="text-h6"> {{ selectedItem.name }} </strong>
            </template>
          </v-list-item>
          <v-list-item :title="selectedItem.link" density="comfortable" lines="two" subtitle="Repository URL">
            <template v-slot:title>
              <strong class="text-subtitle-1"> {{ selectedItem.link }} </strong>
            </template>
          </v-list-item>
          <v-list-item :title="selectedItem.description" density="comfortable" lines="two" subtitle="Description">
            <template v-slot:title>
              <div class="description-text">
                <p class="text-subtitle-1 description-text w-100"> {{ selectedItem.description }} </p>
              </div>
            </template>
          </v-list-item>
          <v-list-item density="comfortable" lines="two" subtitle="Rating">
            <template v-slot:title>
              <p class="text-subtitle-1 rating-text"> {{ selectedItem.rating }} </p>
            </template>
          </v-list-item>
          <v-btn color="surface-variant" class="close-button" @click="hideOverlay">Close</v-btn>
        </v-card>
      </v-overlay>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        buttonText: "See all",
        itemsPerPage: 6,
        currentPage: 1,
        totalRepositories: 100, // Имитация общего числа репозиториев
        repositories: [], // Массив для имитации данных репозиториев
        overlay: false,
        selectedItem: null
      };
    },
    computed: {
      currentPageItems() {
        // Имитация пагинации и получения данных для текущей страницы
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.repositories.slice(startIndex, endIndex);
      }
    },
    methods: {
      async onClickSeeAll() {
        // Имитация асинхронной загрузки всех данных (всех репозиториев)
        this.buttonText = "Loading...";
        await this.simulateAsyncLoad();
        const generatedRepositories = this.generateRepositories();
        this.buttonText = "Hide all";
        this.$emit('repositoriesLoaded', generatedRepositories); // Эмитируем событие с передачей данных
      },
      generateRepositories() {
        // Имитация генерации данных репозиториев
        const repositories = [];
        for (let i = 1; i <= this.totalRepositories; i++) {
          repositories.push({
            name: `Repository ${i}`,
            link: `https://github.com/repo${i}`,
            description: `Description of Repository ${i}`,
            rating: Math.floor(Math.random() * 5) + 1 // Генерация случайного рейтинга от 1 до 5
          });
        }
        return repositories;
      },
      showOverlay(item) {
        this.selectedItem = item;
        this.overlay = true;
      },
      hideOverlay() {
        this.overlay = false;
      },
      nextPage() {
        // Логика для перехода на следующую страницу
        if (this.currentPage < this.pageCount) {
          this.currentPage++;
        }
      },
      prevPage() {
        // Логика для перехода на предыдущую страницу
        if (this.currentPage > 1) {
          this.currentPage--;
        }
      },
      async simulateAsyncLoad() {
        // Имитация асинхронной загрузки данных
        return new Promise(resolve => {
          setTimeout(resolve, 1500); // Задержка в 1.5 секунды
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .description-text, .rating-text {
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }
  
  .overlay-custom {
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .overlay-card {
    min-width: 60vw;
    min-height: 30vh;
    width: 60%;
    max-width: 80vw;
    max-height: 80vh;
    margin: 0 auto;
  }
  
  .close-button {
    position: absolute;
    bottom: 5px;
    right: 5px;
  }
  </style>
  