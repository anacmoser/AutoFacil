/*
 * AutoFácil - Script Principal
 * Tarefas: Carrossel, Menu Mobile, Searchbar, Destinos Dinâmicos, Formulários
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

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


    // ====== PÁGINA ALUGUEL MENSAL ======
    if (currentPage === 'aluguel-mensal') {
        initAluguelMensal();
    }

    // Scroll para topo se houver erro
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

    function mostrarSlide(n) {
        if (n >= imagens.length) index = 0;
        if (n < 0) index = imagens.length - 1;

        imagens.forEach(img => img.classList.remove("active"));
        dots.forEach(dot => dot.classList.remove("active"));

        imagens[index].classList.add("active");
        dots[index].classList.add("active");
    }

    prevBtn.addEventListener("click", () => {
        index--;
        mostrarSlide(index);
    });

    nextBtn.addEventListener("click", () => {
        index++;
        mostrarSlide(index);
    });

    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            index = i;
            mostrarSlide(index);
        });
    });

    setInterval(() => {
        index++;
        mostrarSlide(index);
    }, 5000);

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

    window.addEventListener("resize", updatePlaceholder);
    window.addEventListener("load", updatePlaceholder);
    updatePlaceholder();

    // Posicionamento da searchbar
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

// ====== MENU MOBILE ======
function initMenuMobile() {
    const menuTriggers = document.querySelectorAll('.menu-trigger');

    if (!menuTriggers.length) return;

    let hoverTimer;
    let isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    function closeMenu(trigger) {
        trigger.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
        const panel = trigger.querySelector('.menu-panel');
        if (panel) panel.classList.remove('open');
    }

    function openMenu(trigger) {
        // Fecha outros menus abertos
        menuTriggers.forEach(otherTrigger => {
            if (otherTrigger !== trigger && otherTrigger.classList.contains('open')) {
                closeMenu(otherTrigger);
            }
        });
        
        trigger.classList.add('open');
        trigger.setAttribute('aria-expanded', 'true');
        const panel = trigger.querySelector('.menu-panel');
        if (panel) panel.classList.add('open');
    }

    menuTriggers.forEach(trigger => {
        // Para dispositivos com mouse (hover)
        if (!isTouchDevice) {
            trigger.addEventListener('mouseenter', () => {
                clearTimeout(hoverTimer);
                hoverTimer = setTimeout(() => openMenu(trigger), 200);
            });

            trigger.addEventListener('mouseleave', () => {
                clearTimeout(hoverTimer);
                hoverTimer = setTimeout(() => closeMenu(trigger), 300);
            });

            const panel = trigger.querySelector('.menu-panel');
            if (panel) {
                panel.addEventListener('mouseenter', () => {
                    clearTimeout(hoverTimer);
                });

                panel.addEventListener('mouseleave', () => {
                    hoverTimer = setTimeout(() => closeMenu(trigger), 200);
                });
            }
        }

        // Para dispositivos touch (clique) - mantém a funcionalidade original
        trigger.addEventListener('click', (e) => {
            if (isTouchDevice) {
                e.stopPropagation();
                trigger.classList.contains('open') ? closeMenu(trigger) : openMenu(trigger);
            }
        });

        // Fecha ao clicar fora (para ambos os casos)
        document.addEventListener('click', (e) => {
            if (!trigger.contains(e.target)) {
                closeMenu(trigger);
            }
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            menuTriggers.forEach(trigger => closeMenu(trigger));
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 1000) {
            menuTriggers.forEach(trigger => closeMenu(trigger));
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

// ====== FORMULÁRIOS ======
function initFormularios() {
    // Validação em tempo real
    const inputs = document.querySelectorAll('input');

    inputs.forEach(input => {
        input.addEventListener('blur', function () {
            validarCampo(this);
        });
    });

    // Toggle password visibility para TODOS os formulários
    const togglePasswords = document.querySelectorAll('.toggle-password');

    togglePasswords.forEach(toggle => {
        toggle.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const passwordField = document.getElementById(targetId);

            if (passwordField) {
                const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordField.setAttribute('type', type);
                this.classList.toggle('active');
            }
        });
    });

    // Seleção automática de tipo de conta
    const radios = document.querySelectorAll('.tipo-conta-radio');

    radios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.form) this.form.submit();
        });
    });
}

// ====== PÁGINA DE LOGIN ======
function initLogin() {
    // Seleção automática de tipo de conta
    const radios = document.querySelectorAll('.tipo-conta-radio');
    
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.form) {
                this.form.submit();
            }
        });
    });

    // Validação em tempo real para os campos de login
    const inputs = document.querySelectorAll('#user_pf, #user_pj, #password_pf, #password_pj');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validarCampoLogin(this);
        });
    });
}

// ====== VALIDAÇÃO DE CAMPOS DE LOGIN ======
function validarCampoLogin(campo) {
    const valor = campo.value.trim();
    let erro = '';

    const validacoes = {
        'user_pf': () => {
            if (!valor) return 'E-mail ou CPF é obrigatório.';
            const isCPF = /^\d{11}$/.test(valor.replace(/\D/g, ''));
            const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valor);
            
            if (!isCPF && !isEmail) {
                return 'Digite um e-mail válido ou CPF com 11 dígitos.';
            }
            return '';
        },

        'user_pj': () => {
            if (!valor) return 'E-mail ou CNPJ é obrigatório.';
            const isCNPJ = /^\d{14}$/.test(valor.replace(/\D/g, ''));
            const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valor);
            
            if (!isCNPJ && !isEmail) {
                return 'Digite um e-mail válido ou CNPJ com 14 dígitos.';
            }
            return '';
        },

        'password_pf': () => {
            if (!valor) return 'Senha é obrigatória.';
            if (valor.length < 6) return 'Senha deve ter pelo menos 6 caracteres.';
            return '';
        },

        'password_pj': () => {
            if (!valor) return 'Senha é obrigatória.';
            if (valor.length < 6) return 'Senha deve ter pelo menos 6 caracteres.';
            return '';
        }
    };

    if (validacoes[campo.id]) {
        erro = validacoes[campo.id]();
    }

    mostrarMensagemErro(campo, erro);
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
            if (anoNasc > anoAtual) return 'Data de nascimento inválida.';

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

        'celular': () => {
            const celularNumeros = valor.replace(/\D/g, '');
            if (celularNumeros.length < 10 || celularNumeros.length > 11) {
                return 'Número de celular inválido.';
            }
            if (!/^[1-9]{2}9?[6-9][0-9]{7,8}$/.test(celularNumeros)) {
                return 'Número de celular inválido.';
            }
            return '';
        },

        'celular_empresa': () => {
            const celularNumeros = valor.replace(/\D/g, '');
            if (celularNumeros.length < 10 || celularNumeros.length > 11) {
                return 'Número de celular inválido.';
            }
            if (!/^[1-9]{2}9?[6-9][0-9]{7,8}$/.test(celularNumeros)) {
                return 'Número de celular inválido.';
            }
            return '';
        },

        'telefone_empresa': () => {
            const telefoneNumeros = valor.replace(/\D/g, '');
            if (telefoneNumeros.length !== 10) {
                return 'Número de telefone comercial inválido.';
            }
            if (!/^[1-9]{2}[2-5][0-9]{7}$/.test(telefoneNumeros)) {
                return 'Número de telefone comercial inválido.';
            }
            return '';
        },

        'email': () => {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!valor) return 'E-mail é obrigatório.';
            if (!emailRegex.test(valor)) return 'E-mail inválido.';
            if (valor.length > 100) return 'E-mail muito longo.';
            return '';
        },

        'email_empresa': () => {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!valor) return 'E-mail é obrigatório.';
            if (!emailRegex.test(valor)) return 'E-mail inválido.';
            if (valor.length > 100) return 'E-mail muito longo.';
            return '';
        },

        'cep': () => {
            const cepNumeros = valor.replace(/\D/g, '');
            if (cepNumeros.length !== 8) return 'CEP deve conter 8 dígitos.';
            if (!/^[0-9]{8}$/.test(cepNumeros)) return 'CEP inválido.';
            return '';
        },

        'cep_empresa': () => {
            const cepNumeros = valor.replace(/\D/g, '');
            if (cepNumeros.length !== 8) return 'CEP deve conter 8 dígitos.';
            if (!/^[0-9]{8}$/.test(cepNumeros)) return 'CEP inválido.';
            return '';
        },

        'senha': () => {
            if (!valor) return 'Senha é obrigatória.';
            if (valor.length < 8) return 'Senha deve ter pelo menos 8 caracteres.';
            if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(valor)) {
                return 'Senha deve conter letras maiúsculas, minúsculas e números.';
            }
            return '';
        },

        'senha_empresa': () => {
            if (!valor) return 'Senha é obrigatória.';
            if (valor.length < 8) return 'Senha deve ter pelo menos 8 caracteres.';
            if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(valor)) {
                return 'Senha deve conter letras maiúsculas, minúsculas e números.';
            }
            return '';
        },

        'confirmar': () => {
            const senha = document.getElementById('senha').value;
            if (valor !== senha) return 'As senhas não coincidem.';
            return '';
        },

        'confirmar_empresa': () => {
            const senha = document.getElementById('senha_empresa').value;
            if (valor !== senha) return 'As senhas não coincidem.';
            return '';
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

// ====== VALIDAÇÃO DE CPF ======
function validarCPF(cpf) {
    if (!cpf) return 'CPF é obrigatório.';

    // Remove caracteres não numéricos
    cpf = cpf.replace(/\D/g, '');

    // Verifica se tem 11 dígitos
    if (cpf.length !== 11) return 'CPF deve conter 11 dígitos.';

    // Verifica se não é uma sequência de números iguais
    if (/^(\d)\1+$/.test(cpf)) return 'CPF inválido.';

    // Validação dos dígitos verificadores
    let soma = 0;
    let resto;

    // Primeiro dígito verificador
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return 'CPF inválido.';

    // Segundo dígito verificador
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return 'CPF inválido.';

    return '';
}

// ====== VALIDAÇÃO DE CNPJ ======
function validarCNPJ(cnpj) {
    if (!cnpj) return 'CNPJ é obrigatório.';

    // Remove caracteres não numéricos
    cnpj = cnpj.replace(/\D/g, '');

    // Verifica se tem 14 dígitos
    if (cnpj.length !== 14) return 'CNPJ deve conter 14 dígitos.';

    // Verifica se não é uma sequência de números iguais
    if (/^(\d)\1+$/.test(cnpj)) return 'CNPJ inválido.';

    // Validação dos dígitos verificadores
    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    // Primeiro dígito verificador
    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }
    let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(0))) return 'CNPJ inválido.';

    // Segundo dígito verificador
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(1))) return 'CNPJ inválido.';

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
        cpf.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.substring(0, 11);

            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            }

            e.target.value = value;
        });
    });

    // Formatação de CNPJ
    const cnpjs = document.querySelectorAll('input[id="cnpj"]');
    cnpjs.forEach(cnpj => {
        cnpj.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 14) value = value.substring(0, 14);

            if (value.length <= 14) {
                value = value.replace(/(\d{2})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1/$2');
                value = value.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
            }

            e.target.value = value;
        });
    });

    // Formatação de CEP
    const ceps = document.querySelectorAll('input[id*="cep"]');
    ceps.forEach(cep => {
        cep.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 8) value = value.substring(0, 8);

            if (value.length > 5) {
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            }

            e.target.value = value;
        });
    });

    // Formatação de telefone/celular
    const telefones = document.querySelectorAll('input[type="tel"]');
    telefones.forEach(tel => {
        tel.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length === 11) { // Celular com DDD + 9 dígitos
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            } else if (value.length === 10) { // Telefone fixo
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            } else if (value.length > 6) {
                value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
            } else if (value.length > 0) {
                value = value.replace(/(\d{0,2})/, '($1');
            }

            e.target.value = value;
        });
    });
}

// Inicializar formatação quando a página carregar
document.addEventListener('DOMContentLoaded', function () {
    initFormatacaoCampos();
});


// ====== PÁGINA DE FROTA ======


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

            document.getElementById('cat-resultado').textContent = categoriasNomes[categoria] || '';
            document.getElementById('periodo-resultado').textContent = periodosNomes[periodo] || '';
            document.getElementById('diaria-resultado').textContent = `R$ ${precoDiario}`;
            document.getElementById('mensal-resultado').textContent = `R$ ${precoMensal}`;

            document.querySelector('.resultado-placeholder').style.display = 'none';
            document.querySelector('.resultado-conteudo').style.display = 'block';
        });
    }

    // FAQ Accordion
    const faqPerguntas = document.querySelectorAll('.faq-pergunta');
    faqPerguntas.forEach(pergunta => {
        pergunta.addEventListener('click', function () {
            const resposta = this.nextElementSibling;
            const toggle = this.querySelector('.faq-toggle');

            document.querySelectorAll('.faq-resposta').forEach(item => {
                if (item !== resposta) {
                    item.style.display = 'none';
                    item.previousElementSibling.querySelector('.faq-toggle').textContent = '+';
                }
            });

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
