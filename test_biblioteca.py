from datetime import date

import pytest

import biblioteca as b


def livro_exemplo(titulo="Dom Casmurro", autor="Machado de Assis", ano=1899,
                  categoria="romance", quantidade=3):
    return b.criar_livro(titulo, autor, ano, categoria, quantidade)


# ---------- Validação ----------

def test_validar_texto():
    assert b.validar_texto("  Ana  ") == "Ana"
    with pytest.raises(ValueError):
        b.validar_texto("   ", "O título")


@pytest.mark.parametrize("entrada, esperado", [("1899", 1899), (" 2000 ", 2000), (1, 1)])
def test_validar_ano_valido(entrada, esperado):
    assert b.validar_ano(entrada) == esperado


@pytest.mark.parametrize("entrada", ["abc", "", "0", "-5", "19.9", str(date.today().year + 1)])
def test_validar_ano_invalido(entrada):
    with pytest.raises(ValueError):
        b.validar_ano(entrada)


@pytest.mark.parametrize("entrada", ["abc", "", "0", "-1", "2.5"])
def test_validar_quantidade_invalida(entrada):
    with pytest.raises(ValueError):
        b.validar_quantidade(entrada)


def test_validar_quantidade_valida():
    assert b.validar_quantidade(" 4 ") == 4


def test_criar_livro_padroniza_categoria():
    livro = livro_exemplo(categoria="  ficção científica ")
    assert livro.categoria == "Ficção Científica"
    assert livro.emprestados == 0


def test_criar_livro_invalido():
    with pytest.raises(ValueError):
        b.criar_livro("", "Autor", 2000, "Cat", 1)


# ---------- Consultas ----------

def test_encontrar_livro_ignora_caixa():
    acervo = [livro_exemplo()]
    assert b.encontrar_livro(acervo, "  dom CASMURRO ") is acervo[0]
    assert b.encontrar_livro(acervo, "Outro") is None


def test_buscar_livros_por_titulo_ou_autor_e_retorna_todos():
    acervo = [
        livro_exemplo("Dom Casmurro", "Machado de Assis"),
        livro_exemplo("Memórias Póstumas", "Machado de Assis"),
        livro_exemplo("Dom Quixote", "Cervantes"),
    ]
    assert len(b.buscar_livros(acervo, "machado")) == 2
    assert len(b.buscar_livros(acervo, "dom")) == 2
    assert b.buscar_livros(acervo, "xyz") == []


def test_contar_por_categoria():
    acervo = [
        livro_exemplo("A", categoria="Romance", quantidade=2),
        livro_exemplo("B", categoria="romance", quantidade=5),
        livro_exemplo("C", categoria="Poesia", quantidade=1),
    ]
    assert b.contar_por_categoria(acervo) == {"Poesia": 1, "Romance": 2}
    assert b.contar_por_categoria(acervo, por="exemplares") == {"Poesia": 1, "Romance": 7}


def test_contar_por_categoria_parametro_invalido():
    with pytest.raises(ValueError):
        b.contar_por_categoria([], por="outro")


# ---------- Alterações ----------

def test_adicionar_livro_novo():
    acervo = []
    livro, novo = b.adicionar_livro(acervo, livro_exemplo())
    assert novo is True
    assert acervo == [livro]


def test_adicionar_livro_repetido_soma_estoque():
    acervo = []
    b.adicionar_livro(acervo, livro_exemplo(quantidade=2))
    livro, novo = b.adicionar_livro(acervo, livro_exemplo("dom casmurro", "MACHADO DE ASSIS", quantidade=3))
    assert novo is False
    assert len(acervo) == 1
    assert livro.quantidade == 5


def test_mesmo_titulo_autor_diferente_nao_funde():
    acervo = []
    b.adicionar_livro(acervo, livro_exemplo("Versos", "Autor A"))
    b.adicionar_livro(acervo, livro_exemplo("Versos", "Autor B"))
    assert len(acervo) == 2


def test_remover_livro():
    acervo = [livro_exemplo()]
    assert b.remover_livro(acervo, "dom casmurro") is True
    assert acervo == []
    assert b.remover_livro(acervo, "dom casmurro") is False


def test_emprestar_e_devolver():
    livro = livro_exemplo(quantidade=2)
    b.emprestar_livro(livro)
    b.emprestar_livro(livro)
    assert livro.disponivel == 0
    with pytest.raises(ValueError):
        b.emprestar_livro(livro)

    b.devolver_livro(livro)
    assert livro.disponivel == 1


def test_devolver_sem_emprestimo():
    with pytest.raises(ValueError):
        b.devolver_livro(livro_exemplo())


# ---------- Persistência ----------

def test_salvar_e_carregar(tmp_path):
    arquivo = tmp_path / "acervo.json"
    acervo = [livro_exemplo("Pequeno Príncipe", "Saint-Exupéry"), livro_exemplo()]
    b.emprestar_livro(acervo[1])
    b.salvar_acervo(acervo, arquivo)
    assert b.carregar_acervo(arquivo) == acervo


def test_carregar_arquivo_inexistente(tmp_path):
    assert b.carregar_acervo(tmp_path / "nao_existe.json") == []


def test_carregar_arquivo_corrompido(tmp_path):
    arquivo = tmp_path / "acervo.json"
    arquivo.write_text("{ não é json", encoding="utf-8")
    assert b.carregar_acervo(arquivo) == []


def test_carregar_ignora_registros_invalidos(tmp_path):
    arquivo = tmp_path / "acervo.json"
    arquivo.write_text(
        '[{"titulo": "A", "autor": "B", "ano": 2000, "categoria": "C", "quantidade": 1},'
        ' {"titulo": "sem campos"}]',
        encoding="utf-8",
    )
    acervo = b.carregar_acervo(arquivo)
    assert len(acervo) == 1 and acervo[0].titulo == "A"
