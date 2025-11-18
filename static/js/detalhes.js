/**
 * AutoFácil - Script da Página de Detalhes do Veículo
 * Funcionalidades: Validação de datas, cálculo de dias, verificação de disponibilidade
 */

document.addEventListener('DOMContentLoaded', function () {
    // Elementos do formulário de reserva
    const dataRetirada = document.getElementById('dataRetirada');
    const dataDevolucao = document.getElementById('dataDevolucao');
    const localRetirada = document.getElementById('localRetirada');
    const localDevolucao = document.getElementById('localDevolucao');
    const btnReservar = document.getElementById('btnReservar');
    const disponibilidadeInfo = document.getElementById('disponibilidadeInfo');
    const statusDisponibilidade = document.getElementById('statusDisponibilidade');
    const diasReserva = document.getElementById('diasReserva');
    const textoDias = document.getElementById('textoDias');
    const valorTotal = document.getElementById('valorTotal');

    // Preço diário do veículo (extraído do HTML)
    const precoDiario = parseFloat('{{ veiculo.precoDiario }}');

    // Inicialização
    inicializarDatas();

    function inicializarDatas() {
        // Configurar data mínima para hoje
        const hoje = new Date().toISOString().split('T')[0];
        dataRetirada.min = hoje;
        dataDevolucao.min = hoje;

        // Event listeners para validação de datas
        dataRetirada.addEventListener('change', validarDatas);
        dataDevolucao.addEventListener('change', validarDatas);

        // Event listeners para locais
        if (localRetirada) {
            localRetirada.addEventListener('change', validarFormulario);
        }
        if (localDevolucao) {
            localDevolucao.addEventListener('change', validarFormulario);
        }

        // Validar formulário inicial
        validarFormulario();
    }

    function validarDatas() {
        const dataRet = new Date(dataRetirada.value);
        const dataDev = new Date(dataDevolucao.value);
        const hoje = new Date();

        // Reset do estilo
        dataRetirada.style.borderColor = '';
        dataDevolucao.style.borderColor = '';

        // Validar data de retirada
        if (dataRetirada.value && dataRet < hoje) {
            mostrarErroData(dataRetirada, 'Data de retirada não pode ser anterior a hoje');
            return false;
        }

        // Validar data de devolução
        if (dataDevolucao.value && dataDev < dataRet) {
            mostrarErroData(dataDevolucao, 'Data de devolução não pode ser anterior à retirada');
            return false;
        }

        // Validar período mínimo (pelo menos 1 dia)
        if (dataRetirada.value && dataDevolucao.value) {
            const diffTime = dataDev - dataRet;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (diffDays < 1) {
                mostrarErroData(dataDevolucao, 'Período mínimo de 1 dia');
                return false;
            }

            // Atualizar informações de dias e valor
            atualizarInformacoesReserva(diffDays);
        }

        limparErroData();
        return true;
    }

    function mostrarErroData(campo, mensagem) {
        campo.style.borderColor = '#dc3545';
        
        // Remover mensagens anteriores
        const mensagensAnteriores = document.querySelectorAll('.mensagem-erro-data');
        mensagensAnteriores.forEach(msg => msg.remove());

        // Adicionar nova mensagem
        const erroElement = document.createElement('div');
        erroElement.className = 'mensagem-erro-data';
        erroElement.style.color = '#dc3545';
        erroElement.style.fontSize = '12px';
        erroElement.style.marginTop = '5px';
        erroElement.textContent = mensagem;
        
        campo.parentNode.appendChild(erroElement);

        // Ocultar informações de disponibilidade
        ocultarInformacoesReserva();
    }

    function limparErroData() {
        const mensagensErro = document.querySelectorAll('.mensagem-erro-data');
        mensagensErro.forEach(msg => msg.remove());
    }

    function atualizarInformacoesReserva(dias) {
        // Atualizar texto de dias
        textoDias.textContent = `${dias} ${dias === 1 ? 'dia' : 'dias'} de aluguel`;
        
        // Calcular e atualizar valor total
        const total = precoDiario * dias;
        valorTotal.textContent = total.toFixed(2).replace('.', ',');

        // Mostrar informações
        diasReserva.style.display = 'block';
        statusDisponibilidade.innerHTML = '<i class="fas fa-check-circle" style="color: #28a745;"></i> Veículo disponível para estas datas';

        validarFormulario();
    }

    function ocultarInformacoesReserva() {
        diasReserva.style.display = 'none';
        statusDisponibilidade.innerHTML = '<i class="fas fa-info-circle"></i> Selecione as datas para verificar disponibilidade';
        valorTotal.textContent = '0,00';
    }

    function validarFormulario() {
        const dataRet = dataRetirada.value;
        const dataDev = dataDevolucao.value;
        const localRet = localRetirada ? localRetirada.value : '';
        const localDev = localDevolucao ? localDevolucao.value : '';

        let formularioValido = dataRet && dataDev && localRet && localDev;

        // Validar coerência das datas
        if (dataRet && dataDev) {
            const dataRetObj = new Date(dataRet);
            const dataDevObj = new Date(dataDev);
            formularioValido = formularioValido && (dataDevObj >= dataRetObj);
        }

        // Habilitar/desabilitar botão
        if (btnReservar) {
            btnReservar.disabled = !formularioValido;
        }

        return formularioValido;
    }

    // Prevenir envio se formulário inválido
    const formReserva = document.querySelector('.form-reserva form');
    if (formReserva) {
        formReserva.addEventListener('submit', function (e) {
            if (!validarFormulario()) {
                e.preventDefault();
                alert('Por favor, preencha todas as datas e locais corretamente antes de reservar.');
                return;
            }

            if (!validarDatas()) {
                e.preventDefault();
                alert('Por favor, corrija as datas antes de reservar.');
                return;
            }
        });
    }
});