#include <stdlib.h>
#include <stdio.h>
#include <png.h>
#include <mpi.h>
#include <iostream>

using namespace std;

#define RANGE 5
#define LINEAR_FILTER
#define NEGATE

void read_png_file(char *filename, png_bytep* &row_pointers, int &height, int &width, png_bytep* &copy);
void write_png_file(char *filename, png_bytep* row_pointers, int height, int width);

void worker();
void master(png_bytep* input, int height, int width, png_bytep* output);

int main(int argc, char **argv);
