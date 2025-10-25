// Shared helper functions for frontend pages
const API_BASE = 'http://localhost:5000/api';

async function postJSON(url, data){
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function getJSON(url){
  const res = await fetch(url);
  return res.json();
}

function navHtml(){
  return `
  <div class="nav">
    <div class="brand">Study📖Planner</div>
    <div class="links">
      <a href="index.html">Home</a>
      <a href="#about">About</a>
      <a href="#features">Features</a>
    </div>
  </div>`;
}

// Mount navbar on pages that have <div id="nav"></div>
document.addEventListener('DOMContentLoaded', ()=>{
  const nav = document.getElementById('nav');
  if(nav) nav.innerHTML = navHtml();
});
