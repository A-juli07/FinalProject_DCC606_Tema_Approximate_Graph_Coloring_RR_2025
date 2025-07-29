import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def criar_pasta_graficos():
    """Cria a pasta graficos se não existir"""
    if not os.path.exists('../graficos'):
        os.makedirs('../graficos')

def carregar_resultados():
    """Carrega os dados do arquivo resultados_completos.csv"""
    try:
        df = pd.read_csv('../resultados/resultados_completos.csv')
        
        # Calcula métricas adicionais com tratamento para divisão por zero
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
    """Salva o gráfico atual na pasta graficos"""
    caminho = f'../graficos/{nome_arquivo}'
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo em: {caminho}")
    plt.close()

def plotar_comparacao(df):
    """Gera gráficos comparativos entre os algoritmos"""
    plt.figure(figsize=(15, 10))
    
    # Gráfico 1: Tempo de execução
    plt.subplot(2, 2, 1)
    sns.lineplot(data=df, x='Vertices', y='Tempo(ms)', hue='Algoritmo', 
                 style='Algoritmo', markers=True, dashes=False)
    plt.title('Tempo de Execução por Tamanho do Grafo')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Tempo (ms)')
    plt.grid(True)
    
    # Gráfico 2: Número de cores
    plt.subplot(2, 2, 2)
    sns.lineplot(data=df, x='Vertices', y='Cores', hue='Algoritmo',
                 style='Algoritmo', markers=True, dashes=False)
    plt.title('Número de Cores por Tamanho do Grafo')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Número de Cores')
    plt.grid(True)
    
    # Gráfico 3: Eficiência
    plt.subplot(2, 2, 3)
    sns.lineplot(data=df, x='Vertices', y='Cores/Vértice', hue='Algoritmo',
                 style='Algoritmo', markers=True, dashes=False)
    plt.title('Eficiência da Coloração')
    plt.xlabel('Número de Vértices')
    plt.ylabel('Cores por Vértice')
    plt.grid(True)
    
    # Gráfico 4: Tempo vs Qualidade
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
    """Análise de complexidade temporal"""
    plt.figure(figsize=(10, 6))
    
    for algoritmo in df['Algoritmo'].unique():
        subset = df[df['Algoritmo'] == algoritmo]
        x = subset['Vertices']
        y = subset['Tempo(ms)']
        
        # Filtra valores válidos para log
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

def plotar_distribuicao_cores():
    """Gráficos de distribuição de cores para um tamanho específico"""
    try:
        tamanhos_disponiveis = [50, 100, 200, 500, 1000]
        print("\nTamanhos disponíveis:", ", ".join(map(str, tamanhos_disponiveis)))
        tamanho = int(input("Digite o tamanho do grafo para visualização: "))
        
        if tamanho not in tamanhos_disponiveis:
            print(f"\nTamanho {tamanho} não está na lista de disponíveis!")
            return
            
        plt.figure(figsize=(14, 6))
        
        # DSATUR
        try:
            plt.subplot(1, 2, 1)
            dsatur = pd.read_csv(f'../resultados/dsatur_{tamanho}.csv', skipfooter=2, engine='python')
            plt.scatter(range(len(dsatur)), dsatur['Cor'], c=dsatur['Cor'], 
                        cmap='tab20', s=100, alpha=0.7)
            plt.title(f'DSATUR - Distribuição de Cores\n({tamanho} vértices)')
            plt.xlabel('Vértice')
            plt.ylabel('Cor')
            plt.colorbar()
        except FileNotFoundError:
            print(f"\nArquivo DSATUR para {tamanho} vértices não encontrado!")
            plt.close()
            return
        
        # RLF
        try:
            plt.subplot(1, 2, 2)
            rlf = pd.read_csv(f'../resultados/rlf_{tamanho}.csv', skipfooter=2, engine='python')
            plt.scatter(range(len(rlf)), rlf['Cor'], c=rlf['Cor'], 
                        cmap='tab20', s=100, alpha=0.7)
            plt.title(f'RLF - Distribuição de Cores\n({tamanho} vértices)')
            plt.xlabel('Vértice')
            plt.ylabel('Cor')
            plt.colorbar()
        except FileNotFoundError:
            print(f"\nArquivo RLF para {tamanho} vértices não encontrado!")
            plt.close()
            return
        
        plt.tight_layout()
        salvar_grafico(f'distribuicao_cores_{tamanho}.png')
        
    except ValueError:
        print("\nPor favor, digite um número válido.")

def main():
    print("\n=== Visualização de Resultados de Coloração de Grafos ===")
    
    criar_pasta_graficos()
    df = carregar_resultados()
    
    print("\nGerando gráficos comparativos...")
    plotar_comparacao(df)
    
    print("\nAnalisando complexidade temporal...")
    plotar_complexidade(df)
    
    print("\nVisualizando distribuição de cores...")
    plotar_distribuicao_cores()
    
    print("\nProcesso concluído! Todos os gráficos foram salvos em: ../graficos/")

if __name__ == "__main__":
    main()