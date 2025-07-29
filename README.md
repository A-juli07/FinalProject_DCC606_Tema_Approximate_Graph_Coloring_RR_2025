# Coloração Aproximada de Grafos

### Professor: Hebert Rocha  
### Análise de Algoritmos - DCC606
### Universidade Federal de Roraima - Departamento de Ciência da Computação  

## Objetivo

Este projeto foi desenvolvido como parte da disciplina **DCC606 - Análise de Algoritmos**, com o objetivo de implementar e analisar **algoritmos aproximados para o problema da coloração de grafos**.

## Como Rodar

1. **Clone e Rode os algoritmos**

   Abra um terminal e execute:

   ```bash
   git clone https://github.com/A-juli07/FinalProject_DCC606_Tema_Approximate_Graph_Coloring_RR_2025.git
   ```

2. **Navegue até o diretorio do projeto**

   ```bash
   cd FinalProject_DCC606_Tema_Approximate_Graph_Coloring_RR_2025
   ```
   
3. **Acesse a pasta entradas e rode o Gerador_entradas**

   ```bash
   cd entradas
   python gerador_entradas.py          # Gera entradas entre 50 e 2000
   ```

4. **Acessar a pasta src e rodar o Makefile**

   ```bash
   cd src
   make     
   ./main.exe                         # Executavel do codigo main.c       
   ```

  Roda os algotimos RLF e DSatur com os benchmarks gerados no passo anterior, atualiza ou cria a pasta resultados com csv detalhado de cada algoritmo com o benchmark mas tambem apresenta os resultados completos em csv. 
     
5. **Gerar Gráficos com Python**

   Acesse a pasta de visualização:

   ```bash
   cd visualizacao
   pip install -r requirements.txt     # Instala requerimentos para a codigo
   python visualizacao.py          # Cria os graficos de comparaçaõ
   ```

   As figuras geradas aparecerão em `graficos/`:

   * `comparacao_algoritmos.png`
   * `complexidade_temporal.png`

O projeto inclui:
- Análise e descrição do artigo **"Approximate Graph Coloring by Semidefinite Programming"** (Karger, Motwani, Sudan - 1998). FEITO
- Implementação de **duas soluções aproximadas** para coloração de grafos. EM DESENVOLVIMENTO
- Visualização do grafo com as cores aplicadas. EM DESENVOLVIMENTO
- Análise experimental com benchmarks de grafos. EM DESENVOLVIMENTO
- Discussão dos resultados obtidos. A FAZER
