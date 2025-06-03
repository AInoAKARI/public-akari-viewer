// ui/pulse_ui.js
// Draws a pulsing circle in bottom-left representing emotion resonance.

const canvas = document.getElementById('pulseCanvas');
const ctx = canvas.getContext('2d');

function resize() {
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
}
resize();
window.addEventListener('resize', resize);

let intensity = 0; // 0..1
let mode = 'idle'; // 'heavy', 'tempo', 'idle'

async function fetchVectors() {
  try {
    const res = await fetch('https://gist.githubusercontent.com/AInoAKARI/98729d40c48b2ab8c5a5b2b421baa8/raw'); // TODO: point to JSON
    const data = await res.json();
    const last = data[data.length - 1] || {};
    intensity = Math.min(1, (last.vectors ? last.vectors.length : 0) / 10);
    mode = intensity > 0.7 ? 'heavy' : intensity > 0.3 ? 'tempo' : 'idle';
  } catch (e) {
    console.error(e);
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const t = Date.now() / 1000;
  let radius = 50 + Math.sin(t * 2) * 10 * intensity;

  // color based on mode
  let color = '#444';
  if (mode === 'heavy') color = '#ffffff';
  else if (mode === 'tempo') color = `hsl(${(t*120)%360},100%,60%)`;

  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(canvas.width / 2, canvas.height / 2, radius, 0, Math.PI * 2);
  ctx.fill();

  requestAnimationFrame(draw);
}

setInterval(fetchVectors, 5000);
draw();
