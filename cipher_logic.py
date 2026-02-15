import unicodedata

def limpar_acentos(texto):
    """
    Remove acentos e normaliza o texto para 'limpar' a string.
    Exemplo: 'Coração' -> 'CORACAO'
    """
    if not texto:
        return ""
    # Converte para maiúsculas primeiro para padronizar
    texto = texto.upper()
    # Normaliza e remove acentos
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def criptografar_versiculo(texto, nivel):
    """
    Transforma o texto em números baseados no nível, 
    ignorando acentos e espaços.
    """
    resultado = []
    texto_limpo = limpar_acentos(texto) # Já retorna em caixa alta
    
    for letra in texto_limpo:
        if 'A' <= letra <= 'Z':
            # Posição base (A=1, B=2...)
            posicao_base = ord(letra) - 64
            
            # Lógica dinâmica por nível
            if nivel == 1:
                numero = posicao_base + 5
            elif nivel == 2:
                numero = posicao_base + 10
            elif nivel == 3:
                numero = (posicao_base * 2) + 3
            elif nivel == 4:
                numero = (posicao_base + 15) - 2
            else: # Nível 5
                numero = (posicao_base * 3) + nivel
                
            resultado.append(str(numero))
        
        elif letra == " ":
            resultado.append("-") 
        
        elif letra in "-.,;:":
            resultado.append(letra)
            
    return " ".join(resultado)

def verificar_resposta(entrada_usuario, original):
    """
    Compara a resposta do usuário com o original de forma flexível.
    Aceita maiúsculas, minúsculas e ignora acentos.
    """
    u = limpar_acentos(entrada_usuario)
    o = limpar_acentos(original)
    return u.strip() == o.strip()