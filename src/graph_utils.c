#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "graph_utils.h"

Graph* createGraph(int numVertices) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->numVertices = numVertices;
    graph->adjMatrix = (int**)malloc(numVertices * sizeof(int*));
    
    for (int i = 0; i < numVertices; i++) {
        graph->adjMatrix[i] = (int*)calloc(numVertices, sizeof(int));
    }
    
    return graph;
}

void freeGraph(Graph* graph) {
    for (int i = 0; i < graph->numVertices; i++) {
        free(graph->adjMatrix[i]);
    }
    free(graph->adjMatrix);
    free(graph);
}

void addEdge(Graph* graph, int v, int w) {
    if (v != w && graph->adjMatrix[v][w] == 0) {
        graph->adjMatrix[v][w] = 1;
        graph->adjMatrix[w][v] = 1;
    }
}

Graph* loadGraphFromFile(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Erro ao abrir arquivo");
        return NULL;
    }

    int numVertices, numEdges;
    fscanf(file, "%d %d", &numVertices, &numEdges);
    
    Graph* graph = createGraph(numVertices);
    
    for (int i = 0; i < numEdges; i++) {
        int v, w;
        fscanf(file, "%d %d", &v, &w);
        addEdge(graph, v, w);
    }
    
    fclose(file);
    return graph;
}

void saveColoringToFile(const char* filename, int* colors, int numVertices, double time, int numColors) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        perror("Erro ao abrir arquivo");
        return;
    }
    
    fprintf(fp, "Vertice,Cor\n");
    for (int i = 0; i < numVertices; i++) {
        fprintf(fp, "%d,%d\n", i, colors[i]);
    }
    
    fprintf(fp, "\nMetricas\n");
    fprintf(fp, "Tempo(ms),%f\n", time * 1000);
    fprintf(fp, "Cores,%d\n", numColors);
    fprintf(fp, "Vertices,%d\n", numVertices);
    
    fclose(fp);
}