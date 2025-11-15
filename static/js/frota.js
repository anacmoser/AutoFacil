/*
 * AutoFácil - Script Frota
 * Funcionalidades para páginas de aluguel
 */

document.addEventListener('DOMContentLoaded', function () {
    const currentPage = document.body.dataset.page;

    if (currentPage === 'aluguel-mensal') {
        initAluguelMensal();
    }
});

// ====== PÁGINA ALUGUEL MENSAL ======
function initAluguelMensal() {
    const precos = {
        economico: { 1: 89, 3: 69, 6: 49, 12: 39 },
        intermediario: { 1: 119, 3: 99, 6: 79, 12: 69 },
        suv: { 1: 159, 3: 139, 6: 119, 12: 109 },
        luxo: { 1: 299, 3: 279, 6: 259, 12: 239 }
    };

    const categoriasNomes = {
        economico: "Econômico",
        intermediario: "Intermediário",
        suv: "SUV",
        luxo: "Luxo"
    };

    const periodosNomes = {
        1: "1 mês",
        3: "3 meses",
        6: "6 meses",
        12: "12 meses"
    };

    const btnSimular = document.querySelector('.btn-simular');
    if (btnSimular) {
        btnSimular.addEventListener('click', function () {
            const categoria = document.getElementById('categoria')?.value;
            const periodo = document.getElementById('periodo')?.value;

            if (!categoria || !periodo) {
                alert('Por favor, preencha todos os campos para simular.');
                return;
            }

            const precoDiario = precos[categoria]?.[periodo] || 0;
            const precoMensal = precoDiario * 30;

            document.getElementById('cat-resultado').textContent = categoriasNomes[categoria] || '';
            document.getElementById('periodo-resultado').textContent = periodosNomes[periodo] || '';
            document.getElementById('diaria-resultado').textContent = `R$ ${precoDiario}`;
            document.getElementById('mensal-resultado').textContent = `R$ ${precoMensal}`;

            document.querySelector('.resultado-placeholder').style.display = 'none';
            document.querySelector('.resultado-conteudo').style.display = 'block';
        });
    }

    // FAQ Accordion
    const faqPerguntas = document.querySelectorAll('.faq-pergunta');
    faqPerguntas.forEach(pergunta => {
        pergunta.addEventListener('click', function () {
            const resposta = this.nextElementSibling;
            const toggle = this.querySelector('.faq-toggle');

            document.querySelectorAll('.faq-resposta').forEach(item => {
                if (item !== resposta) {
                    item.style.display = 'none';
                    item.previousElementSibling.querySelector('.faq-toggle').textContent = '+';
                }
            });

            if (resposta.style.display === 'block') {
                resposta.style.display = 'none';
                toggle.textContent = '+';
            } else {
                resposta.style.display = 'block';
                toggle.textContent = '-';
            }
        });
    });
}