const API_URL = "http://127.0.0.1:5000";

// --- FUNÇÃO DO MINI-MODAL ---
function exibirModal(titulo, mensagem, icone = "🛡️") {
    const modal = document.getElementById('custom-modal');
    document.getElementById('modal-title').innerText = titulo;
    document.getElementById('modal-text').innerText = mensagem;
    document.getElementById('modal-icon').innerText = icone;
    
    modal.classList.remove('hidden');

    document.getElementById('modal-close').onclick = () => {
        modal.classList.add('hidden');
    };
}

// Alternar entre telas
document.getElementById('show-register')?.addEventListener('click', () => {
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('register-section').classList.remove('hidden');
});

document.getElementById('show-login')?.addEventListener('click', () => {
    document.getElementById('register-section').classList.add('hidden');
    document.getElementById('login-section').classList.remove('hidden');
});

// Lógica de Cadastro
document.getElementById('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const user = document.getElementById('reg-user').value;
    const pass = document.getElementById('reg-pass').value;

    // Validação de senha forte (Regex)
    const senhaRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
    if (!senhaRegex.test(pass)) {
        exibirModal("Senha Fraca", "A senha deve ter 6+ caracteres, maiúsculas, minúsculas, números e símbolos.", "⚠️");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();

        if (response.ok) {
            exibirModal("Sucesso!", "Escriba registrado! Agora faça o seu login.", "📜");
            setTimeout(() => location.reload(), 2000);
        } else {
            exibirModal("Erro", data.erro, "❌");
        }
    } catch (err) {
        exibirModal("Erro de Conexão", "O Templo está inacessível no momento.", "🔌");
    }
});

// Lógica de Login
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const user = document.getElementById('login-user').value;
    const pass = document.getElementById('login-pass').value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: user, password: pass })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('usuarioLogado', JSON.stringify({
                id: data.id,
                username: data.username,
                nivel: data.nivel
            }));
            window.location.href = "game.html"; 
        } else {
            exibirModal("Acesso Negado", data.erro, "🚫");
        }
    } catch (err) {
        exibirModal("Erro", "Falha ao conectar ao servidor.", "❌");
    }
});