<template>
    <div class="wrapper">
      <!-- Canvas for starfield animation -->
      <canvas ref="canvas"></canvas>
      <SearchBar />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  
  const canvas = ref<HTMLCanvasElement | null>(null);
  let ctx: CanvasRenderingContext2D | null = null;
  const stars: { x: number; y: number; radius: number; speed: number; direction: number }[] = [];
  
  function initStars() {
    if (!canvas.value) return;
    ctx = canvas.value.getContext('2d');
    if (!ctx) return;
  
    canvas.value.width = window.innerWidth;
    canvas.value.height = window.innerHeight;
  
    const centerX = canvas.value.width / 2;
    const centerY = canvas.value.height / 2;
  
    for (let i = 0; i < 100; i++) {
      const angle = Math.random() * Math.PI * 2; // Random angle in radians
      const radius = Math.random() * (canvas.value.width / 2); // Random radius within canvas
      const speed = Math.random() * 1 + 0.5; // Increase speed (adjust the range as needed)
  
      stars.push({
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius,
        radius: Math.random() * 2, // Initial random radius
        speed,
        direction: angle // Store direction instead of angle
      });
    }
  
    drawStars();
  }
  
  function drawStars() {
    if (!ctx || !canvas.value) return;
  
    // Create gradient background
    const gradient = ctx.createRadialGradient(
      canvas.value.width / 2,
      canvas.value.height / 2,
      0,
      canvas.value.width / 2,
      canvas.value.height / 2,
      Math.max(canvas.value.width, canvas.value.height)
    );
    gradient.addColorStop(0, '#00040a'); // Center color (black)
    gradient.addColorStop(1, '#05204d');
  
    // Fill canvas with gradient
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.value.width, canvas.value.height);
  
    const centerX = canvas.value.width / 2;
    const centerY = canvas.value.height / 2;
  
    for (const star of stars) {
      ctx.beginPath();
      ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
      ctx.fillStyle = 'white';
      ctx.fill();
      ctx.closePath();
  
      // Move star outward based on direction and speed
      star.x += Math.cos(star.direction) * star.speed;
      star.y += Math.sin(star.direction) * star.speed;
  
      // Increase the size of the star slightly over time
      star.radius += 0.01;
  
      if (star.radius > 3) star.radius = 0; // Reset radius if it exceeds a certain value
  
      // Wrap stars around the canvas edges
      if (star.x < 0 || star.x > canvas.value.width || star.y < 0 || star.y > canvas.value.height) {
        const angle = Math.random() * Math.PI * 2; // Generate a new random angle
        const newRadius = Math.random() * (canvas.value.width / 2); // Generate a new random radius
        star.x = centerX + Math.cos(angle) * newRadius;
        star.y = centerY + Math.sin(angle) * newRadius;
        star.radius = Math.random() * 2; // Reset radius
        star.direction = angle; // Update direction
      }
    }
  
    requestAnimationFrame(drawStars);
  }
  
  onMounted(() => {
    initStars();
    window.addEventListener('resize', initStars);
  });
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', initStars);
  });
  </script>
  
  <style scoped>
  * {
    margin: 0;
    padding: 0;
  }
  
  .wrapper {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }
  
  canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  </style>
  