"""Sistema de Biblioteca - interface de terminal."""

import biblioteca as b

MENU = """
======================================
       SISTEMA DA BIBLIOTECA
======================================
1 - Pesquisar livro
2 - Cadastrar livro
3 - Remover livro
4 - Ver gráfico por categoria
5 - Listar acervo
6 - Emprestar livro
7 - Devolver livro
8 - Sair do sistema
======================================"""


# ---------- Entrada de dados ----------

def pedir(mensagem, validador):
    """Repete a pergunta até o validador aceitar a resposta."""
    while True:
        try:
            return validador(input(mensagem))
        except ValueError as erro:
            print(erro)


# ---------- Ações do menu ----------

def pesquisar(acervo):
    termo = input("\nDigite o título ou autor que deseja pesquisar: ")
    encontrados = b.buscar_livros(acervo, termo)

    if not encontrados:
        print(f"\nNenhum livro encontrado para '{termo.strip()}'.")
        return

    print(f"\n--- {len(encontrados)} livro(s) encontrado(s) ---")
    for livro in encontrados:
        print(f"\nTítulo: {livro.titulo}")
        print(f"Autor: {livro.autor}")
        print(f"Ano: {livro.ano}")
        print(f"Categoria: {livro.categoria}")
        print(f"Exemplares: {livro.quantidade} (disponíveis: {livro.disponivel})")


def cadastrar(acervo):
    print("\n============================")
    print("      CADASTRO DE LIVRO")
    print("============================")

    titulo = pedir("Digite o título: ", lambda v: b.validar_texto(v, "O título"))
    autor = pedir("Digite o autor: ", lambda v: b.validar_texto(v, "O autor"))
    ano = pedir("Digite o ano de publicação: ", b.validar_ano)
    categoria = pedir("Digite a categoria: ", lambda v: b.validar_texto(v, "A categoria"))
    quantidade = pedir("Digite a quantidade em estoque: ", b.validar_quantidade)

    livro, novo = b.adicionar_livro(acervo, b.criar_livro(titulo, autor, ano, categoria, quantidade))

    if novo:
        print(f"\nLivro '{livro.titulo}' adicionado com sucesso!")
    else:
        print(f"\n'{livro.titulo}' já estava no acervo. Estoque atualizado para {livro.quantidade} exemplar(es).")
    return True


def remover(acervo):
    titulo = input("\nDigite o título do livro que deseja remover: ")
    livro = b.encontrar_livro(acervo, titulo)

    if livro is None:
        print(f"\nLivro '{titulo.strip()}' não encontrado no acervo.")
        return False

    if input(f"Confirma remover '{livro.titulo}'? (s/n): ").strip().lower() != "s":
        print("Operação cancelada.")
        return False

    b.remover_livro(acervo, livro.titulo)
    print(f"\nLivro '{livro.titulo}' removido com sucesso!")
    return True


def mostrar_grafico(acervo):
    if not acervo:
        print("\nNão existem livros cadastrados para gerar o gráfico.")
        return

    print("\n1 - Títulos por categoria")
    print("2 - Exemplares por categoria")
    escolha = input("Escolha: ").strip()
    if escolha == "1":
        por, rotulo = "titulos", "Quantidade de títulos"
    elif escolha == "2":
        por, rotulo = "exemplares", "Quantidade de exemplares"
    else:
        print("Opção inválida.")
        return

    try:
        from grafico import exibir_grafico
        exibir_grafico(b.contar_por_categoria(acervo, por), rotulo)
    except ImportError:
        print("\nPara ver gráficos, instale o matplotlib: pip install matplotlib")


def listar(acervo):
    if not acervo:
        print("\nO acervo está vazio.")
        return

    print("\n --- Acervo da biblioteca ---")
    for livro in acervo:
        print(livro)


def movimentar(acervo, acao, verbo):
    """Empresta ou devolve um livro. `acao` é emprestar_livro ou devolver_livro."""
    titulo = input(f"\nDigite o título do livro que deseja {verbo}: ")
    livro = b.encontrar_livro(acervo, titulo)

    if livro is None:
        print(f"\nLivro '{titulo.strip()}' não encontrado no acervo.")
        return False

    try:
        acao(livro)
    except ValueError as erro:
        print(f"\n{erro}")
        return False

    print(f"\nOperação realizada. Disponíveis de '{livro.titulo}': {livro.disponivel}/{livro.quantidade}")
    return True


# ---------- Programa principal ----------

def main():
    acervo = b.carregar_acervo()
    if acervo:
        print(f"{len(acervo)} livro(s) carregado(s) de {b.ARQUIVO_PADRAO}.")

    try:
        while True:
            print(MENU)
            opcao = input("Digite a opção desejada: ").strip()
            alterou = False

            if opcao == "1":
                pesquisar(acervo)
            elif opcao == "2":
                alterou = cadastrar(acervo)
            elif opcao == "3":
                alterou = remover(acervo)
            elif opcao == "4":
                mostrar_grafico(acervo)
            elif opcao == "5":
                listar(acervo)
            elif opcao == "6":
                alterou = movimentar(acervo, b.emprestar_livro, "emprestar")
            elif opcao == "7":
                alterou = movimentar(acervo, b.devolver_livro, "devolver")
            elif opcao == "8":
                print("\nSaindo do sistema...")
                break
            else:
                print("\nOpção inválida. Por favor, escolha uma opção válida.")

            if alterou:
                b.salvar_acervo(acervo)
    except (KeyboardInterrupt, EOFError):
        print("\n\nSistema encerrado.")


if __name__ == "__main__":
    main()
