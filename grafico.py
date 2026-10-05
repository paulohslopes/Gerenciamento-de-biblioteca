"""Geração de gráficos com matplotlib (importado só quando necessário)."""


def exibir_grafico(contagem, rotulo_y="Quantidade de livros", arquivo=None):
    """Mostra (ou salva em `arquivo`) um gráfico de barras com {categoria: valor}."""
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    fig, ax = plt.subplots()
    ax.bar(list(contagem.keys()), list(contagem.values()), color="steelblue")
    ax.set_xlabel("Categoria")
    ax.set_ylabel(rotulo_y)
    ax.set_title(f"{rotulo_y} por Categoria")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()

    if arquivo:
        fig.savefig(arquivo)
        plt.close(fig)
    else:
        plt.show()
