let index = 0;
const imagens = document.querySelectorAll(".carousel img");
const dots = document.querySelectorAll(".dot");
const prevBtn = document.querySelector(".carousel-btn.prev");
const nextBtn = document.querySelector(".carousel-btn.next");

function mostrarSlide(n) {
  if (n >= imagens.length) index = 0;
  if (n < 0) index = imagens.length - 1;

  imagens.forEach(img => img.classList.remove("active"));
  dots.forEach(dot => dot.classList.remove("active"));

  imagens[index].classList.add("active");
  dots[index].classList.add("active");
}

// Botões
prevBtn.addEventListener("click", () => {
  index--;
  mostrarSlide(index);
});

nextBtn.addEventListener("click", () => {
  index++;
  mostrarSlide(index);
});

// Indicadores
dots.forEach((dot, i) => {
  dot.addEventListener("click", () => {
    index = i;
    mostrarSlide(index);
  });
});

// Auto avançar a cada 5s
setInterval(() => {
  index++;
  mostrarSlide(index);
}, 5000);

// Mostrar primeiro ao carregar
mostrarSlide(index);


function updatePlaceholder() {
    const input = document.querySelector(".marca");
    if (window.innerWidth <= 1000) {
        input.placeholder = "Pesquisar";
    } else {
        input.placeholder = "Digite a marca ou modelo";
    }
}

window.addEventListener("resize", updatePlaceholder);
window.addEventListener("load", updatePlaceholder);


// Dropdown do hambúrguer: clique (mobile) e acessibilidade
const menuTrigger = document.getElementById('menuTrigger');
const menuBtn     = document.getElementById('menu');
const menuPanel   = document.getElementById('menuPanel');

function closeMenu(){ menuTrigger.classList.remove('open'); menuTrigger.setAttribute('aria-expanded','false'); }
function openMenu(){ menuTrigger.classList.add('open'); menuTrigger.setAttribute('aria-expanded','true'); }

// Toggle no clique (especialmente útil < 1000px)
menuBtn.addEventListener('click', (e)=>{
  e.stopPropagation();
  if(menuTrigger.classList.contains('open')) closeMenu(); else openMenu();
});

// Fecha ao clicar fora
document.addEventListener('click', (e)=>{
  if(!menuTrigger.contains(e.target)) closeMenu();
});

// Fecha no ESC
document.addEventListener('keydown', (e)=>{
  if(e.key === 'Escape') closeMenu();
});

// Se voltar para desktop, garante estado fechado
window.addEventListener('resize', ()=>{
  if(window.innerWidth > 1000) closeMenu();
});


// === Ajuste fino do posicionamento da searchbar (desktop/tablet e mobile) ===
(function () {
  const searchbar = document.querySelector('.searchbar');
  const header    = document.querySelector('header');
  const carousel  = document.querySelector('.carousel');

  if (!searchbar || !header || !carousel) return;

  function positionSearchbar() {
    // limpa estilos que atrapalham o recálculo
    searchbar.style.top = '';
    searchbar.style.left = '';
    searchbar.style.transform = '';

    const docTop = window.pageYOffset || document.documentElement.scrollTop;

    if (window.innerWidth > 1000) {
      // (3) PC/Tablet: colar no INÍCIO do carousel (sobrepondo o topo)
      const cRect = carousel.getBoundingClientRect();
      const topAbs = cRect.top + docTop; // topo exato do carousel na página

      searchbar.style.position  = 'absolute';
      searchbar.style.top       = `${topAbs}px`;
      searchbar.style.left      = '50%';
      searchbar.style.transform = 'translateX(-50%)';
    } else {
      // (4) Mobile: centralizada verticalmente no header, sem sobrepor
      const hRect = header.getBoundingClientRect();
      const sbH   = searchbar.offsetHeight || 44;

      // centraliza a barra dentro da altura disponível do header
      const topAbs = hRect.top + docTop + Math.max(4, (header.offsetHeight - sbH) / 2);

      searchbar.style.position  = 'absolute';
      searchbar.style.top       = `${topAbs}px`;
      searchbar.style.left      = '50%';
      searchbar.style.transform = 'translateX(-50%)';
    }
  }

  // recalcula em eventos relevantes
  window.addEventListener('load', positionSearchbar);
  window.addEventListener('resize', positionSearchbar);
  window.addEventListener('scroll', function () {
    // Em desktop/tablet, mantém “grudada” ao topo do carousel mesmo se algo acima mudar de altura
    if (window.innerWidth > 1000) positionSearchbar();
  });
})();
