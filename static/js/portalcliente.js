/*
 * AutoFácil - Script Portal do Cliente
 * Funcionalidades para portal do cliente e reservas
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    if (currentPage === 'portal-cliente') {
        initPortalCliente();
    }
});

// ===== PAGINA PORTAL DO CLIENTE ======
function initPortalCliente() {
    // Navegação entre seções
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const portalSections = document.querySelectorAll('.portal-section');
    
    sidebarItems.forEach(item => {
        item.addEventListener('click', function() {
            const target = this.dataset.target;
            
            sidebarItems.forEach(i => i.classList.remove('active'));
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
    const inputsPerfil = formPerfil.querySelectorAll('input');
    
    if (editarPerfilBtn) {
        editarPerfilBtn.addEventListener('click', function() {
            inputsPerfil.forEach(input => {
                input.removeAttribute('readonly');
            });
            formActionsPerfil.style.display = 'block';
            this.style.display = 'none';
        });
    }
    
    if (cancelarEdicaoBtn) {
        cancelarEdicaoBtn.addEventListener('click', function() {
            inputsPerfil.forEach(input => {
                input.setAttribute('readonly', true);
            });
            formActionsPerfil.style.display = 'none';
            editarPerfilBtn.style.display = 'block';
            
            mostrarMensagemTemporaria('Edição cancelada', 'info');
        });
    }
    
    if (formPerfil) {
        formPerfil.addEventListener('submit', function(e) {
            //e.preventDefault();
            
            inputsPerfil.forEach(input => {
                input.setAttribute('readonly', true);
            });
            formActionsPerfil.style.display = 'none';
            editarPerfilBtn.style.display = 'block';
            
            mostrarMensagemTemporaria('Perfil atualizado com sucesso!', 'success');
        });
    }
    
    // Exclusão de conta
    const excluirContaBtn = document.getElementById('excluir-conta');
    const modalExcluir = document.getElementById('modal-excluir');
    const modalClose = document.querySelector('.modal-close');
    const cancelarExclusaoBtn = document.getElementById('cancelar-exclusao');
    const confirmarExclusaoBtn = document.getElementById('confirmar-exclusao');
    
    if (excluirContaBtn) {
        excluirContaBtn.addEventListener('click', function() {
            modalExcluir.style.display = 'block';
        });
    }
    
    if (modalClose) {
        modalClose.addEventListener('click', function() {
            modalExcluir.style.display = 'none';
        });
    }
    
    if (cancelarExclusaoBtn) {
        cancelarExclusaoBtn.addEventListener('click', function() {
            modalExcluir.style.display = 'none';
        });
    }
    
    if (confirmarExclusaoBtn) {
        confirmarExclusaoBtn.addEventListener('click', function() {
            modalExcluir.style.display = 'none';
            mostrarMensagemTemporaria('Conta excluída com sucesso!', 'success');
            
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        });
    }
    
    window.addEventListener('click', function(e) {
        if (e.target === modalExcluir) {
            modalExcluir.style.display = 'none';
        }
    });
    
    // Filtros de reservas e pagamentos
    const filtroStatus = document.getElementById('filtro-status');
    const filtroPagamento = document.getElementById('filtro-pagamento');
    
    if (filtroStatus) {
        filtroStatus.addEventListener('change', function() {
            mostrarMensagemTemporaria(`Filtrando por: ${this.options[this.selectedIndex].text}`, 'info');
        });
    }
    
    if (filtroPagamento) {
        filtroPagamento.addEventListener('change', function() {
            mostrarMensagemTemporaria(`Filtrando por: ${this.options[this.selectedIndex].text}`, 'info');
        });
    }
    
    // Ações de reservas
    const botoesReserva = document.querySelectorAll('.reserva-actions .btn-action');
    
    botoesReserva.forEach(botao => {
        botao.addEventListener('click', function() {
            const acao = this.textContent.trim();
            
            switch(acao) {
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
        botao.addEventListener('click', function() {
            const acao = this.textContent.trim();
            
            switch(acao) {
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
}