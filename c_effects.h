#define BUFFER_SIZE 312362
#define RVB_SIZE 192000

#define RVB_SHORT 48000
#define BUFFER_SHORT 88200 

/// print signal

void printSignal(int* mysignal);


/// point to point processing ////

void infiniteClip(short* mysignal);
void halfwaveRectification(short* mysignal);
void fullwaveRectification(short* mysignal);


/// delay utils ////

int seconds_to_samples(int fs, float timeS, char* unit);
int tempo_to_samples(int fs, float bpm, float noteDiv);

/// delay functions //

void feedforward_echo(int fs, float bpm, float noteDiv, float b, short* x, short* y);
void feedback_echo(int fs, float bpm, float noteDiv, float a, short* x, short* y);

// delay buffer functions //
void firdelayBuffer(int* x, int fs, float bpm, int noteDiv, float fbGain);
void circularechoBuffer(int x_sample, int* buffer, int delay, int index, float fbGain);

// vibrato
// chorus


typedef enum {
INF,
HALF,
FULL,

ECHO_FWD,
ECHO_FBK,

REVERB,
TEST
} effects_enum_t;



// helper functions to get the min and max of two numbers
#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))
#define MAX(X, Y) (((X) < (Y)) ? (Y) : (X))

void read_reverb(double* reverb_array);
float* convolve(double* h, int* x, int lenH, int lenX, int* lenY);
