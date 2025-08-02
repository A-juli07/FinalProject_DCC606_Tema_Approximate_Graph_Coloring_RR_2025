import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def criar_pasta_graficos():
    if not os.path.exists('../graficos'):
        os.makedirs('../graficos')

def carregar_resultados():
    try:
        df = pd.read_csv('../resultados/resultados_completos.csv')
        df['Cores/Vértice'] = df['Cores'] / df['Vertices']
        df['Densidade'] = np.where(df['Vertices'] > 1, 
                                 df['Cores'] / (df['Vertices'] * (df['Vertices'] - 1)/2),
                                 0)
        return df
    except FileNotFoundError:
        print("Erro: Arquivo '../resultados/resultados_completos.csv' não encontrado!")
        print("Execute primeiro o programa principal para gerar os resultados.")
        exit(1)

def salvar_grafico(nome_arquivo):
    caminho = f'../graficos/{nome_arquivo}'
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo em: {caminho}")
    plt.close()

def plotar_comparacao(df):
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    sns.lineplot(data=df, x='Vertices', y='Tempo(ms)', hue='Algoritmo', 
                 style='Algoritmo', markers=True, dashes=False)
    plt.title('Tempo de Execução por Tamanho do Grafo')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (ms)')
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    sns.lineplot(data=df, x='Vertices', y='Cores', hue='Algoritmo',
                 style='Algoritmo', markers=True, dashes=False)
    plt.title('Número de Cores por Tamanho do Grafo')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Número de Cores')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    sns.lineplot(data=df, x='Vertices', y='Cores/Vértice', hue='Algoritmo',
                 style='Algoritmo', markers=True, dashes=False)
    plt.title('Eficiência da Coloração')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Cores por Vértice')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    sns.scatterplot(data=df, x='Tempo(ms)', y='Cores', hue='Algoritmo',
                    size='Vertices', sizes=(50, 200))
    plt.title('Relação Tempo vs Qualidade')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Número de Cores')
    plt.grid(True)
    
    plt.tight_layout()
    salvar_grafico('comparacao_algoritmos.png')

def plotar_complexidade(df):
    plt.figure(figsize=(10, 6))
    
    for algoritmo in df['Algoritmo'].unique():
        subset = df[df['Algoritmo'] == algoritmo]
        x = subset['Vertices']
        y = subset['Tempo(ms)']
        valid = (x > 0) & (y > 0)
        x_valid = x[valid]
        y_valid = y[valid]
        
        if len(x_valid) > 1:
            coef = np.polyfit(np.log(x_valid), np.log(y_valid), 1)
            y_ajuste = np.exp(coef[1]) * (x_valid ** coef[0])
            plt.loglog(x_valid, y_valid, 'o', label=f'{algoritmo} (dados)')
            plt.loglog(x_valid, y_ajuste, '--', label=f'{algoritmo} ~ O(n^{coef[0]:.2f})')
    
    plt.title('Análise de Complexidade Temporal')
    plt.xlabel('Número de Vértices (log)')
    plt.ylabel('Tempo (ms) (log)')
    plt.legend()
    plt.grid(True)
    salvar_grafico('complexidade_temporal.png')

def main():
    print("\n=== Visualização de Resultados de Coloração de Grafos ===")
    criar_pasta_graficos()
    df = carregar_resultados()
    
    print("\nGerando gráficos comparativos...")
    plotar_comparacao(df)
    
    print("\nAnalisando complexidade temporal...")
    plotar_complexidade(df)
    
    print("\nProcesso concluído! Todos os gráficos foram salvos em: ../graficos/")

if __name__ == "__main__":
    main()
