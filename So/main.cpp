#include <stdlib.h>
#include <stdio.h>
#include <portaudio.h>
#include <cstring>
#include <fftw3.h>
#include <math.h>

#define SAMPLE_RATE 44100.0
#define FRAMES_PER_BUFFER 512
#define N_CHANNELS 2
#define SPECT_LOW_BOUND 20
#define SPECT_HI_BOUND 22000

typedef struct 
{
    double* in;
    double* out;
    fftw_plan p;
    int startIndex;
    int spectSize;
}streamCallbackData;

static streamCallbackData* spectData;

/*Error handler por Port Audio*/
static void checkError(PaError err){
    if (err != paNoError) {
        printf("PortAudio error:%s\n", Pa_GetErrorText(err));
        exit(EXIT_FAILURE);
    }
}

/*Counts every audio deice on the machine. Each device information is displayed using their indexes */
static void displayDeviceInfo() {
    int count = Pa_GetDeviceCount();
    printf("%d audio devices found:\n", count);
    const PaDeviceInfo* devInfo;
    for (int i = 0; i < count; i++) {
        devInfo = Pa_GetDeviceInfo(i);
        printf("Device: %d\n", i);
        printf("    Name: %s\n", devInfo->name);
        printf("    Inputs: %d\n", devInfo->maxInputChannels);
        printf("    Outputs: %d\n", devInfo->maxOutputChannels);
    }
}

static inline float max(float a, float b) {
    return a > b ? a : b;
}

static inline float min(float a, float b) {
    return a < b ? a : b;
}

static int paTestCallback(
    const void* inputBuffer, void* outputBuffer, unsigned long framesPerBuffer,
    const  PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlag,
    void* userData
) {

    streamCallbackData* callbackData = (streamCallbackData*)userData;
    float* in = (float*) inputBuffer;
    (void)outputBuffer;

    int dispSize = 100;
    printf("\r");

    for (unsigned long i = 0; i < framesPerBuffer; i++) {
        callbackData->in[i] = in[i * N_CHANNELS];
    }

    fftw_execute(callbackData->p);
    for (int i = 0; i<dispSize; i++ ) {
        double proportion = i/dispSize;
        double freq = callbackData->out[(int)(callbackData->startIndex 
            + proportion * callbackData->spectSize)];

        if (freq <0.125) {
            printf("▁");
        }
        else if (freq < 0.25){
            printf("▂");
        }
        else if (freq < 0.375){
            printf("▃");
        }
        else if (freq < 0.5){
            printf("▄");
        }
        else if (freq < 0.625){
            printf("▅");
        }
        else if (freq < 0.75){
            printf("▆");
        }
        else if (freq < 0.875){
            printf("▇");
        }
        else {
            printf("█");
        }
    }
    fflush(stdout);

    return 0;
}
int main(){
    /*Start PortAudio*/
    PaError err; 
    err = Pa_Initialize();
    checkError(err);

    spectData = (streamCallbackData*)malloc(sizeof(streamCallbackData));
    spectData->in = (double*)malloc(sizeof(double*) * FRAMES_PER_BUFFER);
    spectData->out = (double*)malloc(sizeof(double*) * FRAMES_PER_BUFFER);

    if (spectData->in == NULL || spectData->out == NULL) {
        printf("Could not allocate spectrum data\n");
        exit(EXIT_FAILURE);
    }
    spectData->p = fftw_plan_r2r_1d(FRAMES_PER_BUFFER,
        spectData->in,
        spectData->out,
        FFTW_R2HC,
        FFTW_ESTIMATE);

    double sampRatio = FRAMES_PER_BUFFER/SAMPLE_RATE;
    spectData->startIndex = std::ceil(sampRatio * SPECT_LOW_BOUND);
    spectData->startIndex = min(
        std::ceil(sampRatio * SPECT_HI_BOUND),
        FRAMES_PER_BUFFER/2.0) - spectData->startIndex;

    displayDeviceInfo();

    /*Selects an específic audio device and sets the parameters for the output and input
    streams to 0*/
    int device = 2;
    PaStreamParameters inStreamParameters;
    PaStreamParameters outStreamParameters;

    memset(&inStreamParameters, 0, sizeof(inStreamParameters));
    inStreamParameters.device = device;
    inStreamParameters.channelCount = 2;
    inStreamParameters.sampleFormat = paFloat32;
    inStreamParameters.hostApiSpecificStreamInfo = NULL;
    inStreamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowInputLatency;
    
    memset(&outStreamParameters, 0, sizeof(outStreamParameters));
    outStreamParameters.device = device;
    outStreamParameters.channelCount = 2;
    outStreamParameters.sampleFormat = paFloat32;
    outStreamParameters.hostApiSpecificStreamInfo = NULL;
    outStreamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowOutputLatency;

    /*Initailize and open a stream*/

    PaStream* stream;
    err = Pa_OpenStream(
        &stream,
        &inStreamParameters,
        &outStreamParameters,
        SAMPLE_RATE,
        FRAMES_PER_BUFFER,
        paNoFlag,
        paTestCallback,
        spectData
    );
    checkError(err);

    err = Pa_StartStream(stream);
    checkError(err);

    Pa_Sleep(10 * 1000);

    err = Pa_StopStream(stream);
    checkError(err);

    err = Pa_CloseStream(stream);
    checkError(err);

    fftw_destroy_plan(spectData->p);
    fftw_free(spectData->in);
    fftw_free(spectData->out);
    free(spectData);

    /*Ends PortAudio*/
    err = Pa_Terminate();
    checkError(err);
    return EXIT_SUCCESS;
}



