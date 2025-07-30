<!DOCTYPE html>  <html lang="en">  
<head>  
  <meta charset="UTF-8">  
  <title>Aadhya ❤️ Rowedy</title>  
  <style>  
    html, body {  
      margin: 0;  
      padding: 0;  
      height: 100%;  
      overflow: hidden;  
      background: black;  
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;  
      color: white;  
      display: flex;  
      justify-content: center;  
      align-items: center;  
      position: relative;  
    }  canvas#galaxy {  
  position: absolute;  
  top: 0;  
  left: 0;  
  z-index: 0;  
}  

h1 {  
  font-size: 2.5em;  
  text-align: center;  
  text-shadow: 2px 2px 10px rgba(255,255,255,0.4);  
  animation: pulse 2s infinite;  
  z-index: 2;  
}  

@keyframes pulse {  
  0% { transform: scale(1); }  
  50% { transform: scale(1.1); }  
  100% { transform: scale(1); }  
}  

.heart {  
  position: absolute;  
  top: 20%;  
  left: 50%;  
  width: 100px;  
  height: 90px;  
  margin-left: -50px;  
  background: red;  
  transform: rotate(-45deg);  
  animation: float 4s infinite ease-in-out;  
  z-index: 1;  
}  

.heart::before,  
.heart::after {  
  content: "";  
  position: absolute;  
  width: 100px;  
  height: 90px;  
  background: red;  
  border-radius: 50%;  
}  

.heart::before {  
  top: -50px;  
  left: 0;  
}  

.heart::after {  
  left: 50px;  
  top: 0;  
}  

@keyframes float {  
  0% { transform: translateY(0) rotate(-45deg); }  
  50% { transform: translateY(-20px) rotate(-45deg); }  
  100% { transform: translateY(0) rotate(-45deg); }  
}  

.rain {  
  position: absolute;  
  width: 100%;  
  height: 100%;  
  top: 0;  
  left: 0;  
  z-index: 0;  
  pointer-events: none;  
}  

.drop {  
  position: absolute;  
  width: 2px;  
  height: 10px;  
  background: rgba(255, 255, 255, 0.3);  
  bottom: 100%;  
  animation: fall linear infinite;  
}  

@keyframes fall {  
  to {  
    transform: translateY(110vh);  
  }  
}

  </style>  
</head>  
<body>  <canvas id="galaxy"></canvas>

  <div class="rain"></div>  
  <div class="heart"></div>  
  <h1>Aadhya ❤️ Love Rowedy</h1>  
  <audio id="bgmusic" src="saiyra.mp3" loop></audio>    <script>  
    // Auto play music on first user interaction  
    document.body.addEventListener('click', function () {  
      const music = document.getElementById('bgmusic');  
      music.play();  
    }, { once: true });  
  
    // Rain effect  
    const rain = document.querySelector('.rain');  
    for (let i = 0; i < 100; i++) {  
      const drop = document.createElement('div');  
      drop.classList.add('drop');  
      drop.style.left = Math.random() * 100 + 'vw';  
      drop.style.animationDuration = (0.5 + Math.random()) + 's';  
      drop.style.animationDelay = Math.random() * 5 + 's';  
      rain.appendChild(drop);  
    }  
  
    // Galaxy effect using Canvas  
    const canvas = document.getElementById("galaxy");  
    const ctx = canvas.getContext("2d");  
    let w, h, particles;  
  
    function initGalaxy() {  
      w = canvas.width = window.innerWidth;  
      h = canvas.height = window.innerHeight;  
      particles = [];  
      for (let i = 0; i < 150; i++) {  
        particles.push({  
          x: Math.random() * w,  
          y: Math.random() * h,  
          r: Math.random() * 2,  
          d: Math.random() * 1.5,  
        });  
      }  
    }  
  
    function drawGalaxy() {  
      ctx.clearRect(0, 0, w, h);  
      ctx.fillStyle = "rgba(255,255,255,0.8)";  
      ctx.beginPath();  
      for (let i = 0; i < particles.length; i++) {  
        const p = particles[i];  
        ctx.moveTo(p.x, p.y);  
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2, true);  
      }  
      ctx.fill();  
      updateParticles();  
    }  
  
    function updateParticles() {  
      for (let i = 0; i < particles.length; i++) {  
        const p = particles[i];  
        p.y += p.d;  
        if (p.y > h) {  
          p.y = 0;  
          p.x = Math.random() * w;  
        }  
      }  
    }  
  
    function loop() {  
      drawGalaxy();  
      requestAnimationFrame(loop);  
    }  
  
    initGalaxy();  
    loop();  
  </script>  </body>  
</html>
