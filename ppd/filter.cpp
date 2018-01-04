#include "filter.hpp"

int id;
int processes;
int stop_working[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

void worker() {
    int height, width;
    png_bytep* image;
    png_bytep* output;
    MPI_Status status;

    MPI_Bcast(&height, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&width, 1, MPI_INT, 0, MPI_COMM_WORLD);

    image = (png_bytep*)malloc(sizeof(png_bytep) * height);
    for (int i = 0; i < height; ++i) {
        image[i] = (png_bytep)malloc(sizeof(png_bytep) * 4 * width);
    }

    output = (png_bytep*)malloc(sizeof(png_bytep) * height);
    for (int i = 0; i < height; ++i) {
        output[i] = (png_bytep)malloc(sizeof(png_bytep) * 4 * width);
        for (int j = 0; j < width * 4; ++j) {
            output[i][j] = 0;
        }
    }
    int begin, end;
    MPI_Recv(&begin, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
    MPI_Recv(&end, 1, MPI_INT, 0, 2, MPI_COMM_WORLD, &status);

    for (int i = 0; i < height; ++i) {
        MPI_Bcast(image[i], width, MPI_INT, 0, MPI_COMM_WORLD);
    }

    for (int px = begin; px < end; ++px) {
        int i = px / width;
        int j = px % width;
        //cout << i << " " << j << "\n" << flush;
        int avg[4] = {0, 0, 0, 0};
        int count = 0;
        for (int k = i - RANGE; k <= i + RANGE; ++k) {
            for (int l = j - RANGE; l <= j + RANGE; ++l) {
                if (k < 0 || l < 0 || k >= height || l >= width) {
                    continue;
                }
                ++count;
                png_bytep px = &image[k][l * 4];
                for (int p = 0; p < 4; ++p) {
                    avg[p] += px[p];
                }
            }
        }
        png_bytep pixel = &output[i][j * 4];
        for (int k = 0; k < 4; ++k) {
            if (!stop_working[id]) {
                pixel[k] = avg[k] / count;
            } else {
                pixel[k] = image[i][j * 4 + k];
            }
        }
    }
    cout << "Worker ready\n" << flush;
    for (int i = 0; i < height; ++i) {
        MPI_Send(output[i], width, MPI_INT, 0, 3, MPI_COMM_WORLD);
        free(output[i]);
        free(image[i]);
    }
    free(image);
    free(output);
}

void master(png_bytep* input, int height, int width, png_bytep* output) {
    MPI_Status status;

    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width * 4; ++j) {
            output[i][j] = 0;
        }
    }   

    if (processes) {
        MPI_Bcast(&height, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&width, 1, MPI_INT, 0, MPI_COMM_WORLD);
        for (int i = 1; i < processes; ++i) {
            int begin = height * width * i / processes;
            int end = height * width * (i + 1) / processes;
            MPI_Send(&begin, 1, MPI_INT, i, 1, MPI_COMM_WORLD);
            MPI_Send(&end, 1, MPI_INT, i, 2, MPI_COMM_WORLD);
        }
        for (int i = 0; i < height; ++i) {
            MPI_Bcast(input[i], width, MPI_INT, 0, MPI_COMM_WORLD);
        }
    }
    for (int px = 0; px < width * height / processes; ++px) {
        int i = px / width;
        int j = px % width;
        int avg[4] = {0, 0, 0, 0};
        int count = 0;
        for (int k = i - RANGE; k <= i + RANGE; ++k) {
            for (int l = j - RANGE; l <= j + RANGE; ++l) {
                if (k < 0 || l < 0 || k >= height || l >= width) {
                    continue;
                }
                ++count;
                png_bytep px = &input[k][l * 4];
                for (int p = 0; p < 4; ++p) {
                    avg[p] += px[p];
                }
            }
        }
        png_bytep pixel = &output[i][j * 4];
        for (int k = 0; k < 4; ++k) {
            pixel[k]  = avg[k] / count;
        }
    }
    cout << "Master finished\n" << flush; 
    if (processes) {
        png_bytep row = (png_bytep)malloc(sizeof(png_byte) * 4 * width);
        for (int source = 1; source < processes; ++source) {
            for (int i = 0; i < height; ++i) {
                //cout << i << "\n" << flush;
                MPI_Recv(row, width, MPI_INT, source, 3, MPI_COMM_WORLD, &status);
                for (int j = 0; j < width * 4; ++j) {
                    output[i][j] += row[j];
                }
            }
        }
        free(row);
    }
}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);

    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &processes);

    if (!id) {
        png_bytep* png_data;
        png_bytep* processed;
        int height, width;
        read_png_file(argv[1], png_data, height, width, processed);

        master(png_data, height, width, processed);
        write_png_file(argv[2], processed, height, width);
    } else {
        //if (!stop_working[id]) {
        worker();
        //}
    }

    MPI_Finalize();
    return 0;
}