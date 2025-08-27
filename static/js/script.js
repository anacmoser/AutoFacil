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
