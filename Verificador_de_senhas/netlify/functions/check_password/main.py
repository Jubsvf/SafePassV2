import json
import re

def validar_senha(senha): [cite: 1]
    criterios = { [cite: 1]
        "comprimento_minimo": len(senha) >= 8, [cite: 1]
        "maiuscula": bool(re.search(r"[A-Z]", senha)), [cite: 1]
        "minuscula": bool(re.search(r"[a-z]", senha)), [cite: 1]
        "numero": bool(re.search(r"\d", senha)), [cite: 1]
        "especial": bool(re.search(r"[!@#$%^&*()_\-+=]", senha)), [cite: 1]
        "sem_padroes_comuns": not any(p in senha.lower() for p in [ [cite: 1]
            "123456", "abcdef", "senha", "password", "qwerty", "admin", "letmein", "abc123" [cite: 1]
        ]), [cite: 1]
    } [cite: 1]

    pesos = { [cite: 1]
        "comprimento_minimo": 1.5, [cite: 1]
        "maiuscula": 1, [cite: 1]
        "minuscula": 1, [cite: 1]
        "numero": 1, [cite: 1]
        "especial": 1, [cite: 1]
        "sem_padroes_comuns": 1.5, [cite: 1]
    } [cite: 1]

    pontuacao = sum(pesos[c] for c, valido in criterios.items() if valido) [cite: 1]
    total_maximo = sum(pesos.values()) [cite: 1]

    dicas = [] [cite: 1]
    if not criterios ["comprimento_minimo"]: [cite: 1]
        dicas.append("Use pelo menos 8 caracteres.") [cite: 1]
    if not criterios["maiuscula"]: [cite: 2]
        dicas.append("Inclua pelo menos uma letra maiúscula.") [cite: 2]
    if not criterios["minuscula"]: [cite: 2]
        dicas.append("Inclua pelo menos uma letra minúscula.") [cite: 2]
    if not criterios["numero"]: [cite: 2]
        dicas.append("Adicione pelo menos um número.") [cite: 2]
    if not criterios["especial"]: [cite: 2]
        dicas.append("Use pelo menos um caractere especial (ex: @, #, !, %).") [cite: 2]
    if not criterios["sem_padroes_comuns"]: [cite: 2]
        dicas.append("Evite senhas comuns ou previsíveis como '123456', 'senha', etc.") [cite: 2]

    porcentagem = pontuacao / total_maximo [cite: 2]

    if porcentagem == 1: [cite: 2]
        classificacao = "Excelente" [cite: 2]
    elif porcentagem >= 0.85: [cite: 2]
        classificacao = "Muito Forte" [cite: 2]
    elif porcentagem >= 0.7: [cite: 2]
        classificacao = "Forte" [cite: 2]
    elif porcentagem >= 0.5: [cite: 2]
        classificacao = "Media" [cite: 2]
    elif porcentagem >= 0.3: [cite: 2]
        classificacao = "Fraca" [cite: 2]
    else: [cite: 2]
        classificacao = "Muito Fraca" [cite: 2]

    return classificacao, round(pontuacao, 2), dicas [cite: 2]

# Esta é a função especial que o Netlify Functions vai chamar
def handler(event, context):
    try:
        # Pega a senha que foi enviada pelo seu site HTML
        # O Netlify Functions recebe os dados JSON no 'event['body']'
        body = json.loads(event['body'])
        senha_digitada = body.get('password', '')

        # Chama a sua função de validação de senha
        classificacao, score, dicas = validar_senha(senha_digitada)

        # Prepara a resposta que será enviada de volta para o seu site HTML
        return {
            'statusCode': 200, # Significa que deu tudo certo
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # Isso é importante para o navegador permitir a comunicação
            },
            'body': json.dumps({ # Transforma o resultado em texto JSON
                'resultado': classificacao,
                'score': score,
                'dicas': dicas
            })
        }
    except Exception as e:
        # Se acontecer algum erro, envia um erro 500
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }