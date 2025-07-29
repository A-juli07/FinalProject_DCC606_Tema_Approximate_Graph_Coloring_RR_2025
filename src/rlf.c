#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <string.h>
#include "graph_utils.h"

int* rlfColoring(Graph* graph, double* timeSpent) {
    clock_t start = clock();
    int n = graph->numVertices;
    int* colors = (int*)malloc(n * sizeof(int));
    memset(colors, -1, n * sizeof(int));
    
    bool* colored = (bool*)calloc(n, sizeof(bool));
    int color = 0;
    
    while (true) {
        // Encontrar vértice não colorido com maior grau entre os não coloridos
        int maxDeg = -1, vertex = -1;
        for (int i = 0; i < n; i++) {
            if (!colored[i]) {
                int deg = 0;
                for (int j = 0; j < n; j++) {
                    if (!colored[j] && graph->adjMatrix[i][j]) {
                        deg++;
                    }
                }
                if (deg > maxDeg) {
                    maxDeg = deg;
                    vertex = i;
                }
            }
        }
        
        if (vertex == -1) break; // Todos coloridos
        
        // Colorir o vértice selecionado
        colors[vertex] = color;
        colored[vertex] = true;
        
        // Tentar colorir outros vértices não adjacentes com a mesma cor
        for (int i = 0; i < n; i++) {
            if (!colored[i] && !graph->adjMatrix[vertex][i]) {
                bool canColor = true;
                for (int j = 0; j < n; j++) {
                    if (colored[j] && colors[j] == color && graph->adjMatrix[i][j]) {
                        canColor = false;
                        break;
                    }
                }
                if (canColor) {
                    colors[i] = color;
                    colored[i] = true;
                }
            }
        }
        
        color++;
    }
    
    *timeSpent = (double)(clock() - start) / CLOCKS_PER_SEC;
    free(colored);
    return colors;
}