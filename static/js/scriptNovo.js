/*
TAREFAS:
  * Organizar código
  * Validação do lado do cliente
  * addEventListener('DOMContentLoaded') + verificação do id da página
*/

document.addEventListener('DOMContentLoaded', function(){
    switch (document.title){
        case 'Cadastro':
            const formulario = document.getElementById('cadastroForm')
            if (formulario.getAttribute('data-form') === 'PF'){
                //bloco
            }
            break;
        case 'Login':
            //bloco
            break;
        case 'Home':
            //bloco
            break;
    }
})