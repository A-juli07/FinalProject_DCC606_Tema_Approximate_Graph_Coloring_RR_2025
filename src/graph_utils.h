#ifndef GRAPH_UTILS_H
#define GRAPH_UTILS_H

typedef struct {
    int numVertices;
    int** adjMatrix;
} Graph;

Graph* createGraph(int numVertices);
void freeGraph(Graph* graph);
void addEdge(Graph* graph, int v, int w);
Graph* loadGraphFromFile(const char* filename);
void saveColoringToFile(const char* filename, int* colors, int numVertices, double time, int numColors);

int* dsaturColoring(Graph* graph, double* timeSpent);
int* rlfColoring(Graph* graph, double* timeSpent);

#endif
