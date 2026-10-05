"""Lógica do Sistema de Biblioteca: livros, validações, buscas e persistência em JSON.

Este módulo não faz nenhum print/input, o que facilita os testes automatizados.
"""

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

ARQUIVO_PADRAO = Path("acervo.json")


@dataclass
class Livro:
    titulo: str
    autor: str
    ano: int
    categoria: str
    quantidade: int          # total de exemplares no acervo
    emprestados: int = 0     # exemplares atualmente emprestados

    @property
    def disponivel(self):
        return self.quantidade - self.emprestados

    def __str__(self):
        return (f"{self.titulo} | {self.autor} | {self.ano} | {self.categoria} | "
                f"Disponíveis: {self.disponivel}/{self.quantidade}")


# ---------- Validação ----------

def validar_texto(valor, campo="O campo"):
    """Remove espaços extras e garante que o texto não é vazio."""
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"{campo} não pode ficar vazio.")
    return valor


def validar_ano(valor):
    """Converte para int e garante que está entre 1 e o ano atual."""
    try:
        ano = int(str(valor).strip())
    except ValueError:
        raise ValueError("Ano inválido. Digite um número inteiro.") from None

    ano_atual = date.today().year
    if not 1 <= ano <= ano_atual:
        raise ValueError(f"O ano deve estar entre 1 e {ano_atual}.")
    return ano


def validar_quantidade(valor):
    """Converte para int e garante que há pelo menos 1 exemplar."""
    try:
        quantidade = int(str(valor).strip())
    except ValueError:
        raise ValueError("Quantidade inválida. Digite um número inteiro.") from None

    if quantidade < 1:
        raise ValueError("A quantidade deve ser pelo menos 1.")
    return quantidade


def criar_livro(titulo, autor, ano, categoria, quantidade):
    """Valida todos os campos e retorna um Livro. A categoria é padronizada (ex.: 'Ficção Científica')."""
    return Livro(
        titulo=validar_texto(titulo, "O título"),
        autor=validar_texto(autor, "O autor"),
        ano=validar_ano(ano),
        categoria=validar_texto(categoria, "A categoria").title(),
        quantidade=validar_quantidade(quantidade),
    )


# ---------- Consultas ----------

def encontrar_livro(acervo, titulo):
    """Busca exata pelo título (ignorando maiúsculas/minúsculas). Retorna o livro ou None."""
    alvo = titulo.strip().casefold()
    for livro in acervo:
        if livro.titulo.casefold() == alvo:
            return livro
    return None


def buscar_livros(acervo, termo):
    """Retorna todos os livros cujo título ou autor contém o termo."""
    termo = termo.strip().casefold()
    return [l for l in acervo
            if termo in l.titulo.casefold() or termo in l.autor.casefold()]


def contar_por_categoria(acervo, por="titulos"):
    """Conta livros por categoria, em ordem alfabética.

    por="titulos"    -> quantos títulos diferentes há em cada categoria
    por="exemplares" -> soma dos exemplares em cada categoria
    """
    if por not in ("titulos", "exemplares"):
        raise ValueError("O parâmetro 'por' deve ser 'titulos' ou 'exemplares'.")

    contagem = {}
    for livro in acervo:
        categoria = livro.categoria.strip().title()
        peso = 1 if por == "titulos" else livro.quantidade
        contagem[categoria] = contagem.get(categoria, 0) + peso
    return dict(sorted(contagem.items()))


# ---------- Alterações ----------

def adicionar_livro(acervo, livro):
    """Adiciona o livro ao acervo.

    Se já existir um livro com o mesmo título e autor, apenas soma os exemplares.
    Retorna (livro_no_acervo, é_novo).
    """
    for existente in acervo:
        if (existente.titulo.casefold() == livro.titulo.casefold()
                and existente.autor.casefold() == livro.autor.casefold()):
            existente.quantidade += livro.quantidade
            return existente, False

    acervo.append(livro)
    return livro, True


def remover_livro(acervo, titulo):
    """Remove o livro pelo título. Retorna True se removeu, False se não achou."""
    livro = encontrar_livro(acervo, titulo)
    if livro is None:
        return False
    acervo.remove(livro)
    return True


def emprestar_livro(livro):
    if livro.disponivel <= 0:
        raise ValueError("Não há exemplares disponíveis para empréstimo.")
    livro.emprestados += 1


def devolver_livro(livro):
    if livro.emprestados <= 0:
        raise ValueError("Nenhum exemplar deste livro está emprestado.")
    livro.emprestados -= 1


# ---------- Persistência ----------

def salvar_acervo(acervo, caminho=ARQUIVO_PADRAO):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump([asdict(l) for l in acervo], f, ensure_ascii=False, indent=2)


def carregar_acervo(caminho=ARQUIVO_PADRAO):
    """Carrega o acervo do JSON.

    Retorna lista vazia se o arquivo não existir ou estiver corrompido,
    e ignora registros inválidos.
    """
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(dados, list):
        return []

    acervo = []
    for item in dados:
        try:
            acervo.append(Livro(**item))
        except TypeError:
            continue
    return acervo
