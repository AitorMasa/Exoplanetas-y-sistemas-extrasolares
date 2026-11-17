



def etiquetas(ax, total):
    for barras in ax.containers:
        ax.bar_label(barras,fmt=lambda n: f"{n:.0f} ({n / total:.1%})",padding=3)