/**
 * AutoFácil - Script da Página de Pagamento
 * Funcionalidades: Seleção de método de pagamento, validações, formatação de campos
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos principais
    const metodoCards = document.querySelectorAll('.metodo-pagamento-card');
    const cartaoForm = document.getElementById('cartao-form');
    const parcelamentoGroup = document.getElementById('parcelamento-group');
    const metodoPagamentoHidden = document.getElementById('metodo-pagamento-hidden');
    const btnConfirmar = document.getElementById('btn-confirmar');
    const formPagamento = document.getElementById('form-pagamento');
    const cnhInput = document.getElementById('cnh');
    const cnhHidden = document.getElementById('cnh-hidden');
    const aceitarTermos = document.getElementById('aceitar-termos');

    // Inicialização
    inicializarPagamento();
    carregarDadosSessao();

    // ====== CONTROLE DOS MÉTODOS DE PAGAMENTO ======
    function inicializarPagamento() {
        // Event listeners para os cards de método de pagamento
        metodoCards.forEach(card => {
            card.addEventListener('click', function() {
                selecionarMetodoPagamento(this);
            });

            // Acessibilidade - teclado
            card.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    selecionarMetodoPagamento(this);
                }
            });

            // Tornar os cards focáveis
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
        });

        // Event listeners para validação em tempo real
        if (aceitarTermos) {
            aceitarTermos.addEventListener('change', validarFormulario);
        }

        if (cnhInput) {
            cnhInput.addEventListener('input', function() {
                formatarCNH(this);
                validarFormulario();
            });

            cnhInput.addEventListener('blur', function() {
                validarCNH(this);
            });
        }

        // Formatação dos campos do cartão
        inicializarCamposCartao();

        // Validação inicial
        validarFormulario();
    }

    function selecionarMetodoPagamento(card) {
        const metodo = card.dataset.metodo;
        const radio = card.querySelector('input[type="radio"]');
        
        // Desselecionar todos os cards
        metodoCards.forEach(c => {
            c.classList.remove('selecionado');
            c.querySelector('input[type="radio"]').checked = false;
        });

        // Selecionar card atual
        card.classList.add('selecionado');
        radio.checked = true;
        metodoPagamentoHidden.value = metodo;
        
        // Atualizar interface baseada no método selecionado
        atualizarInterfacePagamento(metodo);
        validarFormulario();
    }

    function atualizarInterfacePagamento(metodo) {
        // Mostrar/ocultar formulário do cartão
        if (metodo === 'credito' || metodo === 'debito') {
            cartaoForm.style.display = 'block';
            if (metodo === 'credito') {
                parcelamentoGroup.style.display = 'block';
            } else {
                parcelamentoGroup.style.display = 'none';
            }
        } else {
            cartaoForm.style.display = 'none';
            parcelamentoGroup.style.display = 'none';
        }

        // Atualizar total com desconto PIX
        atualizarTotalReserva(metodo);
    }

    function atualizarTotalReserva(metodo) {
        const totalElement = document.getElementById('total-reserva');
        if (!totalElement) return;

        // Valores base (substituir por valores reais do backend)
        const diarias = 5; // Exemplo: 5 dias
        const precoDiaria = 100; // Substituir por valor real
        const taxas = 45.00;
        
        let total = (precoDiaria * diarias) + taxas;
        
        // Aplicar desconto para PIX
        if (metodo === 'pix') {
            const desconto = total * 0.05; // 5% de desconto
            total = total - desconto;
        }
        
        totalElement.textContent = 'R$ ' + total.toFixed(2).replace('.', ',');
    }

    // ====== VALIDAÇÃO DO FORMULÁRIO ======
    function validarFormulario() {
        const metodoSelecionado = document.querySelector('input[name="metodo_pagamento"]:checked');
        const termosAceitos = aceitarTermos ? aceitarTermos.checked : false;
        
        // Validação básica
        let formularioValido = metodoSelecionado && termosAceitos;
        
        // Validação específica para Pessoa Física (CNH)
        if (cnhInput && cnhInput.style.display !== 'none') {
            const cnhValida = cnhInput.value.length === 11;
            formularioValido = formularioValido && cnhValida;
            
            if (!cnhValida && cnhInput.value.length > 0) {
                mostrarErroCampo(cnhInput, 'CNH deve ter 11 dígitos');
            } else {
                limparErroCampo(cnhInput);
            }
        }

        // Validações específicas para cartão
        if (metodoSelecionado && (metodoSelecionado.value === 'credito' || metodoSelecionado.value === 'debito')) {
            const validacaoCartao = validarCamposCartao();
            formularioValido = formularioValido && validacaoCartao;
        }

        // Atualizar estado do botão
        btnConfirmar.disabled = !formularioValido;

        return formularioValido;
    }

    // ====== CAMPOS DO CARTÃO ======
    function inicializarCamposCartao() {
        const numeroCartao = document.getElementById('numero_cartao');
        const validade = document.getElementById('validade');
        const cvv = document.getElementById('cvv');
        const nomeCartao = document.getElementById('nome_cartao');

        if (numeroCartao) {
            numeroCartao.addEventListener('input', function(e) {
                formatarNumeroCartao(e.target);
                validarFormulario();
            });

            numeroCartao.addEventListener('blur', function() {
                validarNumeroCartao(this);
            });
        }

        if (validade) {
            validade.addEventListener('input', function(e) {
                formatarValidade(e.target);
                validarFormulario();
            });

            validade.addEventListener('blur', function() {
                validarValidade(this);
            });
        }

        if (cvv) {
            cvv.addEventListener('input', function(e) {
                formatarCVV(e.target);
                validarFormulario();
            });

            cvv.addEventListener('blur', function() {
                validarCVV(this);
            });
        }

        if (nomeCartao) {
            nomeCartao.addEventListener('input', function() {
                validarFormulario();
            });

            nomeCartao.addEventListener('blur', function() {
                validarNomeCartao(this);
            });
        }
    }

    function validarCamposCartao() {
        const numeroCartao = document.getElementById('numero_cartao');
        const nomeCartao = document.getElementById('nome_cartao');
        const validade = document.getElementById('validade');
        const cvv = document.getElementById('cvv');

        let valido = true;

        if (numeroCartao && numeroCartao.value.replace(/\s/g, '').length !== 16) {
            mostrarErroCampo(numeroCartao, 'Número do cartão deve ter 16 dígitos');
            valido = false;
        } else if (numeroCartao) {
            limparErroCampo(numeroCartao);
        }

        if (nomeCartao && nomeCartao.value.trim().length < 3) {
            mostrarErroCampo(nomeCartao, 'Nome no cartão é obrigatório');
            valido = false;
        } else if (nomeCartao) {
            limparErroCampo(nomeCartao);
        }

        if (validade && !validarFormatoValidade(validade.value)) {
            mostrarErroCampo(validade, 'Data de validade inválida');
            valido = false;
        } else if (validade) {
            limparErroCampo(validade);
        }

        if (cvv && cvv.value.length !== 3) {
            mostrarErroCampo(cvv, 'CVV deve ter 3 dígitos');
            valido = false;
        } else if (cvv) {
            limparErroCampo(cvv);
        }

        return valido;
    }

    // ====== FORMATAÇÃO DE CAMPOS ======
    function formatarCNH(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 11) value = value.substring(0, 11);
        input.value = value;
        
        if (cnhHidden) {
            cnhHidden.value = value;
        }
    }

    function formatarNumeroCartao(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 16) value = value.substring(0, 16);
        value = value.replace(/(\d{4})(?=\d)/g, '$1 ');
        input.value = value;
    }

    function formatarValidade(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 4) value = value.substring(0, 4);
        if (value.length > 2) {
            value = value.replace(/(\d{2})(\d{0,2})/, '$1/$2');
        }
        input.value = value;
    }

    function formatarCVV(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 3) value = value.substring(0, 3);
        input.value = value;
    }

    // ====== VALIDAÇÕES ESPECÍFICAS ======
    function validarCNH(input) {
        const value = input.value.replace(/\D/g, '');
        if (value.length === 11) {
            limparErroCampo(input);
            return true;
        } else if (value.length > 0) {
            mostrarErroCampo(input, 'CNH deve ter 11 dígitos');
            return false;
        }
        return false;
    }

    function validarNumeroCartao(input) {
        const value = input.value.replace(/\s/g, '');
        if (value.length === 16) {
            limparErroCampo(input);
            return true;
        } else if (value.length > 0) {
            mostrarErroCampo(input, 'Número do cartão deve ter 16 dígitos');
            return false;
        }
        return false;
    }

    function validarValidade(input) {
        if (validarFormatoValidade(input.value)) {
            limparErroCampo(input);
            return true;
        } else if (input.value.length > 0) {
            mostrarErroCampo(input, 'Data de validade inválida');
            return false;
        }
        return false;
    }

    function validarCVV(input) {
        if (input.value.length === 3) {
            limparErroCampo(input);
            return true;
        } else if (input.value.length > 0) {
            mostrarErroCampo(input, 'CVV deve ter 3 dígitos');
            return false;
        }
        return false;
    }

    function validarNomeCartao(input) {
        if (input.value.trim().length >= 3) {
            limparErroCampo(input);
            return true;
        } else if (input.value.length > 0) {
            mostrarErroCampo(input, 'Nome no cartão é obrigatório');
            return false;
        }
        return false;
    }

    function validarFormatoValidade(validade) {
        const regex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
        if (!regex.test(validade)) return false;

        const [mes, ano] = validade.split('/');
        const dataAtual = new Date();
        const anoAtual = dataAtual.getFullYear() % 100;
        const mesAtual = dataAtual.getMonth() + 1;

        if (parseInt(ano) < anoAtual) return false;
        if (parseInt(ano) === anoAtual && parseInt(mes) < mesAtual) return false;

        return true;
    }

    // ====== MANIPULAÇÃO DE ERROS ======
    function mostrarErroCampo(campo, mensagem) {
        limparErroCampo(campo);
        
        campo.style.borderColor = '#dc3545';
        
        const erroElement = document.createElement('div');
        erroElement.className = 'mensagem-erro';
        erroElement.textContent = mensagem;
        erroElement.style.color = '#dc3545';
        erroElement.style.fontSize = '12px';
        erroElement.style.marginTop = '5px';
        
        campo.parentNode.appendChild(erroElement);
    }

    function limparErroCampo(campo) {
        campo.style.borderColor = '';
        
        const erroExistente = campo.parentNode.querySelector('.mensagem-erro');
        if (erroExistente) {
            erroExistente.remove();
        }
    }

    // ====== DADOS DA SESSÃO ======
    function carregarDadosSessao() {
        // Em uma implementação real, esses dados viriam do backend/sessão
        const dadosReserva = {
            localRetirada: 'Aeroporto de Guarulhos (GRU)',
            dataRetirada: '15/03/2025 10:00',
            localDevolucao: 'Aeroporto de Guarulhos (GRU)', 
            dataDevolucao: '20/03/2025 10:00'
        };

        const localRetiradaElement = document.getElementById('local-retirada-resumo');
        const dataRetiradaElement = document.getElementById('data-retirada-resumo');
        const localDevolucaoElement = document.getElementById('local-devolucao-resumo');
        const dataDevolucaoElement = document.getElementById('data-devolucao-resumo');

        if (localRetiradaElement) localRetiradaElement.textContent = dadosReserva.localRetirada;
        if (dataRetiradaElement) dataRetiradaElement.textContent = dadosReserva.dataRetirada;
        if (localDevolucaoElement) localDevolucaoElement.textContent = dadosReserva.localDevolucao;
        if (dataDevolucaoElement) dataDevolucaoElement.textContent = dadosReserva.dataDevolucao;
    }

    // ====== SUBMISSÃO DO FORMULÁRIO ======
    if (formPagamento) {
        formPagamento.addEventListener('submit', function(e) {
            if (!validarFormulario()) {
                e.preventDefault();
                mostrarMensagem('Por favor, corrija os erros no formulário antes de continuar.', 'erro');
                return;
            }

            // Mostrar loading
            btnConfirmar.disabled = true;
            btnConfirmar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';

            // Simular processamento (em sistema real, seria uma requisição AJAX)
            setTimeout(() => {
                mostrarMensagem('Pagamento processado com sucesso! Redirecionando...', 'sucesso');
            }, 2000);
        });
    }

    function mostrarMensagem(mensagem, tipo) {
        // Remover mensagens existentes
        const mensagensExistentes = document.querySelectorAll('.mensagem-flutuante');
        mensagensExistentes.forEach(msg => msg.remove());

        // Criar nova mensagem
        const mensagemElement = document.createElement('div');
        mensagemElement.className = `mensagem-flutuante mensagem-${tipo}`;
        mensagemElement.textContent = mensagem;

        // Estilos da mensagem
        Object.assign(mensagemElement.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '6px',
            color: 'white',
            fontWeight: '600',
            zIndex: '10000',
            boxShadow: '0 5px 15px rgba(0,0,0,0.2)'
        });

        // Cores por tipo
        if (tipo === 'sucesso') {
            mensagemElement.style.backgroundColor = '#28a745';
        } else if (tipo === 'erro') {
            mensagemElement.style.backgroundColor = '#dc3545';
        } else {
            mensagemElement.style.backgroundColor = '#17a2b8';
        }

        // Adicionar ao DOM
        document.body.appendChild(mensagemElement);

        // Remover após 5 segundos
        setTimeout(() => {
            if (mensagemElement.parentNode) {
                mensagemElement.parentNode.removeChild(mensagemElement);
            }
        }, 5000);
    }
});