### Function to easily plot scatter for variables
import matplotlib.pyplot as plt
import seaborn as sns

def plot_scatter(df, x, y):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x=x, y=y)
    plt.title(f'Relação entre {x} e {y}')
    plt.xlabel(f'{x}')
    plt.ylabel(f'{y}')
    plt.show()