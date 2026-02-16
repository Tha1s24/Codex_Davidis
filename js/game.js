const API_URL = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost" 
    ? "http://127.0.0.1:5000" 
    : ""; 

let vidas = 5;
let nivelAtual = 1;
let textoOriginal = ""; 

// Seletores do DOM
const cipherDisplay = document.getElementById('cipher-display');
const cipherRef = document.getElementById('cipher-reference');
const livesDisplay = document.getElementById('lives');
const userInput = document.getElementById('user-answer');
const btnCheck = document.getElementById('btn-check');
const displayUsername = document.getElementById('display-username');

function exibirModal(titulo, mensagem, icone = "✨") {
    const modal = document.getElementById('custom-modal');
    if (!modal) return;
    document.getElementById('modal-title').innerText = titulo;
    document.getElementById('modal-text').innerText = mensagem;
    document.getElementById('modal-icon').innerText = icone;
    modal.classList.remove('hidden');
    document.getElementById('modal-close').onclick = () => modal.classList.add('hidden');
}

function carregarDadosUsuario() {
    const usuarioString = localStorage.getItem('usuarioLogado');
    if (usuarioString) {
        const usuario = JSON.parse(usuarioString);
        nivelAtual = usuario.nivel || 1;
        if (displayUsername) displayUsername.innerText = usuario.username;
    } else {
        window.location.href = "index.html";
    }
}

async function carregarDesafio() {
    try {
        const response = await fetch(`${API_URL}/get_desafio/${nivelAtual}`);
        
        if (response.status === 404) {
            exibirModal("Vitória Real", "Você decifrou todos os pergaminhos do Reino!", "🏆");
            return;
        }

        const data = await response.json();
        if (cipherDisplay) cipherDisplay.innerText = data.codigo;
        if (cipherRef) cipherRef.innerText = data.referencia;
        textoOriginal = data.texto_original; 
        atualizarInterface();
    } catch (error) {
        exibirModal("Erro", "Conexão com o Templo perdida.", "❌");
    }
}

function verificarResposta() {
    const normalizar = (str) => {
        if (!str) return "";
        return str.normalize("NFD")
                  .replace(/[\u0300-\u036f]/g, "")
                  .toUpperCase()
                  .trim();
    };

    const palpite = normalizar(userInput.value);
    const respostaCerta = normalizar(textoOriginal);

    if (palpite === "") return;

    if (palpite === respostaCerta) {
        if (nivelAtual === 5) {
            exibirModal("VITÓRIA SUPREMA", "Parabéns, Grande Escriba! Você decifrou o último pergaminho real.", "🏆");
            userInput.value = "";
            return; 
        }

        exibirModal("Sábia Resposta", "O pergaminho foi revelado corretamente.", "🛡️");
        nivelAtual++;
        vidas = 5; 
        userInput.value = "";
        carregarDesafio();
    } else {
        vidas--;
        if (vidas <= 0) {
            exibirModal("Fim de Jornada", "Suas vidas acabaram. Reiniciando estudos...", "💀");
            reiniciarJogo();
        } else {
            exibirModal("Tente Novamente", `Essa tradução não parece correta.`, "❌");
            atualizarInterface();
        }
    }
}

function atualizarInterface() {
    const levelElement = document.getElementById('current-level');
    if (levelElement) levelElement.innerText = nivelAtual;
    if (livesDisplay) livesDisplay.innerText = "🛡️ ".repeat(vidas);
    if (userInput) userInput.focus();
}

function reiniciarJogo() {
    nivelAtual = 1;
    vidas = 5;
    if (userInput) userInput.value = "";
    carregarDesafio();
}

btnCheck?.addEventListener('click', verificarResposta);
userInput?.addEventListener('keypress', (e) => { if (e.key === 'Enter') verificarResposta(); });

window.onload = () => {
    carregarDadosUsuario();
    carregarDesafio();
};