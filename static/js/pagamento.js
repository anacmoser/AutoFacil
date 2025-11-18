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
                // Só formata se não for readonly
                if (!this.readOnly) {
                    formatarCNH(this);
                }
                validarFormulario();
            });

            cnhInput.addEventListener('blur', function () {
                // Só valida se não for readonly
                if (!this.readOnly) {
                    validarCNH(this);
                }
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
    }

    // ====== VALIDAÇÃO DO FORMULÁRIO ======
    function validarFormulario() {
        const metodoSelecionado = document.querySelector('input[name="metodo_pagamento"]:checked');
        const termosAceitos = aceitarTermos ? aceitarTermos.checked : false;

        let formularioValido = metodoSelecionado && termosAceitos;

        // Verifica se o campo CNH está visível E não é readonly (ou seja, precisa ser validado)
        if (cnhInput && cnhInput.offsetParent !== null && !cnhInput.readOnly) {
            if (!validarCNHCompleta(cnhInput.value)) {
                cnhInput.focus();
                return;
            }
        }

        if (metodoSelecionado && (metodoSelecionado.value === 'credito' || metodoSelecionado.value === 'debito')) {
            const validacaoCartao = validarCamposCartao();
            formularioValido = formularioValido && validacaoCartao;
        }

        btnConfirmar.disabled = !formularioValido;
        return formularioValido;
    }

  // ====== VALIDAÇÃO DA CNH - VERSÃO CORRIGIDA ======
function validarCNHCompleta(cnh) {
    // Remove caracteres não numéricos
    cnh = cnh.replace(/\D/g, '');

    // Verifica se tem 11 dígitos
    if (cnh.length !== 11) {
        return false;
    }

    // Verifica se não é uma sequência de números iguais
    if (/^(\d)\1+$/.test(cnh)) {
        return false;
    }

    // Algoritmo CORRETO de validação da CNH
    let soma = 0;
    let multiplicador = 9;

    // Calcula primeiro dígito verificador
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cnh.charAt(i)) * multiplicador;
        multiplicador--;
    }

    let digito1 = soma % 11;
    if (digito1 === 10) {
        digito1 = 0;
    }

    // Calcula segundo dígito verificador
    soma = 0;
    multiplicador = 1;
    
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cnh.charAt(i)) * multiplicador;
        multiplicador++;
    }

    let digito2 = soma % 11;
    
    // Ajuste especial para o segundo dígito
    if (digito2 >= 10) {
        digito2 -= 2;
    }
    if (digito2 < 0) {
        digito2 += 11;
    }

    // Verifica os dígitos
    return parseInt(cnh.charAt(9)) === digito1 && parseInt(cnh.charAt(10)) === digito2;
}

// CNHs válidas para teste
console.log('02650306461:', validarCNHCompleta("02650306461")); // true
console.log('12345678909:', validarCNHCompleta("12345678909")); // false (esta realmente é inválida)


    function validarCNH(input) {
        const value = input.value.replace(/\D/g, '');
        let valido = true;
        let mensagem = '';

        if (value.length === 0) {
            mensagem = 'CNH é obrigatória';
            valido = false;
        } else if (value.length !== 11) {
            mensagem = 'CNH deve ter 11 dígitos';
            valido = false;
        } else if (!validarCNHCompleta(value)) {
            mensagem = 'CNH inválida';
            valido = false;
        }

        if (!valido) {
            mostrarErroCampo(input, mensagem);
        } else {
            limparErroCampo(input);
        }

        return valido;
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
        // Se o campo for readonly, não faz nada
        if (input.readOnly) return;

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
    window.mostrarModalReserva = function () {
        const modal = document.getElementById('modalReservaSucesso');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    window.fecharModalReserva = function () {
        const modal = document.getElementById('modalReservaSucesso');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';

        // Redireciona para minhas reservas
        setTimeout(() => {
            window.location.href = '/portaldoCliente';
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
            e.preventDefault();

            if (!validarFormulario()) {
                alert('Por favor, preencha todos os campos obrigatórios corretamente.');
                return;
            }

            // Validação específica da CNH
            if (cnhInput && cnhInput.offsetParent !== null) {
                if (!validarCNHCompleta(cnhInput.value)) {
                    alert('Por favor, insira uma CNH válida.');
                    cnhInput.focus();
                    return;
                }
            }

            btnConfirmar.disabled = true;
            btnConfirmar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';

            // Simular processamento
            setTimeout(() => {
                mostrarModalReserva();

                // Submeter o formulário após mostrar o modal
                setTimeout(() => {
                    formPagamento.submit();
                }, 3000);
            }, 2000);
        });
    }
});