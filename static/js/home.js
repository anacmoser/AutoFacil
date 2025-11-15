/*
 * AutoFácil - Script Home
 * Funcionalidades específicas da página inicial
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    if (currentPage === 'index') {
        initCarousel();
        initSearchbar();
        initDestinos();
    }
});

// ====== CARROSSEL ======
function initCarousel() {
    const imagens = document.querySelectorAll(".carousel img");
    const dots = document.querySelectorAll(".dot");
    const prevBtn = document.querySelector(".carousel-btn.prev");
    const nextBtn = document.querySelector(".carousel-btn.next");

    if (!imagens.length || !prevBtn || !nextBtn) return;

    let index = 0;
    let carouselInterval;

    function mostrarSlide(n) {
        imagens.forEach(img => img.classList.remove("active"));
        dots.forEach(dot => dot.classList.remove("active"));

        index = n;
        if (index >= imagens.length) index = 0;
        if (index < 0) index = imagens.length - 1;

        imagens[index].classList.add("active");
        dots[index].classList.add("active");
    }

    function nextSlide() {
        mostrarSlide(index + 1);
    }

    function prevSlide() {
        mostrarSlide(index - 1);
    }

    prevBtn.addEventListener("click", () => {
        prevSlide();
        resetInterval();
    });

    nextBtn.addEventListener("click", () => {
        nextSlide();
        resetInterval();
    });

    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            mostrarSlide(i);
            resetInterval();
        });
    });

    function startInterval() {
        carouselInterval = setInterval(nextSlide, 5000);
    }

    function resetInterval() {
        clearInterval(carouselInterval);
        startInterval();
    }

    mostrarSlide(0);
    startInterval();
}

// ====== SEARCHBAR RESPONSIVA ======
function initSearchbar() {
    function updatePlaceholder() {
        const input = document.querySelector(".marca");
        if (input) {
            input.placeholder = window.innerWidth <= 1000 ? "Pesquisar" : "Digite a marca ou modelo";
        }
    }

    window.addEventListener("resize", updatePlaceholder);
    window.addEventListener("load", updatePlaceholder);
    updatePlaceholder();

    const searchbar = document.querySelector('.searchbar');
    const header = document.querySelector('header');
    const carousel = document.querySelector('.carousel');

    if (!searchbar || !header || !carousel) return;

    function positionSearchbar() {
        searchbar.style.top = '';
        searchbar.style.left = '';
        searchbar.style.transform = '';

        const docTop = window.pageYOffset || document.documentElement.scrollTop;

        if (window.innerWidth > 1000) {
            const cRect = carousel.getBoundingClientRect();
            const topAbs = cRect.top + docTop;

            searchbar.style.position = 'absolute';
            searchbar.style.top = `${topAbs}px`;
            searchbar.style.left = '50%';
            searchbar.style.transform = 'translateX(-50%)';
        } else {
            const hRect = header.getBoundingClientRect();
            const sbH = searchbar.offsetHeight || 44;
            const topAbs = hRect.top + docTop + Math.max(4, (header.offsetHeight - sbH) / 2);

            searchbar.style.position = 'absolute';
            searchbar.style.top = `${topAbs}px`;
            searchbar.style.left = '50%';
            searchbar.style.transform = 'translateX(-50%)';
        }
    }

    window.addEventListener('load', positionSearchbar);
    window.addEventListener('resize', positionSearchbar);
    window.addEventListener('scroll', function () {
        if (window.innerWidth > 1000) positionSearchbar();
    });
}

// ====== DESTINOS DINÂMICOS ======
function initDestinos() {
    const destinosData = {
        ferias: [
            "Porto Seguro, BA", "Maceió, AL", "João Pessoa, PB", "Ubatuba, SP",
            "Cabo Frio, RJ", "Natal, RN", "Ilhéus, BA", "Florianópolis, SC"
        ],
        roteiros: [
            "São Paulo, SP", "Campinas, SP", "Curitiba, PR", "Recife, PE",
            "Brasília, DF", "Goiânia, GO", "Belo Horizonte, MG", "Porto Alegre, RS"
        ],
        moto: [
            "Chapada Diamantina, BA", "Serra do Rio do Rastro, SC", "São Thomé das Letras, MG", "Estrada Real, MG",
            "Petrópolis, RJ", "Serra da Canastra, MG", "Alto Paraíso, GO", "Carrancas, MG"
        ],
        natureza: [
            "Brotas, SP", "Itacaré, BA", "Bonito, MS", "Bonito (MS) - roteiros",
            "Alto Paraíso, GO", "Carrancas, MG", "Recife, PE", "Nova Friburgo, RJ"
        ],
        familia: [
            "Caldas Novas, GO", "Foz do Iguaçu, PR", "Balneário Camboriú, SC", "Poços de Caldas, MG",
            "Ólimpia, SP", "Praia do Forte, BA", "Canela, RS", "Beto Carrero (Penha, SC)"
        ]
    };

    const grid = document.getElementById('destinosGrid');
    const pills = Array.from(document.querySelectorAll('.destinos-filtros .pill'));

    if (!grid || !pills.length) return;

    function splitColumns(items, cols = 4) {
        const perCol = Math.ceil(items.length / cols);
        const columns = [];
        for (let i = 0; i < cols; i++) {
            columns.push(items.slice(i * perCol, (i + 1) * perCol));
        }
        return columns;
    }

    function renderCategoria(cat) {
        const items = destinosData[cat] || [];
        const cols = window.innerWidth <= 680 ? 2 : (window.innerWidth <= 1000 ? 3 : 4);
        const columns = splitColumns(items, cols);

        grid.innerHTML = '';
        columns.forEach(col => {
            const ul = document.createElement('ul');
            ul.className = 'destinos-col';
            if (col.length === 0) {
                const li = document.createElement('li');
                li.textContent = '';
                ul.appendChild(li);
            } else {
                col.forEach(name => {
                    const li = document.createElement('li');
                    li.textContent = name;
                    ul.appendChild(li);
                });
            }
            grid.appendChild(ul);
        });
    }

    pills.forEach(btn => {
        btn.addEventListener('click', function () {
            const active = document.querySelector('.destinos-filtros .pill.active');
            if (active) {
                active.classList.remove('active');
                active.setAttribute('aria-pressed', 'false');
            }
            this.classList.add('active');
            this.setAttribute('aria-pressed', 'true');

            renderCategoria(this.dataset.cat);
        });

        btn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                btn.click();
            }
        });
    });

    const defaultBtn = document.querySelector('.destinos-filtros .pill.active') || pills[0];
    if (defaultBtn) {
        renderCategoria(defaultBtn.dataset.cat);
    }

    let resizeTimer = null;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const active = document.querySelector('.destinos-filtros .pill.active');
            if (active) renderCategoria(active.dataset.cat);
        }, 120);
    });
}