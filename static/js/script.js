/*
 * AutoFácil - Script Principal
 * Tarefas: Carrossel, Menu Mobile, Searchbar, Destinos Dinâmicos, Formulários
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    // Inicializar formatação de campos para todas as páginas
    initFormatacaoCampos();

    // ====== CARROSSEL ======
    if (currentPage === 'index') {
        initCarousel();
        initSearchbar();
        initDestinos();
    }

    // ====== MENU MOBILE ======
    if (document.getElementById('menuTrigger')) {
        initMenuMobile();
    }

    // ====== FORMULÁRIOS ======
    if (currentPage === 'cadastro' || currentPage === 'aluguel-mensal' || currentPage === 'login') {
        initFormularios();
    }

    // ====== PÁGINA DE FROTA ======
    if (currentPage === 'frota') {
        initFrota();
    }

    // ====== PÁGINA ALUGUEL MENSAL ======
    if (currentPage === 'aluguel-mensal') {
        initAluguelMensal();
    }

    // Scroll para topo se houver erro (para páginas com Flask)
    if (typeof erro !== 'undefined' && erro) {
        window.scrollTo(0, 0);
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
        if (n >= imagens.length) index = 0;
        if (n < 0) index = imagens.length - 1;

        imagens.forEach(img => img.classList.remove("active"));
        dots.forEach(dot => dot.classList.remove("active"));

        if (imagens[index]) {
            imagens[index].classList.add("active");
            dots[index].classList.add("active");
        }
    }

    function avancarSlide() {
        index++;
        mostrarSlide(index);
    }

    function reiniciarIntervalo() {
        clearInterval(carouselInterval);
        carouselInterval = setInterval(avancarSlide, 5000);
    }

    prevBtn.addEventListener("click", () => {
        index--;
        mostrarSlide(index);
        reiniciarIntervalo();
    });

    nextBtn.addEventListener("click", () => {
        index++;
        mostrarSlide(index);
        reiniciarIntervalo();
    });

    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            index = i;
            mostrarSlide(index);
            reiniciarIntervalo();
        });
    });

    // Iniciar carrossel automático
    carouselInterval = setInterval(avancarSlide, 5000);
    mostrarSlide(index);
}

// ====== SEARCHBAR RESPONSIVA ======
function initSearchbar() {
    function updatePlaceholder() {
        const input = document.querySelector(".marca");
        if (input) {
            input.placeholder = window.innerWidth <= 1000 ? "Pesquisar" : "Digite a marca ou modelo";
        }
    }

    // Posicionamento da searchbar
    const searchbar = document.querySelector('.searchbar');
    const header = document.querySelector('header');
    const carousel = document.querySelector('.carousel');

    if (!searchbar || !header || !carousel) return;

    function positionSearchbar() {
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

    // Event listeners
    window.addEventListener("resize", updatePlaceholder);
    window.addEventListener("resize", positionSearchbar);
    window.addEventListener('scroll', function () {
        if (window.innerWidth > 1000) positionSearchbar();
    });

    // Inicializar
    updatePlaceholder();
    positionSearchbar();
}

// ====== MENU MOBILE ======
function initMenuMobile() {
    const menuTrigger = document.getElementById('menuTrigger');
    const menuPanel = document.getElementById('menuPanel');

    if (!menuTrigger || !menuPanel) return;

    function closeMenu() {
        menuTrigger.classList.remove('open');
        menuTrigger.setAttribute('aria-expanded', 'false');
        menuPanel.classList.remove('open');
    }

    function openMenu() {
        menuTrigger.classList.add('open');
        menuTrigger.setAttribute('aria-expanded', 'true');
        menuPanel.classList.add('open');
    }

    function toggleMenu() {
        if (menuTrigger.classList.contains('open')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    menuTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
    });

    document.addEventListener('click', (e) => {
        if (!menuTrigger.contains(e.target)) closeMenu();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 1000) closeMenu();
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
            col.forEach(name => {
                const li = document.createElement('li');
                li.textContent = name;
                ul.appendChild(li);
            });
            grid.appendChild(ul);
        });
    }

    function ativarPill(pill) {
        // Desativar todas as pills
        pills.forEach(p => {
            p.classList.remove('active');
            p.setAttribute('aria-pressed', 'false');
        });

        // Ativar pill clicada
        pill.classList.add('active');
        pill.setAttribute('aria-pressed', 'true');
        renderCategoria(pill.dataset.cat);
    }

    pills.forEach(btn => {
        btn.addEventListener('click', function () {
            ativarPill(this);
        });

        btn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                ativarPill(btn);
            }
        });
    });

    // Render inicial
    const defaultBtn = document.querySelector('.destinos-filtros .pill.active') || pills[0];
    if (defaultBtn) {
        renderCategoria(defaultBtn.dataset.cat);
    }

    // Re-render em resize
    let resizeTimer = null;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const active = document.querySelector('.destinos-filtros .pill.active');
            if (active) renderCategoria(active.dataset.cat);
        }, 120);
    });
}

// ====== FORMULÁRIOS ======
function initFormularios() {
    // Validação em tempo real para todos os inputs
    const inputs = document.querySelectorAll('input:not([type="submit"]):not([type="button"])');

    inputs.forEach(input => {
        input.addEventListener('blur', function () {
            validarCampo(this);
        });

        // Validação também no input para campos formatados
        if (input.id.includes('cpf') || input.id.includes('cnpj') || input.id.includes('cep') || input.type === 'tel') {
            input.addEventListener('input', function () {
                // Pequeno delay para permitir a formatação
                setTimeout(() => validarCampo(this), 100);
            });
        }
    });

    // Toggle password visibility
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    if (togglePassword && password) {
        togglePassword.addEventListener('click', function () {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.classList.toggle('active');

            // Alterar ícone/texto se necessário
            const icon = this.querySelector('img, i');
            if (icon) {
                if (type === 'text') {
                    icon.alt = 'Ocultar senha';
                    icon.title = 'Ocultar senha';
                } else {
                    icon.alt = 'Mostrar senha';
                    icon.title = 'Mostrar senha';
                }
            }
        });
    }

    // Seleção automática de tipo de conta
    const radios = document.querySelectorAll('.tipo-conta-radio');

    radios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.form) {
                // Pequeno delay para melhor UX
                setTimeout(() => this.form.submit(), 100);
            }
        });
    });
}

// ====== VALIDAÇÃO DE CAMPOS ======
function validarCampo(campo) {
    const valor = campo.value.trim();
    let erro = '';

    const validacoes = {
        'nome': () => {
            if (!valor) return 'Nome completo é obrigatório.';
            if (valor.length < 6) return 'Nome deve ter pelo menos 6 caracteres.';
            if (!/^[A-Za-zÀ-ÿ\s]{6,}$/.test(valor)) return 'Nome deve conter apenas letras e espaços.';
            return '';
        },

        'nome_representante': () => {
            if (!valor) return 'Nome completo é obrigatório.';
            if (valor.length < 6) return 'Nome deve ter pelo menos 6 caracteres.';
            if (!/^[A-Za-zÀ-ÿ\s]{6,}$/.test(valor)) return 'Nome deve conter apenas letras e espaços.';
            return '';
        },

        'nascimento': () => {
            if (!valor) return 'Data de nascimento é obrigatória.';

            const dataNasc = new Date(valor);
            const hoje = new Date();
            const anoNasc = dataNasc.getFullYear();
            const anoAtual = hoje.getFullYear();

            // Verificar se a data é válida
            if (isNaN(dataNasc.getTime())) return 'Data de nascimento inválida.';

            // Verificar limites de ano
            if (anoNasc < 1900) return 'Data de nascimento inválida.';
            if (anoNasc > anoAtual) return 'Data de nascimento não pode ser no futuro.';

            // Calcular idade precisa (considerando mês e dia)
            let idade = anoAtual - anoNasc;
            const mesAtual = hoje.getMonth();
            const diaAtual = hoje.getDate();
            const mesNasc = dataNasc.getMonth();
            const diaNasc = dataNasc.getDate();

            // Ajustar idade se ainda não fez aniversário este ano
            if (mesAtual < mesNasc || (mesAtual === mesNasc && diaAtual < diaNasc)) {
                idade--;
            }

            if (idade < 18) return 'É necessário ter pelo menos 18 anos.';
            if (idade > 120) return 'Data de nascimento inválida.';

            return '';
        },

        'cpf': () => validarCPF(valor),
        'cpf_representante': () => validarCPF(valor),

        'cnpj': () => validarCNPJ(valor),

        'celular': () => validarTelefone(valor, 'celular'),
        'celular_empresa': () => validarTelefone(valor, 'celular'),
        'telefone_empresa': () => validarTelefone(valor, 'fixo'),

        'email': () => validarEmail(valor),
        'email_empresa': () => validarEmail(valor),

        'cep': () => validarCEP(valor),
        'cep_empresa': () => validarCEP(valor),

        'senha': () => validarSenha(valor),
        'senha_empresa': () => validarSenha(valor),

        'confirmar': () => {
            const senha = document.getElementById('senha')?.value || '';
            return valor !== senha ? 'As senhas não coincidem.' : '';
        },

        'confirmar_empresa': () => {
            const senha = document.getElementById('senha_empresa')?.value || '';
            return valor !== senha ? 'As senhas não coincidem.' : '';
        },

        'razao_social': () => {
            if (!valor) return 'Razão social é obrigatória.';
            if (valor.length < 3) return 'Razão social muito curta.';
            if (valor.length > 100) return 'Razão social muito longa.';
            return '';
        },

        'nome_fantasia': () => {
            if (!valor) return 'Nome fantasia é obrigatório.';
            if (valor.length < 3) return 'Nome fantasia muito curto.';
            if (valor.length > 100) return 'Nome fantasia muito longo.';
            return '';
        },

        'cargo_representante': () => {
            if (!valor) return 'Cargo é obrigatório.';
            if (valor.length < 2) return 'Cargo muito curto.';
            return '';
        }
    };

    if (validacoes[campo.id]) {
        erro = validacoes[campo.id]();
    }

    mostrarMensagemErro(campo, erro);
}

// ====== VALIDAÇÕES ESPECÍFICAS ======
function validarCPF(cpf) {
    if (!cpf) return 'CPF é obrigatório.';

    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11) return 'CPF deve conter 11 dígitos.';
    if (/^(\d)\1+$/.test(cpf)) return 'CPF inválido.';

    // Validação dos dígitos verificadores
    let soma = 0, resto;

    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return 'CPF inválido.';

    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return 'CPF inválido.';

    return '';
}

function validarCNPJ(cnpj) {
    if (!cnpj) return 'CNPJ é obrigatório.';

    cnpj = cnpj.replace(/\D/g, '');
    if (cnpj.length !== 14) return 'CNPJ deve conter 14 dígitos.';
    if (/^(\d)\1+$/.test(cnpj)) return 'CNPJ inválido.';

    // Validação dos dígitos verificadores
    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += parseInt(numeros.charAt(tamanho - i)) * pos--;
        if (pos < 2) pos = 9;
    }
    let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(0))) return 'CNPJ inválido.';

    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += parseInt(numeros.charAt(tamanho - i)) * pos--;
        if (pos < 2) pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(1))) return 'CNPJ inválido.';

    return '';
}

function validarTelefone(telefone, tipo) {
    if (!telefone) return tipo === 'celular' ? 'Celular é obrigatório.' : 'Telefone é obrigatório.';

    const numeros = telefone.replace(/\D/g, '');

    if (tipo === 'celular') {
        if (numeros.length < 10 || numeros.length > 11) return 'Número de celular inválido.';
        if (!/^[1-9]{2}9?[6-9][0-9]{7,8}$/.test(numeros)) return 'Número de celular inválido.';
    } else {
        if (numeros.length !== 10) return 'Número de telefone comercial inválido.';
        if (!/^[1-9]{2}[2-5][0-9]{7}$/.test(numeros)) return 'Número de telefone comercial inválido.';
    }

    return '';
}

function validarEmail(email) {
    if (!email) return 'E-mail é obrigatório.';

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) return 'E-mail inválido.';
    if (email.length > 100) return 'E-mail muito longo.';

    return '';
}

function validarCEP(cep) {
    if (!cep) return 'CEP é obrigatório.';

    const cepNumeros = cep.replace(/\D/g, '');
    if (cepNumeros.length !== 8) return 'CEP deve conter 8 dígitos.';
    if (!/^[0-9]{8}$/.test(cepNumeros)) return 'CEP inválido.';

    return '';
}

function validarSenha(senha) {
    if (!senha) return 'Senha é obrigatória.';
    if (senha.length < 8) return 'Senha deve ter pelo menos 8 caracteres.';
    if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(senha)) {
        return 'Senha deve conter letras maiúsculas, minúsculas e números.';
    }
    return '';
}

// ====== EXIBIR MENSAGEM DE ERRO ======
function mostrarMensagemErro(campo, erro) {
    let mensagemErro = campo.parentNode.querySelector('.mensagem-erro');

    if (erro) {
        if (!mensagemErro) {
            mensagemErro = document.createElement('div');
            mensagemErro.className = 'mensagem-erro';
            campo.parentNode.appendChild(mensagemErro);
        }
        mensagemErro.textContent = erro;
        campo.classList.add('erro');
    } else {
        if (mensagemErro) {
            mensagemErro.remove();
        }
        campo.classList.remove('erro');
    }
}

// ====== FORMATAÇÃO DE CAMPOS ======
function initFormatacaoCampos() {
    // Formatação de CPF
    const cpfs = document.querySelectorAll('input[id*="cpf"]');
    cpfs.forEach(cpf => {
        cpf.addEventListener('input', formatarCPF);
    });

    // Formatação de CNPJ
    const cnpjs = document.querySelectorAll('input[id="cnpj"]');
    cnpjs.forEach(cnpj => {
        cnpj.addEventListener('input', formatarCNPJ);
    });

    // Formatação de CEP
    const ceps = document.querySelectorAll('input[id*="cep"]');
    ceps.forEach(cep => {
        cep.addEventListener('input', formatarCEP);
    });

    // Formatação de telefone/celular
    const telefones = document.querySelectorAll('input[type="tel"]');
    telefones.forEach(tel => {
        tel.addEventListener('input', formatarTelefone);
    });
}

function formatarCPF(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.substring(0, 11);

    if (value.length <= 11) {
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }

    e.target.value = value;
}

function formatarCNPJ(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 14) value = value.substring(0, 14);

    if (value.length <= 14) {
        value = value.replace(/(\d{2})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1/$2');
        value = value.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
    }

    e.target.value = value;
}

function formatarCEP(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 8) value = value.substring(0, 8);

    if (value.length > 5) {
        value = value.replace(/(\d{5})(\d)/, '$1-$2');
    }

    e.target.value = value;
}

function formatarTelefone(e) {
    let value = e.target.value.replace(/\D/g, '');

    if (value.length === 11) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (value.length === 10) {
        value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else if (value.length > 6) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else if (value.length > 0) {
        value = value.replace(/(\d{0,2})/, '($1');
    }

    e.target.value = value;
}

// ====== PÁGINA DE FROTA ======
function initFrota() {
    const filtroBtns = document.querySelectorAll('.filtro-btn');
    const aplicarBtn = document.getElementById('aplicar-filtros');
    const limparBtn = document.getElementById('limpar-filtros');

    if (!filtroBtns.length || !aplicarBtn || !limparBtn) return;

    filtroBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            filtroBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });

    aplicarBtn.addEventListener('click', function () {
        alert('Filtros aplicados com sucesso!');
        // Em produção, aqui viria a lógica de filtragem
    });

    limparBtn.addEventListener('click', function () {
        filtroBtns.forEach(btn => btn.classList.remove('active'));
        document.querySelector('[data-categoria="todos"]')?.classList.add('active');

        // Limpar outros filtros se existirem
        ['marca', 'modelo', 'transmissao', 'combustivel', 'preco', 'malas', 'passageiros', 'portas']
            .forEach(id => {
                const element = document.getElementById(id);
                if (element) element.value = '';
            });

        alert('Filtros limpos!');
    });
}

// ====== PÁGINA ALUGUEL MENSAL ======
function initAluguelMensal() {
    const precos = {
        economico: { 1: 89, 3: 69, 6: 49, 12: 39 },
        intermediario: { 1: 119, 3: 99, 6: 79, 12: 69 },
        suv: { 1: 159, 3: 139, 6: 119, 12: 109 },
        luxo: { 1: 299, 3: 279, 6: 259, 12: 239 }
    };

    const categoriasNomes = {
        economico: "Econômico",
        intermediario: "Intermediário",
        suv: "SUV",
        luxo: "Luxo"
    };

    const periodosNomes = {
        1: "1 mês",
        3: "3 meses",
        6: "6 meses",
        12: "12 meses"
    };

    const btnSimular = document.querySelector('.btn-simular');
    if (btnSimular) {
        btnSimular.addEventListener('click', function () {
            const categoria = document.getElementById('categoria')?.value;
            const periodo = document.getElementById('periodo')?.value;

            if (!categoria || !periodo) {
                alert('Por favor, preencha todos os campos para simular.');
                return;
            }

            const precoDiario = precos[categoria]?.[periodo] || 0;
            const precoMensal = precoDiario * 30;

            // Atualizar resultados
            const resultado = document.querySelector('.resultado-conteudo');
            const placeholder = document.querySelector('.resultado-placeholder');

            if (resultado && placeholder) {
                document.getElementById('cat-resultado').textContent = categoriasNomes[categoria] || '';
                document.getElementById('periodo-resultado').textContent = periodosNomes[periodo] || '';
                document.getElementById('diaria-resultado').textContent = `R$ ${precoDiario}`;
                document.getElementById('mensal-resultado').textContent = `R$ ${precoMensal}`;

                placeholder.style.display = 'none';
                resultado.style.display = 'block';
            }
        });
    }

    // FAQ Accordion
    const faqPerguntas = document.querySelectorAll('.faq-pergunta');
    faqPerguntas.forEach(pergunta => {
        pergunta.addEventListener('click', function () {
            const resposta = this.nextElementSibling;
            const toggle = this.querySelector('.faq-toggle');

            // Fechar outras respostas
            document.querySelectorAll('.faq-resposta').forEach(item => {
                if (item !== resposta) {
                    item.style.display = 'none';
                    const otherToggle = item.previousElementSibling.querySelector('.faq-toggle');
                    if (otherToggle) otherToggle.textContent = '+';
                }
            });

            // Alternar resposta atual
            if (resposta.style.display === 'block') {
                resposta.style.display = 'none';
                toggle.textContent = '+';
            } else {
                resposta.style.display = 'block';
                toggle.textContent = '-';
            }
        });
    });
}