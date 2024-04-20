<template>
  <div class="Carousel">
    <swiper
      :slidesPerView="3"
      :spaceBetween="30"
      :freeMode="true"
      :pagination="{
        clickable: true,
      }"
      :modules="modules"
      class="mySwiper"
    >
      <swiper-slide>Slide 1</swiper-slide>
      <swiper-slide>Slide 2</swiper-slide>
      <swiper-slide>Slide 3</swiper-slide>
      <swiper-slide>Slide 4</swiper-slide>
      <swiper-slide>Slide 5</swiper-slide>
      <swiper-slide>Slide 6</swiper-slide>
      <swiper-slide>Slide 7</swiper-slide>
      <swiper-slide>Slide 8</swiper-slide>
      <swiper-slide>Slide 9</swiper-slide>
    </swiper>
  </div>
</template>

<script>
  // Import Swiper Vue.js components
  import { Swiper, SwiperSlide } from 'swiper/vue';

  // Import Swiper styles
  import 'swiper/css';

  import 'swiper/css/free-mode';
  import 'swiper/css/pagination';

  // import required modules
  import { FreeMode, Pagination } from 'swiper/modules';

  export default {
    components: {
      Swiper,
      SwiperSlide,
    },
    setup() {
      return {
        modules: [FreeMode, Pagination],
      };
    },
  };
</script>
<style>
.Carousel{
  background: #000;
}
#app {
  height: 100%;
}

html,
body {
  position: relative;
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  background: #eee;
  font-family: Helvetica Neue, Helvetica, Arial, sans-serif;
  font-size: 14px;
  color: #000;
}

.Carousel {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* Занимает всю высоту родительского контейнера */
}

.mySwiper {
  width: 80%; /* Ширина Swiper занимает 80% от родительского контейнера */
  height: 80%; /* Высота Swiper занимает 80% от родительского контейнера */
}

.swiper-slide {
  text-align: center;
  font-size: 18px;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.swiper-slide img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
