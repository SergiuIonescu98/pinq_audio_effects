#include <stdio.h>
#include <math.h>
#include "c_effects.h"
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <time.h>

void printSignal(int* mysignal)
{
    for (int i=0; i<BUFFER_SIZE; i++)
        printf("%i ",mysignal[i]);
    printf("\n");
}

////// point to point processing //////////

void infiniteClip(short* mysignal)
{
    for (int i = 1; i < BUFFER_SIZE; i++)
    {
        if (mysignal[i] >= 0)
            mysignal[i] = pow(2, 15) - 1;
        else
            mysignal[i] = 0;
    }
}

void halfwaveRectification(short* mysignal)
{
    for (int i = 1; i < BUFFER_SIZE; i++)
        if (mysignal[i] < 0 )
            mysignal[i] = 0;
}

void fullwaveRectification(short* mysignal)
{
    for (int i=1; i < BUFFER_SIZE; i++)
    {
        if (mysignal[i] < 0)
            mysignal[i] = (-1)*mysignal[i];
    }
}


///////////////// delay utils //////////

int seconds_to_samples(int fs, float timeS, char* unit)
{
    if (strcmp(unit, "ms") == 0)
        timeS = timeS/1000;
    
    int timeSamples = (int)(timeS * fs);

    return timeSamples;
}


int tempo_to_samples(int fs, float bpm, float noteDiv)
{
    float bps = bpm / 60;
    printf("This is the bps %f \n", bps);

    float secPerBeat = 1/bps;

    float timeSec = noteDiv * secPerBeat;
    printf("This is the timeSec %f \n", timeSec);

    int timeSamples = (int)(timeSec * fs);
    
    return timeSamples;
}

void feedforward_echo(int fs, float bpm, float noteDiv, float b, short* x, short* y)
{
    int d = tempo_to_samples(fs, bpm, noteDiv);
    printf("## THIS IS THE TEMPO %i \n", d);
    for (int i=1 ; i < BUFFER_SIZE; i++)
        {
            if (i < d + 1)
                y[i] = x[i];
            else
                y[i] = x[i] + b * x[i-d];
        }
}

void feedback_echo(int fs, float bpm, float noteDiv, float a, short* x, short* y)
{
    int d = tempo_to_samples(fs, bpm, noteDiv);
    printf("## THIS IS THE TEMPO %i \n", d);
    for (int i=1; i< BUFFER_SIZE; i++)
        {
            if (i < d + 1)
                y[i] = x[i];
            else
                y[i] = x[i] + (-1)*a * x[i-d];
        }
}


void firdelayBuffer(int* x, int fs, float bpm, int noteDiv, float fbGain)
{
    printf("## FIRDELAYBUFFER TO BE DONE##\n");
}

void circularechoBuffer(int x_sample, int* buffer, int delay, int index, float fbGain)
{
    printf("## CIRCULARBUFFER TO BE DONE##\n");
}

// vibrato
// chorus

// convolution

float* convolve(double* h, int* x, int lenH, int lenX, int* lenY)
{
    int nconv = lenH+lenX-1;
    (*lenY) = nconv;
    int i,j,h_start,x_start,x_end, index;

    float *y = (float*) calloc(nconv, sizeof(float));
    printf("## NUMBER OF CONV %i ##\n", nconv);
    for (i=0; i<nconv; i++)
    {
        x_start = MAX(0,i-lenH+1);
        x_end   = MIN(i+1,lenX);
        h_start = MIN(i,lenH-1);
        index = h_start;

        for(j=x_start; j<x_end; j++)
        {           
            // y[i] += h[index] * x[j];
            // if (x_start == 0)
            //     index = index - 1;
            // else
            //     index = h_start-(j%x_start)-1;

            y[i] += h[h_start--]*x[j]; 

        }

        if (i%10000 == 0)
             printf("### STEP  %i\n", i );
        //break;
    }
    return y;
}


void read_reverb(double* reverb_array){
    FILE *myfile;
    double myvariable;

    myfile=fopen("reverb.txt", "r");

    for(int i = 0; i < RVB_SHORT; i++)
    {
        fscanf(myfile,"%lf",&myvariable);
        reverb_array[i] = myvariable;
    }

    fclose(myfile);
}


float max_value(float *y, int dim)
{
    float max = 0;
    for ( int i=0 ; i< dim ; i++)
        if (max < y[i])
            max = y[i];
    printf("## THIS IS THE MAX VALUE %f## \n", max);
    return max;
}   

void normalise_16b(float* y, int dim)
{
    float max_sample = max_value(y, dim);
    for ( int i = 0 ; i < dim ; i++)
        y[i] = y[i] * (pow(2, 15) - 1 ) / max_sample;
}



int main(int argc, const char **argv)
{
    
    int givenKey;
    effects_enum_t effects;
    int fs = 44100;

    if(argc < 3)
    {
        printf("Expected argument: shared memory id !\n");
        printf("Expected effects argument \n");
        return 0;
    }
    sscanf(argv[1], "%d", &givenKey);
    sscanf(argv[2], "%d", &effects);

    short* shared_memory;
    short buffer_memory[BUFFER_SIZE];
    double reverb_array[RVB_SIZE];

    if ((shared_memory = (short*) (shmat(givenKey, NULL, 0))) == (void *) -1)
    {
        printf("Error attaching shared memory id");
        return 0;
    }


    printf("The is the flag byte %i \n", shared_memory[0]);

    // int fs, int bpm, int noteDiv, float b, int* x, int* y

    double time_spent = 0.0;
    clock_t begin = clock();

    switch(effects)
    {
        case INF:
            printf("## Infinite Cliping ## \n");
            infiniteClip(shared_memory);
            break;
        case HALF:
            printf("## Half Wave Rectification ## \n");
            halfwaveRectification(shared_memory);
            break;
        case FULL:
            printf("## Full Wave Rectification ## \n");
            fullwaveRectification(shared_memory);
            break;

        case ECHO_FWD:
            printf("## Echo FWD ## \n");
            feedforward_echo(fs, 105, 0.5, 0.45, shared_memory, buffer_memory);        
            for (int i=1; i<BUFFER_SIZE; i++)
                shared_memory[i] = buffer_memory[i];
            break;
        case ECHO_FBK:
            printf("## ECHO FBK ##\n");
            feedback_echo(fs, 105, 0.5, -0.75, shared_memory, buffer_memory);
            for ( int i=1; i<BUFFER_SIZE; i++)
                shared_memory[i] = buffer_memory[i];
            break;
        
        case REVERB:
            printf("## ECHO REVERB ##\n");
            read_reverb(reverb_array);
            printf("## REVERB ARRAY READ ##\n");
            int lenY;
            float *y = convolve(reverb_array, shared_memory, RVB_SHORT, BUFFER_SHORT, &lenY);
            
            normalise_16b(y, lenY);

            printf("### len of conv %i\n", lenY);
            for(int i=0;i<lenY;i++) {
                //printf("%0.f ",y[i]);
                shared_memory[i] = y[i];
            }

            puts("");
            free(y);
            break;
    }

    clock_t end = clock();
    time_spent += (double)(end - begin) / CLOCKS_PER_SEC;
    printf("The elapsed time is %f ms\n", time_spent * 1000);


    shared_memory[0] = 1;
    shmdt(shared_memory);

    return 0;
}