# 📖 Sistema de Biblioteca

Sistema de terminal em Python para gerenciar o acervo de uma biblioteca: cadastro, busca, empréstimos e gráficos por categoria, com os dados salvos em arquivo JSON.

## Funcionalidades

- Cadastro de livros com validação (título, autor, categoria obrigatórios; ano válido; quantidade ≥ 1)
- Cadastro repetido (mesmo título e autor) soma os exemplares em vez de duplicar
- Pesquisa por título ou autor (parcial, sem diferenciar maiúsculas), mostrando todos os resultados
- Remoção com confirmação
- Empréstimo e devolução com controle de exemplares disponíveis
- Gráfico de barras por categoria (títulos ou exemplares), feito com matplotlib
- Persistência automática em `acervo.json`
- Testes automatizados com `pytest`

## Como executar

Requer Python 3.8+.

```bash
pip install -r requirements.txt
python main.py
```

O matplotlib só é necessário para a opção de gráfico; o restante funciona sem ele.

## Como rodar os testes

```bash
pytest
```

## Estrutura

```
sistema-biblioteca/
├── main.py              # interface de terminal (menu e entrada/saída)
├── biblioteca.py        # lógica: livros, validação, busca e persistência
├── grafico.py           # geração do gráfico com matplotlib
├── test_biblioteca.py   # testes automatizados
├── requirements.txt
└── README.md
```

A lógica é separada da interface, o que torna o código testável e reutilizável (por exemplo, em uma futura versão web).

## Próximos passos

- Registrar quem pegou cada livro emprestado e a data de devolução
- Interface web com Flask ou Streamlit
- Exportar o acervo para CSV

## Autor

Paulo Henrique — [GitHub](https://github.com/paulohslopes)
