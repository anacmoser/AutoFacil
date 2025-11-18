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
    let precoDiario = 0;
    
    // Controlar se o modal já foi mostrado
    let modalMostrado = false;

    // Inicialização
    inicializarPagina();

    function inicializarPagina() {
        inicializarPrecoDiario();
        inicializarDatas();
        inicializarModal();
    }

    function inicializarPrecoDiario() {
        try {
            // Método 1: Do elemento HTML
            const precoElement = document.querySelector('.preco-diario .valor');
            if (precoElement) {
                const precoTexto = precoElement.textContent.replace('R$', '').replace(',', '.').trim();
                precoDiario = parseFloat(precoTexto);
            }
            
            // Método 2: Se ainda for NaN, tentar do template
            if (isNaN(precoDiario)) {
                // Buscar o preço no template Flask
                const precoTemplate = '{{ veiculo.precoDiario }}';
                if (precoTemplate && precoTemplate !== '{{ veiculo.precoDiario }}') {
                    precoDiario = parseFloat(precoTemplate);
                }
            }
            
            // Método 3: Valor padrão se ainda for NaN
            if (isNaN(precoDiario)) {
                precoDiario = 100; // Valor padrão
                console.warn('Preço diário não encontrado, usando valor padrão:', precoDiario);
            }

            console.log('Preço diário carregado:', precoDiario);
        } catch (error) {
            console.error('Erro ao extrair preço diário:', error);
            precoDiario = 100; // Valor padrão em caso de erro
        }
    }

    function inicializarDatas() {
        // Configurar data mínima para hoje
        const hoje = new Date().toISOString().split('T')[0];
        if (dataRetirada) dataRetirada.min = hoje;
        if (dataDevolucao) dataDevolucao.min = hoje;

        // Event listeners para validação de datas
        if (dataRetirada) {
            dataRetirada.addEventListener('change', function() {
                validarDatas();
                atualizarDataDevolucaoMinima();
            });
        }

        if (dataDevolucao) {
            dataDevolucao.addEventListener('change', validarDatas);
        }

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

    function inicializarModal() {
        // Event listener para fechar modal
        const btnFecharModal = document.getElementById('btnFecharModal');
        if (btnFecharModal) {
            btnFecharModal.addEventListener('click', fecharModalDesconto);
        }

        // Fechar modal clicando fora
        const modalDesconto = document.getElementById('modalDesconto');
        if (modalDesconto) {
            modalDesconto.addEventListener('click', function(e) {
                if (e.target === modalDesconto) {
                    fecharModalDesconto();
                }
            });
        }

        // Fechar modal com ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                fecharModalDesconto();
            }
        });
    }

    function atualizarDataDevolucaoMinima() {
        if (dataRetirada.value && dataDevolucao) {
            dataDevolucao.min = dataRetirada.value;
            
            // Se a data de devolução for anterior à nova data mínima, limpar
            if (dataDevolucao.value && dataDevolucao.value < dataRetirada.value) {
                dataDevolucao.value = '';
                ocultarInformacoesReserva();
            }
        }
    }

    function validarDatas() {
        if (!dataRetirada.value || !dataDevolucao.value) {
            ocultarInformacoesReserva();
            return true; // Retorna true para não bloquear o formulário
        }

        const dataRet = new Date(dataRetirada.value);
        const dataDev = new Date(dataDevolucao.value);
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);

        // Reset do estilo
        if (dataRetirada) dataRetirada.style.borderColor = '';
        if (dataDevolucao) dataDevolucao.style.borderColor = '';

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
        if (!campo) return;
        
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
        // Validar dias
        if (isNaN(dias) || dias < 1) {
            console.error('Número de dias inválido:', dias);
            return;
        }

        // Atualizar texto de dias
        if (textoDias) {
            textoDias.textContent = `${dias} ${dias === 1 ? 'dia' : 'dias'} de aluguel`;
        }
        
        // Calcular e atualizar valor total
        const total = precoDiario * dias;
        
        // Validar cálculo
        if (isNaN(total)) {
            console.error('Erro no cálculo do total. Preço:', precoDiario, 'Dias:', dias);
            if (valorTotal) valorTotal.textContent = '0,00';
        } else {
            if (valorTotal) {
                valorTotal.textContent = total.toFixed(2).replace('.', ',');
            }
        }
        
        // Mostrar informações
        if (diasReserva) diasReserva.style.display = 'block';
        if (statusDisponibilidade) {
            statusDisponibilidade.innerHTML = '<i class="fas fa-check-circle" style="color: #28a745;"></i> Veículo disponível para estas datas';
        }
        
        // Verificar e mostrar desconto se aplicável - APENAS NA PRIMEIRA VEZ
        if (!modalMostrado) {
            verificarDesconto(dias);
            modalMostrado = true;
        }
        
        validarFormulario();
    }

    function ocultarInformacoesReserva() {
        if (diasReserva) diasReserva.style.display = 'none';
        if (statusDisponibilidade) {
            statusDisponibilidade.innerHTML = '<i class="fas fa-info-circle"></i> Selecione as datas para verificar disponibilidade';
        }
        if (valorTotal) valorTotal.textContent = '0,00';
    }

    function verificarDesconto(dias) {
        const modalDesconto = document.getElementById('modalDesconto');
        const mensagemDesconto = document.getElementById('mensagemDesconto');
        const periodoModal = document.getElementById('periodoModal');
        const descontoModal = document.getElementById('descontoModal');
        const economiaModal = document.getElementById('economiaModal');
        const totalModal = document.getElementById('totalModal');
        
        if (!modalDesconto || !mensagemDesconto) return;
        
        let desconto = 0;
        let mensagem = '';
        
        // MOSTRAR MODAL PARA QUALQUER DATA - APENAS NA PRIMEIRA VEZ
        if (dias >= 1) {
            if (dias >= 30 && dias < 90) {
                desconto = 10;
                mensagem = 'Desconto especial para aluguel de 30 a 89 dias!';
            } else if (dias >= 90 && dias < 180) {
                desconto = 30;
                mensagem = 'Excelente desconto para aluguel de 90 a 179 dias!';
            } else if (dias >= 180) {
                desconto = 45;
                mensagem = 'Super desconto para aluguel acima de 180 dias!';
            } else {
                desconto = 0;
                mensagem = 'Confira nossos descontos para períodos mais longos!';
            }
            
            const totalSemDesconto = precoDiario * dias;
            const valorDesconto = totalSemDesconto * (desconto / 100);
            const totalComDesconto = totalSemDesconto - valorDesconto;
            
            mensagemDesconto.textContent = mensagem;
            if (periodoModal) periodoModal.textContent = `${dias} dias`;
            if (descontoModal) descontoModal.textContent = desconto > 0 ? `${desconto}%` : '0%';
            if (economiaModal) economiaModal.textContent = desconto > 0 ? `R$ ${valorDesconto.toFixed(2).replace('.', ',')}` : 'R$ 0,00';
            if (totalModal) totalModal.textContent = `R$ ${totalComDesconto.toFixed(2).replace('.', ',')}`;
            
            // Mostrar o modal
            modalDesconto.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            console.log('Modal de desconto exibido para', dias, 'dias');
        }
    }

    function fecharModalDesconto() {
        const modalDesconto = document.getElementById('modalDesconto');
        if (modalDesconto) {
            modalDesconto.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    function validarFormulario() {
        const dataRet = dataRetirada ? dataRetirada.value : '';
        const dataDev = dataDevolucao ? dataDevolucao.value : '';
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
            
            // Atualizar estilo do botão
            if (formularioValido) {
                btnReservar.style.backgroundColor = '#ff8c14';
                btnReservar.style.cursor = 'pointer';
            } else {
                btnReservar.style.backgroundColor = '#ccc';
                btnReservar.style.cursor = 'not-allowed';
            }
        }

        return formularioValido;
    }

    // REMOVER A VALIDAÇÃO QUE IMPEDE O ENVIO DO FORMULÁRIO
    // O formulário deve ser enviado normalmente, a validação do servidor vai tratar os erros

    // Miniaturas da galeria
    const miniaturas = document.querySelectorAll('.miniatura');
    const imagemPrincipal = document.getElementById('imagemPrincipal');

    if (miniaturas.length > 0 && imagemPrincipal) {
        miniaturas.forEach(miniatura => {
            miniatura.addEventListener('click', function() {
                // Remover classe active de todas as miniaturas
                miniaturas.forEach(m => m.classList.remove('active'));
                
                // Adicionar classe active na miniatura clicada
                this.classList.add('active');
                
                // Atualizar imagem principal
                const novaImagem = this.getAttribute('data-imagem');
                if (novaImagem) {
                    imagemPrincipal.src = novaImagem;
                    imagemPrincipal.alt = this.querySelector('img').alt;
                }
            });
        });
    }

    // Debug: Log para verificar se o script carregou corretamente
    console.log('Script de detalhes do veículo carregado com sucesso');
    console.log('Preço diário:', precoDiario);
});