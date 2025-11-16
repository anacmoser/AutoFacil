/*
 * AutoFácil - Script Base
 * Funcionalidades comuns a todas as páginas
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    // ====== MENU MOBILE ======
    if (document.querySelector('.menu-trigger')) {
        initMenuMobile();
    }

    // ====== ACESSIBILIDADE ====== 
    initAcessibilidade();

    // ====== FORMATAÇÃO DE CAMPOS ======
    initFormatacaoCampos();

    // Scroll para topo se houver erro
    if (typeof erro !== 'undefined' && erro) {
        window.scrollTo(0, 0);
    }
});

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

        trigger.addEventListener('click', (e) => {
            if (isTouchDevice) {
                e.stopPropagation();
                trigger.classList.contains('open') ? closeMenu(trigger) : openMenu(trigger);
            }
        });

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

// ====== SISTEMA DE ACESSIBILIDADE ======
function initAcessibilidade() {
    const acessibilidadeTrigger = document.querySelector('.nav-right .menu-trigger:nth-child(2)');

    if (!acessibilidadeTrigger) return;

    const configPadrao = {
        tamanhoFonte: 1,
        altoContraste: false
    };

    function carregarConfiguracoes() {
        const salvo = localStorage.getItem('acessibilidadeConfig');
        if (salvo) {
            const config = JSON.parse(salvo);
            config.tamanhoFonte = parseFloat(config.tamanhoFonte) || 1;
            return config;
        }
        return {...configPadrao};
    }

    function salvarConfiguracoes(config) {
        localStorage.setItem('acessibilidadeConfig', JSON.stringify(config));
    }

    function aplicarConfiguracoes(config) {
        const html = document.documentElement;
        
        html.classList.remove('fonte-normal', 'fonte-grande', 'fonte-muito-grande', 'fonte-super-grande', 'fonte-maximo', 'alto-contraste');
        
        if (config.tamanhoFonte === 1) {
            html.classList.add('fonte-normal');
        } else if (config.tamanhoFonte === 1.25) {
            html.classList.add('fonte-grande');
        } else if (config.tamanhoFonte === 1.5) {
            html.classList.add('fonte-muito-grande');
        } else if (config.tamanhoFonte === 1.75) {
            html.classList.add('fonte-super-grande');
        } else if (config.tamanhoFonte === 2.0) {
            html.classList.add('fonte-maximo');
        }
        
        if (config.altoContraste) {
            html.classList.add('alto-contraste');
        }
    }

    let configAtual = carregarConfiguracoes();
    aplicarConfiguracoes(configAtual);

    const botoes = document.querySelectorAll('.acessibilidade-btn');

    botoes.forEach(botao => {
        botao.addEventListener('click', function() {
            const acao = this.dataset.action;

            switch(acao) {
                case 'aumentar-fonte':
                    if (configAtual.tamanhoFonte < 2.0) {
                        configAtual.tamanhoFonte = parseFloat((configAtual.tamanhoFonte + 0.25).toFixed(2));
                    }
                    break;
                    
                case 'diminuir-fonte':
                    if (configAtual.tamanhoFonte > 1) {
                        configAtual.tamanhoFonte = parseFloat((configAtual.tamanhoFonte - 0.25).toFixed(2));
                    }
                    break;
                    
                case 'alto-contraste':
                    configAtual.altoContraste = !configAtual.altoContraste;
                    this.querySelector('span').textContent = configAtual.altoContraste ? '☑' : '▣';
                    break;
                    
                case 'resetar':
                    configAtual = {...configPadrao};
                    document.querySelector('[data-action="alto-contraste"] span').textContent = '▣';
                    break;
            }
            
            aplicarConfiguracoes(configAtual);
            salvarConfiguracoes(configAtual);
            
            const menuPanel = acessibilidadeTrigger.querySelector('.menu-panel');
            if (menuPanel) {
                menuPanel.classList.remove('open');
                acessibilidadeTrigger.classList.remove('open');
                acessibilidadeTrigger.setAttribute('aria-expanded', 'false');
            }
        });
    });
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
        });
    });
}