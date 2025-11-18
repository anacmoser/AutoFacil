/*
 * AutoFácil - Script Portal do Cliente
 * Funcionalidades para portal do cliente e reservas
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    if (currentPage === 'portal-cliente') {
        initPortalCliente();
        initImageUpload(); // Adiciona a função de upload de imagem
        initCEP(); // Inicializa a funcionalidade de CEP
    }
});

// ===== INICIALIZAÇÃO DA API DE CEP =====
function initCEP() {
    // Adicionar evento para buscar CEP quando o campo perder o foco
    const cepInputs = document.querySelectorAll('#cep, #cep_empresa');
    cepInputs.forEach(cepInput => {
        cepInput.addEventListener('blur', function() {
            buscarEnderecoPorCEP(this);
        });
    });
}

// ===== API DE CEP =====
async function buscarEnderecoPorCEP(cepInput) {
    const cep = cepInput.value.replace(/\D/g, '');
    
    // Verifica se CEP tem 8 dígitos
    if (cep.length !== 8) {
        return;
    }

    try {
        // Mostrar loading
        cepInput.classList.add('carregando');
        
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const dados = await response.json();

        // Remover loading
        cepInput.classList.remove('carregando');

        if (dados.erro) {
            mostrarMensagemTemporaria('CEP não encontrado.', 'error');
            return;
        }

        // Preencher campos de endereço automaticamente
        preencherEnderecoPortal(dados, cepInput.id);

    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
        cepInput.classList.remove('carregando');
        mostrarMensagemTemporaria('Erro ao buscar CEP. Tente novamente.', 'error');
    }
}

// ===== PREENCHER ENDEREÇO NO PORTAL =====
function preencherEnderecoPortal(dados, cepFieldId) {
    // Determinar os IDs dos campos baseado no campo de CEP usado
    const isEmpresa = cepFieldId === 'cep_empresa';
    const prefix = isEmpresa ? 'empresa_' : '';
    
    const campos = {
        logradouro: `${prefix}logradouro`,
        bairro: `${prefix}bairro`,
        cidade: `${prefix}cidade`,
        estado: `${prefix}estado`
    };

    // Preencher cada campo se existir
    Object.keys(campos).forEach(chave => {
        const campoId = campos[chave];
        const campo = document.getElementById(campoId);
        
        if (campo && dados[chave]) {
            campo.value = dados[chave];
            
            // Disparar evento de change para atualizar o estado do campo
            setTimeout(() => {
                campo.dispatchEvent(new Event('change', { bubbles: true }));
            }, 100);
        }
    });

    // Preencher complemento se estiver vazio
    const complementoField = document.getElementById(`${prefix}complemento`);
    if (complementoField && dados.complemento && !complementoField.value) {
        complementoField.value = dados.complemento;
    }

    // Focar no campo número para facilitar o preenchimento
    const numeroField = document.getElementById(`${prefix}numero`);
    if (numeroField) {
        setTimeout(() => {
            numeroField.focus();
        }, 200);
    }

    mostrarMensagemTemporaria('Endereço preenchido automaticamente!', 'success');
}

// ===== PAGINA PORTAL DO CLIENTE ======
function initPortalCliente() {
    // Navegação entre seções - NOVOS NOMES
    const perfilCards = document.querySelectorAll('.perfil-card');
    const portalSections = document.querySelectorAll('.portal-section');

    perfilCards.forEach(card => {
        card.addEventListener('click', function () {
            const target = this.dataset.target;

            perfilCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');

            portalSections.forEach(section => section.classList.remove('active'));
            document.getElementById(`${target}-section`).classList.add('active');
        });
    });

    // Edição de perfil
    const editarPerfilBtn = document.getElementById('editar-perfil');
    const cancelarEdicaoBtn = document.getElementById('cancelar-edicao');
    const formPerfil = document.getElementById('form-perfil');
    const formActionsPerfil = document.getElementById('form-actions-perfil');

    // Edição de endereço
    const editarEnderecoBtn = document.getElementById('editar-endereco');
    const cancelarEdicaoEnderecoBtn = document.getElementById('cancelar-edicao-endereco');
    const formEndereco = document.getElementById('form-endereco');

    // Alteração de Senha - CORREÇÃO: ADICIONAR EVENTO DO BOTÃO
    const btnAlterarSenha = document.getElementById('btn-alterar-senha');
    const formAlterarSenha = document.getElementById('form-alterar-senha');
    const cancelarAlterarSenhaBtn = document.getElementById('cancelar-alterar-senha');
    const formNovaSenha = document.getElementById('form-nova-senha');

    // Modal de Confirmação de Senha para Editar Dados
    const modalConfirmarSenha = document.getElementById('modal-confirmar-senha');
    const formConfirmarSenha = document.getElementById('form-confirmar-senha');
    const cancelarConfirmacaoBtn = document.getElementById('cancelar-confirmacao');
    let acaoPendente = null; // Para armazenar qual ação será executada após confirmação

    // ===== EVENTO DO BOTÃO ALTERAR SENHA - CORRIGIDO =====
    if (btnAlterarSenha && formAlterarSenha) {
        btnAlterarSenha.addEventListener('click', function() {
            console.log('Botão alterar senha clicado');
            formAlterarSenha.style.display = 'block';
            this.style.display = 'none';
        });
    }

    // Modificar o evento de editar perfil para pedir senha
    if (editarPerfilBtn && formPerfil) {
        editarPerfilBtn.addEventListener('click', function () {
            acaoPendente = 'editar-perfil';
            modalConfirmarSenha.style.display = 'block';
        });
    }

    // Modificar o evento de editar endereço para pedir senha
    if (editarEnderecoBtn && formEndereco) {
        editarEnderecoBtn.addEventListener('click', function () {
            acaoPendente = 'editar-endereco';
            modalConfirmarSenha.style.display = 'block';
        });
    }

    if (cancelarEdicaoBtn) {
        cancelarEdicaoBtn.addEventListener('click', function () {
            // Bloqueia todos os campos novamente
            formPerfil.querySelectorAll('input, select').forEach(input => {
                if (input.tagName === 'SELECT') {
                    input.disabled = true;
                } else {
                    input.setAttribute('readonly', true);
                }
                input.style.backgroundColor = '#f5f5f5';
                input.style.borderColor = '#ddd';
            });

            document.getElementById('form-actions-perfil').style.display = 'none';
            editarPerfilBtn.style.display = 'block';

            mostrarMensagemTemporaria('Edição cancelada', 'info');
        });
    }

    if (cancelarEdicaoEnderecoBtn) {
        cancelarEdicaoEnderecoBtn.addEventListener('click', function () {
            // Bloqueia todos os campos de endereço
            formEndereco.querySelectorAll('input, select').forEach(input => {
                if (input.tagName === 'SELECT') {
                    input.disabled = true;
                } else {
                    input.setAttribute('readonly', true);
                }
                input.style.backgroundColor = '#f5f5f5';
                input.style.borderColor = '#ddd';
            });

            document.getElementById('form-actions-endereco').style.display = 'none';
            editarEnderecoBtn.style.display = 'block';

            mostrarMensagemTemporaria('Edição de endereço cancelada', 'info');
        });
    }

    // Cancelar alteração de senha - CORRIGIDO
    if (cancelarAlterarSenhaBtn && formAlterarSenha && btnAlterarSenha) {
        cancelarAlterarSenhaBtn.addEventListener('click', function () {
            console.log('Cancelar alteração de senha clicado');
            formAlterarSenha.style.display = 'none';
            btnAlterarSenha.style.display = 'block';
            if (formNovaSenha) {
                formNovaSenha.reset();
            }
            limparMensagensErro();
        });
    }

    // Formulário de nova senha - CORRIGIDO (REMOVER preventDefault)
    if (formNovaSenha) {
        formNovaSenha.addEventListener('submit', function (e) {
            // REMOVER e.preventDefault() - DEIXAR O FORMULÁRIO SER ENVIADO
            // e.preventDefault();
            
            console.log('Formulário de senha submetido');

            const senhaAtual = document.getElementById('senha-atual').value;
            const novaSenha = document.getElementById('nova-senha').value;
            const confirmarSenha = document.getElementById('confirmar-senha').value;

            // Validações
            if (!validarSenha(senhaAtual, novaSenha, confirmarSenha)) {
                e.preventDefault(); // Só prevenir se houver erro de validação
                return;
            }

            // Mostrar loading
            const btnSubmit = this.querySelector('button[type="submit"]');
            if (btnSubmit) {
                btnSubmit.disabled = true;
                btnSubmit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Alterando...';
            }

            // O formulário será enviado normalmente para o Flask
            // Não precisa fazer nada aqui, o formulário segue o fluxo normal
        });
    }

    // Confirmação de Senha
    if (formConfirmarSenha) {
        formConfirmarSenha.addEventListener('submit', function (e) {
            e.preventDefault();

            const senhaConfirmacao = document.getElementById('senha-confirmacao').value;

            if (!senhaConfirmacao) {
                mostrarMensagemTemporaria('Por favor, digite sua senha.', 'error');
                return;
            }

            // Verificar senha no servidor (simulação)
            verificarSenhaNoServidor(senhaConfirmacao, function (sucesso) {
                if (sucesso) {
                    modalConfirmarSenha.style.display = 'none';
                    formConfirmarSenha.reset();

                    // Executar a ação pendente
                    if (acaoPendente === 'editar-perfil') {
                        liberarEdicaoPerfil();
                    } else if (acaoPendente === 'editar-endereco') {
                        liberarEdicaoEndereco();
                    }

                    acaoPendente = null;
                } else {
                    mostrarMensagemTemporaria('Senha incorreta. Tente novamente.', 'error');
                }
            });
        });
    }

    if (cancelarConfirmacaoBtn) {
        cancelarConfirmacaoBtn.addEventListener('click', function () {
            modalConfirmarSenha.style.display = 'none';
            formConfirmarSenha.reset();
            acaoPendente = null;
        });
    }

    // Toggle para mostrar/ocultar senha
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('i');

            if (passwordInput && passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else if (passwordInput) {
                passwordInput.type = 'password';
                icon.className = 'fas fa-eye';
            }
        });
    });

    // Exclusão de conta - CORRIGIDO (enviar formulário em vez de simular)
    const excluirContaBtn = document.getElementById('excluir-conta');
    const modalExcluir = document.getElementById('modal-excluir');
    const modalClose = document.querySelector('.modal-close');
    const cancelarExclusaoBtn = document.getElementById('cancelar-exclusao');
    const confirmarExclusaoBtn = document.getElementById('confirmar-exclusao');

    if (excluirContaBtn) {
        excluirContaBtn.addEventListener('click', function () {
            if (modalExcluir) modalExcluir.style.display = 'block';
        });
    }

    if (modalClose) {
        modalClose.addEventListener('click', function () {
            if (modalExcluir) modalExcluir.style.display = 'none';
        });
    }

    if (cancelarExclusaoBtn) {
        cancelarExclusaoBtn.addEventListener('click', function () {
            if (modalExcluir) modalExcluir.style.display = 'none';
        });
    }

    if (confirmarExclusaoBtn) {
        confirmarExclusaoBtn.addEventListener('click', function () {
            // Criar um formulário dinâmico para exclusão
            const formExcluir = document.createElement('form');
            formExcluir.method = 'POST';
            formExcluir.action = '/excluirConta';
            
            document.body.appendChild(formExcluir);
            formExcluir.submit();
        });
    }

    window.addEventListener('click', function (e) {
        if (e.target === modalExcluir) {
            modalExcluir.style.display = 'none';
        }
        if (e.target === modalConfirmarSenha) {
            modalConfirmarSenha.style.display = 'none';
            formConfirmarSenha.reset();
            acaoPendente = null;
        }
    });

    // Filtros de reservas e pagamentos
    const filtroStatus = document.getElementById('filtro-status');
    const filtroPagamento = document.getElementById('filtro-pagamento');

    if (filtroStatus) {
        filtroStatus.addEventListener('change', function () {
            mostrarMensagemTemporaria(`Filtrando por: ${this.options[this.selectedIndex].text}`, 'info');
        });
    }

    if (filtroPagamento) {
        filtroPagamento.addEventListener('change', function () {
            mostrarMensagemTemporaria(`Filtrando por: ${this.options[this.selectedIndex].text}`, 'info');
        });
    }

    // Ações de reservas
    const botoesReserva = document.querySelectorAll('.reserva-actions .btn-action');

    botoesReserva.forEach(botao => {
        botao.addEventListener('click', function () {
            const acao = this.textContent.trim();

            switch (acao) {
                case 'Detalhes':
                    mostrarMensagemTemporaria('Abrindo detalhes da reserva...', 'info');
                    break;
                case 'Cancelar':
                    if (confirm('Tem certeza que deseja cancelar esta reserva?')) {
                        mostrarMensagemTemporaria('Reserva cancelada com sucesso!', 'success');
                        this.closest('.reserva-item').querySelector('.reserva-status').textContent = 'Cancelada';
                        this.closest('.reserva-item').querySelector('.reserva-status').className = 'reserva-status cancelada';
                        this.remove();
                    }
                    break;
                case 'Avaliar':
                    mostrarMensagemTemporaria('Abrindo formulário de avaliação...', 'info');
                    break;
            }
        });
    });

    // Ações de pagamentos
    const botoesPagamento = document.querySelectorAll('.pagamento-actions .btn-action');

    botoesPagamento.forEach(botao => {
        botao.addEventListener('click', function () {
            const acao = this.textContent.trim();

            switch (acao) {
                case 'Pagar':
                    mostrarMensagemTemporaria('Abrindo página de pagamento...', 'info');
                    break;
                case 'Detalhes':
                    mostrarMensagemTemporaria('Abrindo detalhes da fatura...', 'info');
                    break;
                case 'Comprovante':
                    mostrarMensagemTemporaria('Baixando comprovante...', 'info');
                    break;
            }
        });
    });

    // Validação de campos de endereço quando editados
    const camposEndereco = document.querySelectorAll('#form-endereco input, #form-endereco select');
    camposEndereco.forEach(campo => {
        campo.addEventListener('blur', function() {
            if (!this.hasAttribute('readonly') && !this.disabled) {
                validarCampoEndereco(this);
            }
        });
    });
}

// ===== VALIDAÇÃO DE CAMPOS DE ENDEREÇO =====
function validarCampoEnderepo(campo) {
    const valor = campo.value.trim();
    let erro = '';

    const validacoes = {
        'cep': () => {
            const cepNumeros = valor.replace(/\D/g, '');
            if (cepNumeros.length !== 8) return 'CEP deve conter 8 dígitos.';
            if (!/^[0-9]{8}$/.test(cepNumeros)) return 'CEP inválido.';
            return '';
        },
        'logradouro': () => {
            if (!valor) return 'Logradouro é obrigatório.';
            if (valor.length < 3) return 'Logradouro muito curto.';
            return '';
        },
        'numero': () => {
            if (!valor) return 'Número é obrigatório.';
            return '';
        },
        'bairro': () => {
            if (!valor) return 'Bairro é obrigatório.';
            if (valor.length < 2) return 'Bairro muito curto.';
            return '';
        },
        'cidade': () => {
            if (!valor) return 'Cidade é obrigatória.';
            if (valor.length < 2) return 'Cidade muito curta.';
            return '';
        },
        'estado': () => {
            if (!valor) return 'Estado é obrigatório.';
            if (valor.length !== 2) return 'Estado deve ter 2 caracteres.';
            return '';
        },
        'complemento': () => {
            // Complemento é opcional, sem validação específica
            return '';
        }
    };

    // Para campos de empresa (com prefixo empresa_)
    const campoId = campo.id.replace('empresa_', '');
    if (validacoes[campoId]) {
        erro = validacoes[campoId]();
    }

    mostrarMensagemErroEndereco(campo, erro);
}

function mostrarMensagemErroEndereco(campo, erro) {
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

// ===== FUNÇÕES AUXILIARES PARA SENHA =====

function liberarEdicaoPerfil() {
    const formPerfil = document.getElementById('form-perfil');
    const editarPerfilBtn = document.getElementById('editar-perfil');

    // Determina se é PJ ou PF
    const isPJ = document.getElementById('CNPJ') !== null;
    const camposEditaveisPF = ['email', 'telefone', 'celular', 'cnh'];
    const camposEditaveisPJ = ['email', 'telefone', 'celular', 'ramo', 'tamanho', 'representante', 'cargo_representante'];
    const camposLiberar = isPJ ? camposEditaveisPJ : camposEditaveisPF;

    // Libera apenas os campos permitidos
    formPerfil.querySelectorAll('input, select').forEach(input => {
        const fieldName = input.name || input.id;
        if (camposLiberar.includes(fieldName)) {
            if (input.tagName === 'SELECT') {
                input.disabled = false;
            } else {
                input.removeAttribute('readonly');
            }
            input.style.backgroundColor = '#fff';
            input.style.borderColor = '#3669a4';
        }
    });

    document.getElementById('form-actions-perfil').style.display = 'flex';
    editarPerfilBtn.style.display = 'none';

    mostrarMensagemTemporaria('Dados liberados para edição', 'success');
}

function liberarEdicaoEndereco() {
    const formEndereco = document.getElementById('form-endereco');
    const editarEnderecoBtn = document.getElementById('editar-endereco');

    // Libera todos os campos de endereço (incluindo o select de estado)
    formEndereco.querySelectorAll('input, select').forEach(input => {
        if (input.tagName === 'SELECT') {
            input.disabled = false;
        } else {
            input.removeAttribute('readonly');
        }
        input.style.backgroundColor = '#fff';
        input.style.borderColor = '#3669a4';
    });

    document.getElementById('form-actions-endereco').style.display = 'flex';
    editarEnderecoBtn.style.display = 'none';

    mostrarMensagemTemporaria('Endereço liberado para edição', 'success');
}

function validarSenha(senhaAtual, novaSenha, confirmarSenha) {
    let valido = true;
    limparMensagensErro();

    console.log('Validando senhas...');

    // Validar senha atual
    if (!senhaAtual || senhaAtual.length === 0) {
        mostrarErroCampo('senha-atual', 'Digite sua senha atual');
        valido = false;
    }

    // Validar nova senha
    if (!novaSenha || novaSenha.length < 6) {
        mostrarErroCampo('nova-senha', 'A senha deve ter pelo menos 6 caracteres');
        valido = false;
    }

    // Validar confirmação
    if (!confirmarSenha || novaSenha !== confirmarSenha) {
        mostrarErroCampo('confirmar-senha', 'As senhas não coincidem');
        valido = false;
    }

    // Validar se nova senha é diferente da atual
    if (novaSenha && senhaAtual && novaSenha === senhaAtual) {
        mostrarErroCampo('nova-senha', 'A nova senha deve ser diferente da atual');
        valido = false;
    }

    console.log('Validação resultado:', valido);
    return valido;
}

function mostrarErroCampo(campoId, mensagem) {
    const campo = document.getElementById(campoId);
    if (!campo) {
        console.error('Campo não encontrado:', campoId);
        return;
    }
    
    campo.classList.add('campo-erro');

    // Remove mensagem de erro anterior se existir
    const erroAnterior = campo.parentNode.querySelector('.mensagem-erro');
    if (erroAnterior) {
        erroAnterior.remove();
    }

    // Adiciona nova mensagem de erro
    const mensagemErro = document.createElement('span');
    mensagemErro.className = 'mensagem-erro';
    mensagemErro.textContent = mensagem;
    campo.parentNode.appendChild(mensagemErro);
}

function limparMensagensErro() {
    document.querySelectorAll('.mensagem-erro').forEach(erro => erro.remove());
    document.querySelectorAll('.campo-erro').forEach(campo => campo.classList.remove('campo-erro'));
}

// ===== SIMULAÇÃO DE CHAMADAS AO SERVIDOR =====

function alterarSenhaNoServidor(senhaAtual, novaSenha) {
    console.log('Enviando senha para o servidor...');

    // Simular requisição AJAX
    mostrarMensagemTemporaria('Alterando senha...', 'info');

    setTimeout(() => {
        // Simular sucesso (na prática, você faria uma requisição real)
        const sucesso = true; // Simular sucesso

        if (sucesso) {
            mostrarMensagemTemporaria('Senha alterada com sucesso!', 'success');
            const formAlterarSenha = document.getElementById('form-alterar-senha');
            const btnAlterarSenha = document.getElementById('btn-alterar-senha');
            const formNovaSenha = document.getElementById('form-nova-senha');
            
            if (formAlterarSenha) formAlterarSenha.style.display = 'none';
            if (btnAlterarSenha) btnAlterarSenha.style.display = 'block';
            if (formNovaSenha) {
                formNovaSenha.reset();
                limparMensagensErro();
            }
        } else {
            mostrarMensagemTemporaria('Erro ao alterar senha. Verifique a senha atual.', 'error');
        }
    }, 1500);
}

function verificarSenhaNoServidor(senha, callback) {
    // Simular verificação no servidor
    setTimeout(() => {
        // Na prática, você faria uma requisição real para verificar a senha
        const senhaCorreta = true; // Simular senha correta

        callback(senhaCorreta);
    }, 1000);
}

// ===== FUNÇÃO DE UPLOAD DE IMAGEM =====
function initImageUpload() {
    const fileInput = document.getElementById('file-input');
    const avatarImage = document.getElementById('avatar-image');
    const alterarFotoBtn = document.getElementById('alterar-foto');

    if (alterarFotoBtn && fileInput && avatarImage) {
        alterarFotoBtn.addEventListener('click', function () {
            fileInput.click();
        });

        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                // Verifica se é uma imagem
                if (!file.type.startsWith('image/')) {
                    mostrarMensagemTemporaria('Por favor, selecione uma imagem válida.', 'error');
                    return;
                }

                // Verifica o tamanho do arquivo (máximo 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    mostrarMensagemTemporaria('A imagem deve ter no máximo 5MB.', 'error');
                    return;
                }

                const reader = new FileReader();

                reader.onload = function (e) {
                    avatarImage.src = e.target.result;
                    mostrarMensagemTemporaria('Foto atualizada com sucesso!', 'success');

                    // Aqui você pode adicionar código para salvar a imagem no servidor
                    // salvarImagemNoServidor(e.target.result);
                };

                reader.onerror = function () {
                    mostrarMensagemTemporaria('Erro ao carregar a imagem.', 'error');
                };

                reader.readAsDataURL(file);
            }
        });
    }
}

// ===== FUNÇÃO AUXILIAR PARA MENSAGENS TEMPORÁRIAS =====
function mostrarMensagemTemporaria(mensagem, tipo = 'info') {
    const mensagemEl = document.createElement('div');
    mensagemEl.className = `mensagem-temporaria mensagem-${tipo}`;
    mensagemEl.textContent = mensagem;

    Object.assign(mensagemEl.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 20px',
        borderRadius: '6px',
        color: 'white',
        fontWeight: '600',
        zIndex: '10000',
        boxShadow: '0 5px 15px rgba(0,0,0,0.2)',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });

    const cores = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };

    mensagemEl.style.backgroundColor = cores[tipo] || cores.info;

    document.body.appendChild(mensagemEl);

    setTimeout(() => {
        mensagemEl.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        mensagemEl.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (mensagemEl.parentNode) {
                mensagemEl.parentNode.removeChild(mensagemEl);
            }
        }, 300);
    }, 3000);
}