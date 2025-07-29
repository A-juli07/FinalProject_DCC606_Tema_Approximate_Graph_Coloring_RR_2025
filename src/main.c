#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <time.h>
#include "graph_utils.h"

void run_algorithm(const char* algo_name, Graph* graph, FILE* results_file) {
    double time;
    int* colors;
    int numColors = 0;
    
    if (strcmp(algo_name, "DSATUR") == 0) {
        colors = dsaturColoring(graph, &time);
    } else {
        colors = rlfColoring(graph, &time);
    }
    
    // Calcula número de cores usadas
    for (int i = 0; i < graph->numVertices; i++) {
        if (colors[i] >= numColors) {
            numColors = colors[i] + 1;
        }
    }
    
    // Salva no arquivo de resultados
    fprintf(results_file, "%s,%d,%d,%.3f\n", 
            algo_name, graph->numVertices, numColors, time * 1000);
    
    free(colors);
}

int main() {
    // Cria pasta de resultados
    system("mkdir ..\\resultados 2> nul");
    
    // Abre arquivo único de resultados
    FILE* results_file = fopen("../resultados/resultados_completos.csv", "w");
    if (!results_file) {
        perror("Erro ao criar arquivo de resultados");
        return 1;
    }
    
    // Cabeçalho do CSV
    fprintf(results_file, "Algoritmo,Vertices,Cores,Tempo(ms)\n");
    
    DIR *dir;
    struct dirent *ent;
    
    if ((dir = opendir("../entradas")) != NULL) {
        while ((ent = readdir(dir)) != NULL) {
            if (strstr(ent->d_name, ".txt")) {
                char input_path[512];
                snprintf(input_path, sizeof(input_path), "../entradas/%s", ent->d_name);
                
                printf("Processando: %s\n", ent->d_name);
                
                Graph* graph = loadGraphFromFile(input_path);
                if (!graph) {
                    printf("Erro ao carregar grafo: %s\n", input_path);
                    continue;
                }
                
                // Executa ambos algoritmos
                run_algorithm("DSATUR", graph, results_file);
                run_algorithm("RLF", graph, results_file);
                
                freeGraph(graph);
            }
        }
        closedir(dir);
    } else {
        perror("Erro ao abrir diretorio de entradas");
        fclose(results_file);
        return 1;
    }
    
    fclose(results_file);
    printf("\nProcessamento concluido! Resultados em: ../resultados/resultados_completos.csv\n");
    system("start ..\\resultados");
    return 0;
}