/*
 * AutoFácil - Script Colaboradores
 * Funcionalidades para páginas de colaboradores
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    if (currentPage === 'colaborador') {
        initColaborador();
    }
});

// ===== PAGINA DO COLABORADOR =====
function initColaborador() {
    const perfilCards = document.querySelectorAll('.perfil-card');
    const perfilContents = document.querySelectorAll('.perfil-content');

    function determinarPerfilPadrao() {
        const cargo = document.body.dataset.colabCargo;
        
        const mapeamento = {
            'admin': 'administrador',
            'gerente': 'gerente', 
            'atendente': 'atendente',
            'suporte': 'suporte'
        };
        
        return mapeamento[cargo] || 'atendente';
    }
    
    let perfilAtivo = determinarPerfilPadrao();
    
    function ocultarPerfisNaoPermitidos() {
        const cargoUsuario = document.body.dataset.colabCargo;
        
        const permissoes = {
            'admin': ['atendente', 'gerente', 'administrador', 'suporte'],
            'gerente': ['gerente'], 
            'atendente': ['atendente'], 
            'suporte': ['suporte'] 
        };
        
        const perfisPermitidos = permissoes[cargoUsuario] || ['atendente'];
        
        perfilCards.forEach(card => {
            const perfilCard = card.dataset.perfil;
            if (!perfisPermitidos.includes(perfilCard)) {
                card.style.display = 'none';
            }
        });
    }
    
    ocultarPerfisNaoPermitidos();
    
    function ativarPerfil(perfil) {
        perfilAtivo = perfil;
        
        perfilCards.forEach(card => {
            if (card.style.display !== 'none') {
                card.classList.remove('active');
                card.setAttribute('aria-pressed', 'false');
            }
        });
        
        const cardAtivo = document.querySelector(`.perfil-card[data-perfil="${perfil}"]`);
        if (cardAtivo && cardAtivo.style.display !== 'none') {
            cardAtivo.classList.add('active');
            cardAtivo.setAttribute('aria-pressed', 'true');
        }
        
        perfilContents.forEach(content => {
            content.classList.remove('active');
            content.setAttribute('aria-hidden', 'true');
        });
        
        const conteudoAtivo = document.getElementById(`${perfil}-content`);
        if (conteudoAtivo) {
            conteudoAtivo.classList.add('active');
            conteudoAtivo.setAttribute('aria-hidden', 'false');
            
            setTimeout(() => {
                conteudoAtivo.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 100);
        }
    }

    perfilCards.forEach(card => {
        if (card.style.display !== 'none') {
            card.addEventListener('click', function () {
                const perfil = this.dataset.perfil;
                ativarPerfil(perfil);
            });
            
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const perfil = this.dataset.perfil;
                    ativarPerfil(perfil);
                }
            });
            
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
            card.setAttribute('aria-pressed', 'false');
        }
    });

    function verificarHashURL() {
        const hash = window.location.hash.substring(1);
        const perfisValidos = ['atendente', 'gerente', 'administrador', 'suporte'];

        if (perfisValidos.includes(hash)) {
            ativarPerfil(hash);
        }
    }

    verificarHashURL();

    const botoesAcao = document.querySelectorAll('.btn-action, .btn-card-action, .btn-relatorio, .btn-admin');

    botoesAcao.forEach(botao => {
        botao.addEventListener('click', function (e) {
            e.preventDefault();

            const originalText = this.textContent;
            this.textContent = 'Processando...';
            this.disabled = true;

            setTimeout(() => {
                this.textContent = originalText;
                this.disabled = false;

                mostrarMensagemTemporaria('Ação simulada com sucesso!', 'success');
            }, 1000);
        });
    });

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

    function carregarDadosSimulados() {
        setTimeout(() => {
            document.body.classList.add('dados-carregados');
        }, 500);
    }

    carregarDadosSimulados();

    document.addEventListener('keydown', function (e) {
        if (e.altKey) {
            switch (e.key) {
                case '1':
                    e.preventDefault();
                    ativarPerfil('atendente');
                    break;
                case '2':
                    e.preventDefault();
                    ativarPerfil('gerente');
                    break;
                case '3':
                    e.preventDefault();
                    ativarPerfil('administrador');
                    break;
                case '4':
                    e.preventDefault();
                    ativarPerfil('suporte');
                    break;
            }
        }
    });

    ativarPerfil(perfilAtivo);
}
function toggleForm() {
    const f = document.getElementById('form-add-user');
    f.style.display = f.style.display === 'none' ? 'block' : 'none';
  }