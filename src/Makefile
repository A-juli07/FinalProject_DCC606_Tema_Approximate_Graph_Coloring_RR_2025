CC = gcc
CFLAGS = -Wall -O3
TARGET = main.exe
SRC_FILES = main.c dsatur.c rlf.c graph_utils.c

all: $(TARGET)

$(TARGET): $(SRC_FILES)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	del $(TARGET)
	rmdir /s /q ..\resultados

.PHONY: all clean