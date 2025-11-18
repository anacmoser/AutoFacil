/*
 * AutoFácil - Script Base
 * Funcionalidades comuns a todas as páginas
 */

// ====== MENU MOBILE ======
function initMenuMobile() {
    // Função placeholder - substitua pelo seu código real se necessário
    console.log('Menu mobile inicializado');
}

// ====== SISTEMA DE ACESSIBILIDADE ======
function initAcessibilidade() {
    console.log('=== INICIANDO ACESSIBILIDADE ===');
    
    // Método mais flexível para encontrar o trigger
    const acessibilidadeTrigger = document.querySelector('.menu-trigger [title="Acessibilidade"], .menu-trigger [alt*="acessibilidade"], .nav-right .menu-trigger:nth-child(2)');
    
    console.log('Trigger encontrado:', acessibilidadeTrigger);
    
    if (!acessibilidadeTrigger) {
        console.warn('❌ Trigger de acessibilidade não encontrado');
        console.log('Tentando seletor alternativo...');
        
        // Tentativa alternativa
        const triggers = document.querySelectorAll('.menu-trigger');
        console.log('Todos os menu-triggers:', triggers);
        return;
    }

    const configPadrao = {
        tamanhoFonte: 1,
        altoContraste: false
    };

    function carregarConfiguracoes() {
        try {
            const salvo = localStorage.getItem('acessibilidadeConfig');
            console.log('Configuração salva no localStorage:', salvo);
            
            if (salvo) {
                const config = JSON.parse(salvo);
                config.tamanhoFonte = parseFloat(config.tamanhoFonte) || 1;
                return config;
            }
        } catch (e) {
            console.error('Erro ao carregar configurações:', e);
        }
        return {...configPadrao};
    }

    function salvarConfiguracoes(config) {
        try {
            localStorage.setItem('acessibilidadeConfig', JSON.stringify(config));
            console.log('Configuração salva:', config);
        } catch (e) {
            console.error('Erro ao salvar configurações:', e);
        }
    }

    function aplicarConfiguracoes(config) {
        const html = document.documentElement;
        
        console.log('Aplicando configurações:', config);
        
        // Remove todas as classes de fonte e contraste
        const classesParaRemover = ['fonte-normal', 'fonte-grande', 'fonte-muito-grande', 'fonte-super-grande', 'fonte-maximo', 'alto-contraste'];
        classesParaRemover.forEach(classe => html.classList.remove(classe));
        
        // Aplica a classe de fonte correspondente
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
        
        // Aplica alto contraste se necessário
        if (config.altoContraste) {
            html.classList.add('alto-contraste');
        }
        
        console.log('✅ Configuração aplicada - Tamanho:', config.tamanhoFonte, 'Contraste:', config.altoContraste);
        console.log('Classes no HTML:', html.className);
    }

    // Carregar e aplicar configurações
    let configAtual = carregarConfiguracoes();
    aplicarConfiguracoes(configAtual);

    // Adicionar event listeners aos botões
    const botoes = document.querySelectorAll('.acessibilidade-btn');
    console.log('Botões de acessibilidade encontrados:', botoes.length);
    
    botoes.forEach((botao, index) => {
        console.log(`Botão ${index + 1}:`, botao.dataset.action);
        
        botao.addEventListener('click', function(e) {
            e.preventDefault();
            const acao = this.dataset.action;
            console.log('🎯 Botão clicado:', acao);

            switch(acao) {
                case 'aumentar-fonte':
                    if (configAtual.tamanhoFonte < 2.0) {
                        configAtual.tamanhoFonte = parseFloat((configAtual.tamanhoFonte + 0.25).toFixed(2));
                        console.log('📈 Novo tamanho:', configAtual.tamanhoFonte);
                    } else {
                        console.log('⚠️ Tamanho máximo atingido');
                    }
                    break;
                    
                case 'diminuir-fonte':
                    if (configAtual.tamanhoFonte > 1) {
                        configAtual.tamanhoFonte = parseFloat((configAtual.tamanhoFonte - 0.25).toFixed(2));
                        console.log('📉 Novo tamanho:', configAtual.tamanhoFonte);
                    } else {
                        console.log('⚠️ Tamanho mínimo atingido');
                    }
                    break;
                    
                case 'alto-contraste':
                    configAtual.altoContraste = !configAtual.altoContraste;
                    const spanContraste = this.querySelector('span');
                    if (spanContraste) {
                        spanContraste.textContent = configAtual.altoContraste ? '☑' : '▣';
                    }
                    console.log('🎨 Alto contraste:', configAtual.altoContraste);
                    break;
                    
                case 'resetar':
                    configAtual = {...configPadrao};
                    const spanReset = document.querySelector('[data-action="alto-contraste"] span');
                    if (spanReset) {
                        spanReset.textContent = '▣';
                    }
                    console.log('🔄 Configurações resetadas');
                    break;
            }
            
            aplicarConfiguracoes(configAtual);
            salvarConfiguracoes(configAtual);
        });
    });
    
    console.log('✅ Acessibilidade inicializada com sucesso');
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

// ====== INICIALIZAÇÃO GERAL ======
document.addEventListener('DOMContentLoaded', function () {
    console.log('=== DOM CARREGADO - INICIALIZANDO ===');
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
    
    console.log('=== TODAS AS FUNÇÕES INICIALIZADAS ===');
});