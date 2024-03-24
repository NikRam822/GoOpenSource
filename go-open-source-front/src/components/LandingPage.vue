<template>
  <div class="WelcomePageBody">
    <div class="logo" :style="{ 'background-image': 'url(' + logoUrl + ')' }"></div>
    <section class="layers">
      <div class="layers__container">
        <div class="layers__item layer-1"
          :style="{ 'background-image': 'url(' + layer1Url + ')', 'transform': 'scale(0.98)' }"></div>
        <div class="layers__item layer-3">
          <div class="hero-content">
            <h1 class="hero-text">Исследуй<span style="margin-top: 5px;">Понимай</span></h1>
            <div class="wrap" :style="{ 'margin': '5px' }">
              <button class="button" @click="handleButtonClick">Submit</button>
            </div>
          </div>
        </div>
        <div class="layers__item layer-2" :style="{ 'background-image': 'url(' + layer2Url + ')' }"></div>
      </div>
    </section>
  </div>
</template>

<script>
import router from "@/router";
import logoImg from "@/assets/img/logo.svg";
import layer1Img from "@/assets/img/blob1.gif";
import layer2Img from "@/assets/img/layer-2.png";

export default {
  name: 'WelcomePage',
  data() {
    return {
      logoUrl: logoImg,
      layer1Url: layer1Img,
      layer2Url: layer2Img
    };
  },
  methods: {
    async handleButtonClick() {
      document.querySelector('.logo').classList.add('fade-out-logo');
      document.querySelector('.button').classList.add('fade-out');
      document.querySelector('.hero-text').classList.add('fade-out');
      document.querySelector('.layers__item.layer-3').classList.add('fade-out');
      document.querySelector('.layers__item.layer-1').classList.add('fade-out');
      document.querySelector('.layers__item.layer-2').classList.add('fade-out');

      setTimeout(async () => {
        try {
          await router.push('/search');
        } catch (error) {
          console.error('Error navigating to about page:', error);
        }
      }, 1500);
    },
    async setupMouseMoveListener() {
      document.addEventListener('mousemove', this.handleMouseMove);
    },
    handleMouseMove(e) {
      Object.assign(document.documentElement, {
        style: `
          --move-x: ${(e.clientX - window.innerWidth / 2) * -0.005}deg;
          --move-y: ${(e.clientY - window.innerHeight / 2) * 0.01}deg;
        `
      });
    },
    randomNum(max, min) {
      return Math.floor(Math.random() * max) + min;
    },
  },
  mounted() {
    this.setupMouseMoveListener();
  }
};

</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Alegreya+Sans+SC:wght@300&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --index: calc(1vw + 1vh);
  --transition: 1.5s cubic-bezier(.05, .5, 0, 1);
}

.WelcomePageBody {
  background-color: white;
  color: #fff;
  font-family: Roboto;
}

.WelcomePageBody .logo {
  --logo-size: calc(var(--index) * 9);
  width: var(--logo-size);
  height: var(--logo-size);
  background-repeat: no-repeat;
  position: absolute;
  left: calc(51% - calc(var(--logo-size) / 2));
  top: calc(var(--index) * 2.8);
  z-index: 1;
}

.WelcomePageBody .layers {
  perspective: 1000px;
  overflow: hidden;
}

.WelcomePageBody .layers__container {
  height: 100vh;
  min-height: 500px;
  transform-style: preserve-3d;
  transform: rotateX(var(--move-y)) rotateY(var(--move-x));
  will-change: transform;
  transition: transform var(--transition);
}

.WelcomePageBody .layers__item {
  position: absolute;
  inset: -5vw;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.WelcomePageBody .layer-1 {
  transform: translateZ(-55px) scale(1.26);
}

.WelcomePageBody .layer-2 {
  transform: translateY(130px) scale(1.2);
}

.WelcomePageBody .layer-3 {
  transform: translateZ(180px) scale(.8);
}

.WelcomePageBody .hero-content {
  font-size: calc(var(--index) * 2.5);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: calc(var(--index) * -.15);
  line-height: 1.35em;
  margin-top: calc(var(--index) * 5.5);
}

.WelcomePageBody .hero-content span {
  display: block;
}

.WelcomePageBody .hero-content__p {
  text-transform: none;
  font-family: Roboto;
  letter-spacing: normal;
  font-size: calc(var(--index) *1);
  line-height: 3;
}

.WelcomePageBody .button-start {
  font-family: Arial;
  font-weight: 600;
  text-transform: uppercase;
  font-size: calc(var(--index) * .71);
  letter-spacing: -.02vw;
  padding: calc(var(--index) * .02) calc(var(--index) * 1.25);
  background-color: white;
  /* Белый фон */
  color: black;
  /* Черный текст */
  border-radius: 10em;
  border: white 0px solid;
  outline: none;
  cursor: pointer;
  margin-top: calc(var(--index) * 2.5);
  transition: background-color 0.3s, color 0.3s;
  /* Плавное изменение цвета при наведении */
}

.WelcomePageBody .button-start:hover {
  background-color: black;
  color: white;
}

.WelcomePageBody .move-right {
  transition: transform 1s ease-out;
  transform: translateX(100%);
}

.WelcomePageBody .fade-out {
  opacity: 0;
  transition: opacity 1s ease-out;
}

.WelcomePageBody .fade-out-logo {
  opacity: 0;
  transition: opacity 1s ease-out;
}
</style>

<style>
.WelcomePageBody html,
body {
  height: 100%;
}

.WelcomePageBody .wrap {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.WelcomePageBody .button {
  min-width: 300px;
  min-height: 60px;
  font-family: 'Nunito', sans-serif;
  font-size: 22px;
  text-transform: uppercase;
  letter-spacing: 1.3px;
  font-weight: 700;
  color: #313133;
  background: #4FD1C5;
  background: linear-gradient(90deg, rgba(129, 230, 217, 1) 0%, rgba(79, 209, 197, 1) 100%);
  border: none;
  border-radius: 1000px;
  box-shadow: 12px 12px 24px rgba(79, 209, 197, .64);
  transition: all 0.3s ease-in-out 0s;
  cursor: pointer;
  outline: none;
  position: relative;
  padding: 10px;
}

.WelcomePageBody button::before {
  content: '';
  border-radius: 1000px;
  min-width: calc(300px + 12px);
  min-height: calc(60px + 12px);
  border: 6px solid #00FFCB;
  box-shadow: 0 0 60px rgba(0, 255, 203, .64);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: all .3s ease-in-out 0s;
}

.WelcomePageBody .button:hover,
.button:focus {
  color: #313133;
  transform: translateY(-6px);
}

.WelcomePageBody button:hover::before,
button:focus::before {
  opacity: 1;
}

.WelcomePageBody button::after {
  content: '';
  width: 30px;
  height: 30px;
  border-radius: 100%;
  border: 6px solid #00FFCB;
  position: absolute;
  z-index: -1;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: ring 1.5s infinite;
}

.WelcomePageBody button:hover::after,
button:focus::after {
  animation: none;
  display: none;
}

@keyframes ring {
  0% {
    width: 30px;
    height: 30px;
    opacity: 1;
  }

  100% {
    width: 300px;
    height: 300px;
    opacity: 0;
  }
}
</style>
