<template>
    <div>
      <!-- Search bar -->
      <div class="search-wrapper" :class="{ active: searchActive, 'search-icon-upper': searchUsed }">
        <div class="input-holder">
          <textarea
            ref="searchInput"
            class="search-input"
            placeholder="Type to search"
            v-model="searchQuery"
            @keydown.enter="handleEnter"
          ></textarea>
          <button class="search-icon" @click="customSearchFunction"><span></span></button>
        </div>
      </div>
      <div class="cards">
        <v-col align="center">
          <v-progress-circular v-if="switch" indeterminate size="50" width="10" color="grey-lighten-3"></v-progress-circular>
        </v-col>
        <ReposCards v-show="show" :repositories="repositories"></ReposCards>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        searchActive: false,
        searchQuery: '',
        show: false,
        switch: false,
        repositories: [],
        searchUsed: false
      };
    },
    mounted() {
      setTimeout(() => {
        this.searchActive = true;
      }, 500);
    },
    methods: {
      handleEnter(event) {
        if (event.key === 'Enter') {
          // Вставляем символ новой строки в текущую позицию курсора
          const textarea = this.$refs.searchInput;
          const cursorPosition = textarea.selectionStart;
          const newSearchQuery =
            this.searchQuery.slice(0, cursorPosition) +
            this.searchQuery.slice(cursorPosition);
  
          this.searchQuery = newSearchQuery;
          
          // Поднимаем поисковую строку
          this.searchActive = false;
          setTimeout(() => {
            this.searchActive = true;
          }, 0);
        }
      },
      async customSearchFunction() {
        this.switch = true;
        this.searchUsed = true;
  
        try {
          const response = await axios.post('http://127.0.0.1:8000/getRepositories', {
            queryForProject: this.searchQuery
          }, {
            withCredentials: true,
          });
  
          this.show = true;
          this.repositories = response.data.repositories;
          this.switch = false;
        } catch (error) {
          console.error('Error fetching repositories:', error);
        }
      }
    }
  };
  </script>
  <style scoped>
/* .rotating-message {
  z-index: 1;
  color: black;
  font-size: 14px;
} */

  .cards {
  margin-top: 20px; /* Adjust this value to provide spacing below the search bar */
  padding-top: 20px; /* Add padding to separate the content from the search bar */
}

  .search-wrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50px;
    border: 5px solid transparent;
    background: radial-gradient(circle, red, blue);
    overflow: hidden;
    margin-bottom: 5;
  }
  
  .search-wrapper.active .input-holder {
    width: 450px;
    border-radius: 50px;
    background: white;
    transition: all 0.5s ease;
  }
  
  .input-holder {
    height: 70px;
    width: 70px;
    overflow: hidden;
    background: white;
    border-radius: 20px;
    position: relative;
    transition: all 0.3s ease-in-out;
  }
  
  .search-wrapper.active .input-holder .search-input {
    opacity: 1;
    transform: translate(0, 10px);
  }
  
  .search-wrapper .input-holder .search-input {
    width: calc(100% - 70px);
    height: 50px;
    padding: 0px 20px;
    opacity: 1;
    position: absolute;
    top: 0px;
    left: 70px;
    background: transparent;
    box-sizing: border-box;
    border: none;
    outline: none;
    font-family: "Open Sans", Arial, Verdana;
    font-size: 16px;
    font-weight: 400;
    line-height: 20px;
    color: black;
    transform: translate(0, 0);
    transition: all 0.3s ease;
    transition-delay: 0.3s;
    resize: none; /* Отключаем возможность изменения размеров */
  }
  
  .search-wrapper .input-holder .search-icon {
    width: 70px;
    height: 70px;
    border: none;
    border-radius: 6px;
    background: #fff;
    padding: 0px;
    outline: none;
    position: absolute;
    top: 0;
    right: 0;
    z-index: 2;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
  }
  
  .search-wrapper.active .input-holder .search-icon {
    width: 50px;
    height: 50px;
    margin: 10px;
    border-radius: 30px;
  }
  
  .search-wrapper .input-holder .search-icon span {
    width: 22px;
    height: 22px;
    display: inline-block;
    vertical-align: middle;
    position: relative;
    transform: rotate(45deg);
    transition: all 0.4s ease;
  }
  
  .search-wrapper.active .input-holder .search-icon span {
    transform: rotate(-45deg);
  }
  
  .search-wrapper .input-holder .search-icon span::before,
  .search-wrapper .input-holder .search-icon span::after {
    position: absolute;
    content: '';
  }
  
  .search-wrapper .input-holder .search-icon span::before {
    width: 4px;
    height: 11px;
    left: 9px;
    top: 18px;
    border-radius: 2px;
    background: #fe5f55;
  }
  
  .search-wrapper .input-holder .search-icon span::after {
    width: 14px;
    height: 14px;
    left: 0px;
    top: 0px;
    border-radius: 16px;
    border: 4px solid #fe5f55;
  }
  
  .search-icon-upper {
    top: 10vh; /* Adjust as needed */
    transition: top 0.3s ease;
  }

  .cards {
    margin-top: 100px; /* Adjust this value to push cards down below search-wrapper */
  }
</style>
