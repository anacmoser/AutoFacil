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
        initLocaisDropdown();
        initDatePicker();
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

    // Adicionar funcionalidade de busca
    function setupSearchFunctionality() {
        const searchForm = document.querySelector('.searchbar form');
        const searchInput = document.querySelector('.searchbar .marca');
        const localInput = document.querySelector('.searchbar .local');
        const dateInput = document.querySelector('.searchbar .date');
        
        if (searchForm && searchInput) {
            // Configurar o formulário para enviar para a rota correta
            searchForm.setAttribute('action', '/frota/buscar');
            searchForm.setAttribute('method', 'GET');
            
            // Configurar os nomes dos campos conforme esperado pelo backend
            searchInput.setAttribute('name', 'termo');
            
            if (localInput) {
                localInput.setAttribute('name', 'local');
            }
            
            if (dateInput) {
                dateInput.setAttribute('name', 'data');
            }
            
            // Adicionar botão de submit invisível para acessibilidade
            const submitButton = document.createElement('button');
            submitButton.setAttribute('type', 'submit');
            submitButton.style.display = 'none';
            submitButton.textContent = 'Buscar';
            searchForm.appendChild(submitButton);
            
            // Adicionar validação no submit
            searchForm.addEventListener('submit', function(e) {
                const searchValue = searchInput.value.trim();
                
                if (!searchValue) {
                    e.preventDefault();
                    // Feedback visual para campo vazio
                    searchInput.style.borderColor = '#ff4444';
                    searchInput.placeholder = 'Digite algo para buscar...';
                    setTimeout(() => {
                        searchInput.style.borderColor = '';
                        updatePlaceholder();
                    }, 2000);
                    searchInput.focus();
                    return;
                }
                
                console.log('Enviando busca:', searchValue); // Para debug
            });
            
            // Adicionar busca com Enter
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    // Deixa o formulário ser submetido normalmente
                    console.log('Enter pressionado, submetendo formulário');
                }
            });
            
            // Limpar feedback visual ao digitar
            searchInput.addEventListener('input', function() {
                this.style.borderColor = '';
                updatePlaceholder();
            });
        }
    }

    // Posicionamento responsivo da searchbar
    function positionSearchbar() {
        const searchbar = document.querySelector('.searchbar');
        const header = document.querySelector('header');
        const carousel = document.querySelector('.carousel');
        
        if (!searchbar || !header || !carousel) return;
        
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

    // Inicialização
    function initializeSearchbar() {
        updatePlaceholder();
        setupSearchFunctionality();
        positionSearchbar();
    }

    // Event Listeners
    window.addEventListener("resize", function() {
        updatePlaceholder();
        positionSearchbar();
    });
    
    window.addEventListener("load", initializeSearchbar);
    
    window.addEventListener('scroll', function () {
        if (window.innerWidth > 1000) positionSearchbar();
    });

    // Inicializar imediatamente se o DOM já estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeSearchbar);
    } else {
        initializeSearchbar();
    }
}

// ====== DROPDOWN DE LOCAIS ======
function initLocaisDropdown() {
    const localInput = document.querySelector('.searchbar .local');
    
    if (!localInput) return;

    // Criar dropdown para locais
    const dropdown = document.createElement('div');
    dropdown.className = 'locais-dropdown';
    dropdown.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        max-height: 200px;
        overflow-y: auto;
        z-index: 1000;
        display: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;

    // Adicionar dropdown após o input
    localInput.parentNode.style.position = 'relative';
    localInput.parentNode.appendChild(dropdown);

    // Buscar locais do servidor
    function carregarLocais() {
        // Mostrar loading
        dropdown.innerHTML = '<div style="padding: 10px; text-align: center; color: #666;">Carregando locais...</div>';
        dropdown.style.display = 'block';

        fetch('/api/locais')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta do servidor');
                }
                return response.json();
            })
            .then(locais => {
                if (locais && locais.length > 0) {
                    dropdown.innerHTML = '';
                    locais.forEach(local => {
                        const option = document.createElement('div');
                        option.className = 'local-option';
                        option.style.cssText = `
                            padding: 10px;
                            cursor: pointer;
                            border-bottom: 1px solid #f0f0f0;
                            transition: background-color 0.2s;
                        `;
                        option.textContent = local.Nome;
                        option.addEventListener('mouseenter', function() {
                            this.style.backgroundColor = '#f5f5f5';
                        });
                        option.addEventListener('mouseleave', function() {
                            this.style.backgroundColor = '';
                        });
                        option.addEventListener('click', function() {
                            localInput.value = local.Nome;
                            dropdown.style.display = 'none';
                        });
                        dropdown.appendChild(option);
                    });
                } else {
                    mostrarLocaisPadrao();
                }
            })
            .catch(error => {
                console.error('Erro ao carregar locais:', error);
                mostrarLocaisPadrao();
            });
    }

    function mostrarLocaisPadrao() {
        // Locais padrão em caso de erro
        const locaisPadrao = [
            'São Paulo - Centro',
            'Rio de Janeiro - Copacabana', 
            'Belo Horizonte - Savassi',
            'Brasília - Asa Sul',
            'Salvador - Barra',
            'Florianópolis - Centro'
        ];
        
        dropdown.innerHTML = '';
        locaisPadrao.forEach(local => {
            const option = document.createElement('div');
            option.className = 'local-option';
            option.style.cssText = `
                padding: 10px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                transition: background-color 0.2s;
            `;
            option.textContent = local;
            option.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f5f5f5';
            });
            option.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
            option.addEventListener('click', function() {
                localInput.value = local;
                dropdown.style.display = 'none';
            });
            dropdown.appendChild(option);
        });
    }

    // Event listeners para o input de local
    localInput.addEventListener('focus', function() {
        if (dropdown.children.length === 0) {
            carregarLocais();
        } else {
            dropdown.style.display = 'block';
        }
    });

    localInput.addEventListener('input', function() {
        const filter = this.value.toLowerCase();
        const options = dropdown.querySelectorAll('.local-option');
        let hasVisibleOptions = false;
        
        options.forEach(option => {
            const text = option.textContent.toLowerCase();
            if (text.includes(filter)) {
                option.style.display = 'block';
                hasVisibleOptions = true;
            } else {
                option.style.display = 'none';
            }
        });
        
        dropdown.style.display = hasVisibleOptions ? 'block' : 'none';
    });

    // Fechar dropdown ao clicar fora
    document.addEventListener('click', function(e) {
        if (!localInput.parentNode.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });

    // Navegação com teclado
    localInput.addEventListener('keydown', function(e) {
        const options = dropdown.querySelectorAll('.local-option:not([style*="display: none"])');
        let currentIndex = -1;

        options.forEach((option, index) => {
            if (option.classList.contains('highlighted')) {
                currentIndex = index;
            }
        });

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const nextIndex = (currentIndex + 1) % options.length;
            options.forEach(opt => opt.classList.remove('highlighted'));
            options[nextIndex].classList.add('highlighted');
            options[nextIndex].style.backgroundColor = '#f0f0f0';
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prevIndex = currentIndex <= 0 ? options.length - 1 : currentIndex - 1;
            options.forEach(opt => opt.classList.remove('highlighted'));
            options[prevIndex].classList.add('highlighted');
            options[prevIndex].style.backgroundColor = '#f0f0f0';
        } else if (e.key === 'Enter' && currentIndex !== -1) {
            e.preventDefault();
            options[currentIndex].click();
        }
    });
}

// ====== CALENDÁRIO PARA DATA ======
function initDatePicker() {
    const dateInput = document.querySelector('.searchbar .date');
    
    if (!dateInput) return;

    // Configurar data mínima como hoje
    const hoje = new Date();
    const dataMinima = hoje.toISOString().split('T')[0];
    
    // Quando o tipo mudar para date, configurar min
    dateInput.addEventListener('focus', function() {
        if (this.type === 'date') {
            this.min = dataMinima;
        }
    });

    // Validar data quando o usuário sair do campo
    dateInput.addEventListener('blur', function() {
        if (this.type === 'date' && this.value) {
            const dataSelecionada = new Date(this.value);
            const dataHoje = new Date(dataMinima);
            
            if (dataSelecionada < dataHoje) {
                this.value = '';
                alert('Por favor, selecione uma data futura.');
            }
        }
    });

    // Impedir datas passadas via teclado
    dateInput.addEventListener('keydown', function(e) {
        if (this.type === 'date') {
            // Permitir apenas navegação e teclas de controle
            if (![
                'Backspace', 'Delete', 'Tab', 'Escape', 'Enter', 
                'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'
            ].includes(e.key)) {
                // Se o usuário tentar digitar manualmente, validar depois
                setTimeout(() => {
                    if (this.value && new Date(this.value) < new Date(dataMinima)) {
                        this.value = '';
                    }
                }, 0);
            }
        }
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