/**
 * AutoFácil - Script da Página de Pagamento
 * Funcionalidades: Seleção de método de pagamento, validações, formatação de campos
 */

document.addEventListener('DOMContentLoaded', function () {
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
    const descontoPix = document.getElementById('desconto-pix');
    const valorDesconto = document.getElementById('valor-desconto');

    // Inicialização
    inicializarPagamento();

    // ====== CONTROLE DOS MÉTODOS DE PAGAMENTO ======
    function inicializarPagamento() {
        // Event listeners para os cards de método de pagamento
        metodoCards.forEach(card => {
            card.addEventListener('click', function () {
                selecionarMetodoPagamento(this);
            });

            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    selecionarMetodoPagamento(this);
                }
            });

            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
            card.setAttribute('aria-label', `Selecionar ${card.querySelector('h3').textContent} como método de pagamento`);
        });

        // Event listeners para validação
        if (aceitarTermos) {
            aceitarTermos.addEventListener('change', validarFormulario);
        }

        if (cnhInput) {
            cnhInput.addEventListener('input', function () {
                formatarCNH(this);
                validarFormulario();
            });

            cnhInput.addEventListener('blur', function () {
                validarCNH(this);
            });
        }

        inicializarCamposCartao();
        validarFormulario();
    }

    function selecionarMetodoPagamento(card) {
        const metodo = card.dataset.metodo;
        const radio = card.querySelector('input[type="radio"]');

        // Remover seleção de todos os cards
        metodoCards.forEach(c => {
            c.classList.remove('selecionado');
            c.querySelector('input[type="radio"]').checked = false;
            c.setAttribute('aria-checked', 'false');
        });

        // Adicionar seleção ao card clicado
        card.classList.add('selecionado');
        radio.checked = true;
        card.setAttribute('aria-checked', 'true');
        metodoPagamentoHidden.value = metodo;

        atualizarInterfacePagamento(metodo);
        validarFormulario();
    }

    function atualizarInterfacePagamento(metodo) {
        if (metodo === 'credito' || metodo === 'debito') {
            cartaoForm.style.display = 'block';
            parcelamentoGroup.style.display = metodo === 'credito' ? 'block' : 'none';
        } else {
            cartaoForm.style.display = 'none';
            parcelamentoGroup.style.display = 'none';
        }

        atualizarTotalReserva(metodo);
    }

    function atualizarTotalReserva(metodo) {
        const totalElement = document.getElementById('total-reserva');
        if (!totalElement) return;

        // Extrair valor atual do total (sem desconto)
        const totalTexto = totalElement.textContent.replace('R$', '').replace(',', '.').trim();
        let totalBase = parseFloat(totalTexto);

        // Se já tem desconto aplicado, remover para recalcular
        if (descontoPix && descontoPix.style.display !== 'none') {
            const descontoTexto = valorDesconto.textContent.replace('-', '').replace('R$', '').replace(',', '.').trim();
            const descontoValor = parseFloat(descontoTexto);
            totalBase += descontoValor;
        }

        let total = totalBase;

        if (metodo === 'pix') {
            const desconto = totalBase * 0.05;
            total = totalBase - desconto;

            if (descontoPix) {
                descontoPix.style.display = 'flex';
                valorDesconto.textContent = '- R$ ' + desconto.toFixed(2).replace('.', ',');
            }
        } else {
            if (descontoPix) {
                descontoPix.style.display = 'none';
            }
        }

        totalElement.textContent = 'R$ ' + total.toFixed(2).replace('.', ',');
    }

    // ====== VALIDAÇÃO DO FORMULÁRIO ======
    function validarFormulario() {
        const metodoSelecionado = document.querySelector('input[name="metodo_pagamento"]:checked');
        const termosAceitos = aceitarTermos ? aceitarTermos.checked : false;

        let formularioValido = metodoSelecionado && termosAceitos;

        if (cnhInput && cnhInput.offsetParent !== null) {
            const cnhValida = cnhInput.value.length === 11;
            formularioValido = formularioValido && cnhValida;
        }

        if (metodoSelecionado && (metodoSelecionado.value === 'credito' || metodoSelecionado.value === 'debito')) {
            const validacaoCartao = validarCamposCartao();
            formularioValido = formularioValido && validacaoCartao;
        }

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
            numeroCartao.addEventListener('input', function (e) {
                formatarNumeroCartao(e.target);
                validarFormulario();
            });
        }

        if (validade) {
            validade.addEventListener('input', function (e) {
                formatarValidade(e.target);
                validarFormulario();
            });
        }

        if (cvv) {
            cvv.addEventListener('input', function (e) {
                formatarCVV(e.target);
                validarFormulario();
            });
        }

        if (nomeCartao) {
            nomeCartao.addEventListener('input', function () {
                validarFormulario();
            });
        }
    }

    function validarCamposCartao() {
        const numeroCartao = document.getElementById('numero_cartao');
        const nomeCartao = document.getElementById('nome_cartao');
        const validade = document.getElementById('validade');
        const cvv = document.getElementById('cvv');

        if (!numeroCartao || !nomeCartao || !validade || !cvv) return false;

        return numeroCartao.value.replace(/\s/g, '').length === 16 &&
            nomeCartao.value.trim().length >= 3 &&
            validarFormatoValidade(validade.value) &&
            cvv.value.length === 3;
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

    function validarCNH(input) {
        const value = input.value.replace(/\D/g, '');
        if (value.length !== 11 && value.length > 0) {
            mostrarErroCampo(input, 'CNH deve ter 11 dígitos');
        } else {
            limparErroCampo(input);
        }
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

    function mostrarErroCampo(campo, mensagem) {
        limparErroCampo(campo);
        campo.style.borderColor = '#dc3545';

        const erroElement = document.createElement('div');
        erroElement.className = 'mensagem-erro';
        erroElement.textContent = mensagem;
        campo.parentNode.appendChild(erroElement);
    }

    function limparErroCampo(campo) {
        campo.style.borderColor = '';
        const erroExistente = campo.parentNode.querySelector('.mensagem-erro');
        if (erroExistente) {
            erroExistente.remove();
        }
    }

    // ====== MODAL DE SUCESSO ======
    window.mostrarModalReserva = function() {
        const modal = document.getElementById('modalReservaSucesso');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    window.fecharModalReserva = function() {
        const modal = document.getElementById('modalReservaSucesso');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        
        // Redireciona para minhas reservas
        setTimeout(() => {
            window.location.href = '/minhasReservas';
        }, 500);
    }

    // Fechar modal clicando fora
    document.addEventListener('click', function (e) {
        const modal = document.getElementById('modalReservaSucesso');
        if (e.target === modal) {
            fecharModalReserva();
        }
    });

    // Fechar com ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            fecharModalReserva();
        }
    });

    // ====== SUBMISSÃO DO FORMULÁRIO ======
    if (formPagamento) {
        formPagamento.addEventListener('submit', function (e) {
            e.preventDefault(); // Previne envio para testar

            if (!validarFormulario()) {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }

            btnConfirmar.disabled = true;
            btnConfirmar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';

            // Simular processamento
            setTimeout(() => {
                mostrarModalReserva();
                
                // Para enviar de verdade, descomente:
                // formPagamento.submit();
            }, 2000);
        });
    }
});