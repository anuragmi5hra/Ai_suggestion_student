// Shared helper functions for frontend pages
const API_BASE = 'https://ai-suggestion-student.onrender.com/';

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
    <div class="logo">
  <span class="logo-icon">📘</span>
  <span class="logo-text">Study<span class="highlight">Planner</span></span>
</div>

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
