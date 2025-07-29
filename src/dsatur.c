#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <string.h>
#include "graph_utils.h"

typedef struct {
    int vertex;
    int degree;
    int saturation;
} VertexInfo;

int compareVertex(const void* a, const void* b) {
    VertexInfo* va = (VertexInfo*)a;
    VertexInfo* vb = (VertexInfo*)b;
    if (va->saturation != vb->saturation) {
        return vb->saturation - va->saturation;
    }
    return vb->degree - va->degree;
}

int* dsaturColoring(Graph* graph, double* timeSpent) {
    clock_t start = clock();
    int n = graph->numVertices;
    int* colors = (int*)malloc(n * sizeof(int));
    memset(colors, -1, n * sizeof(int));
    
    int* degrees = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        degrees[i] = 0;
        for (int j = 0; j < n; j++) {
            degrees[i] += graph->adjMatrix[i][j];
        }
    }
    
    VertexInfo* vertices = (VertexInfo*)malloc(n * sizeof(VertexInfo));
    for (int i = 0; i < n; i++) {
        vertices[i].vertex = i;
        vertices[i].degree = degrees[i];
        vertices[i].saturation = 0;
    }
    
    bool* colored = (bool*)calloc(n, sizeof(bool));
    
    for (int count = 0; count < n; count++) {
        // Ordenar vértices por saturação e grau
        qsort(vertices, n, sizeof(VertexInfo), compareVertex);
        
        // Encontrar o primeiro vértice não colorido
        int current = -1;
        for (int i = 0; i < n; i++) {
            if (!colored[vertices[i].vertex]) {
                current = vertices[i].vertex;
                break;
            }
        }
        if (current == -1) break;
        
        // Encontrar a menor cor disponível
        bool* available = (bool*)calloc(n, sizeof(bool));
        for (int i = 0; i < n; i++) {
            if (graph->adjMatrix[current][i] && colors[i] != -1) {
                available[colors[i]] = true;
            }
        }
        
        int cr;
        for (cr = 0; cr < n; cr++) {
            if (!available[cr]) break;
        }
        
        colors[current] = cr;
        colored[current] = true;
        
        // Atualizar saturação dos vizinhos
        for (int i = 0; i < n; i++) {
            if (graph->adjMatrix[current][i] && !colored[i]) {
                vertices[i].saturation++;
            }
        }
        
        free(available);
    }
    
    *timeSpent = (double)(clock() - start) / CLOCKS_PER_SEC;
    
    free(degrees);
    free(vertices);
    free(colored);
    return colors;
}
