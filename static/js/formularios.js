/*
 * AutoFácil - Script Formulários
 * Funcionalidades para login e cadastro
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    if (currentPage === 'cadastro' || currentPage === 'aluguel-mensal' || currentPage === 'login' || currentPage === 'login-colaborador') {
        initToggle();
    }

    if (currentPage === 'cadastro' || currentPage === 'login' || currentPage === 'login-colaborador'){
        initFormularios();
    }
});

// ====== FORMULÁRIOS ======
function initFormularios() {
    const inputs = document.querySelectorAll('input');

    inputs.forEach(input => {
        input.addEventListener('blur', function () {
            validarCampo(this);
        });
    });

    const radios = document.querySelectorAll('.tipo-conta-radio');

    radios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.form) this.form.submit();
        });
    });

    // Adicionar evento para buscar CEP quando o campo perder o foco
    const cepInputs = document.querySelectorAll('#cep, #cep_empresa');
    cepInputs.forEach(cepInput => {
        cepInput.addEventListener('blur', function() {
            buscarEnderecoPorCEP(this);
        });
    });
}

// ====== API DE CEP ======
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
            mostrarMensagemErro(cepInput, 'CEP não encontrado.');
            return;
        }

        // Preencher campos de endereço automaticamente
        preencherEndereco(dados, cepInput.id);

    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
        cepInput.classList.remove('carregando');
        mostrarMensagemErro(cepInput, 'Erro ao buscar CEP. Tente novamente.');
    }
}

// ====== PREENCHER ENDEREÇO ======
function preencherEndereco(dados, cepFieldId) {
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
            
            // Disparar evento de blur para validar o campo preenchido
            setTimeout(() => {
                campo.dispatchEvent(new Event('blur'));
            }, 100);
        }
    });

    // Preencher número e complemento se estiverem vazios (opcional)
    const numeroField = document.getElementById(`${prefix}numero`);
    const complementoField = document.getElementById(`${prefix}complemento`);
    
    if (numeroField && !numeroField.value) {
        numeroField.focus(); // Foca no campo número para usuário preencher
    }
    
    if (complementoField && dados.complemento && !complementoField.value) {
        complementoField.value = dados.complemento;
    }
}

// ==== TOGGLE PASSWORD ======
function initToggle(){
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

            if (isNaN(dataNasc.getTime())) return 'Data de nascimento inválida.';

            if (anoNasc < 1900) return 'Data de nascimento inválida.';
            if (anoNasc > anoAtual) return 'Data de nascimento inválida.';

            let idade = anoAtual - anoNasc;
            const mesAtual = hoje.getMonth();
            const diaAtual = hoje.getDate();
            const mesNasc = dataNasc.getMonth();
            const diaNasc = dataNasc.getDate();

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
        },

        // Novas validações para campos de endereço
        'logradouro': () => {
            if (!valor) return 'Logradouro é obrigatório.';
            if (valor.length < 3) return 'Logradouro muito curto.';
            return '';
        },

        'empresa_logradouro': () => {
            if (!valor) return 'Logradouro é obrigatório.';
            if (valor.length < 3) return 'Logradouro muito curto.';
            return '';
        },

        'bairro': () => {
            if (!valor) return 'Bairro é obrigatório.';
            if (valor.length < 2) return 'Bairro muito curto.';
            return '';
        },

        'empresa_bairro': () => {
            if (!valor) return 'Bairro é obrigatório.';
            if (valor.length < 2) return 'Bairro muito curto.';
            return '';
        },

        'cidade': () => {
            if (!valor) return 'Cidade é obrigatória.';
            if (valor.length < 2) return 'Cidade muito curta.';
            return '';
        },

        'empresa_cidade': () => {
            if (!valor) return 'Cidade é obrigatória.';
            if (valor.length < 2) return 'Cidade muito curta.';
            return '';
        },

        'estado': () => {
            if (!valor) return 'Estado é obrigatório.';
            if (valor.length !== 2) return 'Estado deve ter 2 caracteres.';
            return '';
        },

        'empresa_estado': () => {
            if (!valor) return 'Estado é obrigatório.';
            if (valor.length !== 2) return 'Estado deve ter 2 caracteres.';
            return '';
        },

        'numero': () => {
            if (!valor) return 'Número é obrigatório.';
            return '';
        },

        'empresa_numero': () => {
            if (!valor) return 'Número é obrigatório.';
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

    cpf = cpf.replace(/\D/g, '');

    if (cpf.length !== 11) return 'CPF deve conter 11 dígitos.';

    if (/^(\d)\1+$/.test(cpf)) return 'CPF inválido.';

    let soma = 0;
    let resto;

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

// ====== VALIDAÇÃO DE CNPJ ======
function validarCNPJ(cnpj) {
    if (!cnpj) return 'CNPJ é obrigatório.';

    cnpj = cnpj.replace(/\D/g, '');

    if (cnpj.length !== 14) return 'CNPJ deve conter 14 dígitos.';

    if (/^(\d)\1+$/.test(cnpj)) return 'CNPJ inválido.';

    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }
    let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(0))) return 'CNPJ inválido.';

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