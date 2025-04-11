#include <portaudio.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <math.h>

#define SAMPLE_RATE 44100.00
#define FRAMES_PER_BUFFER 512
#define SECONDS 2
#define PERIOD 200
#define LOOPS 3

#ifndef PI
#define PI 3.14159265
#endif

struct AudioData{
    float sine[PERIOD];
    int phase;
    unsigned long generatedFrames;
    volatile int completedCallback;
    volatile int callbackAfterCompleted;

};

static void checkErr(PaError err){
    if (err != paNoError){
        printf("PortAudio error: %s", Pa_GetErrorText(err));
        exit(EXIT_FAILURE);
    }
}

int main(){
    PaError err;
    PaDeviceIndex device;
    PaStreamParameters outStreamParameters;
    PaStream* stream;
    AudioData data;
    int i , j;
    
    for(i = 0; i<PERIOD; i++){
        data.sine[i]=(float) sin(((double)i/(double)PERIOD)*PI*2.);
    }

    err = Pa_Initialize();
    checkErr(err);

    device = Pa_GetDefaultOutputDevice();
    
    memset(&outStreamParameters, 0, sizeof(outStreamParameters));
    outStreamParameters.device = device;
    outStreamParameters.channelCount = 2;
    outStreamParameters.sampleFormat = paFloat32;
    outStreamParameters.hostApiSpecificStreamInfo = NULL;
    outStreamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowOutputLatency;

    err = Pa_OpenStream(&stream,
                        NULL,
                        &outStreamParameters,
                        SAMPLE_RATE,
                        FRAMES_PER_BUFFER,
                        paNoFlag,
                        NULL,
                        NULL);
    checkErr(err);

    for (i = 0; i<=LOOPS; i++){
        data.phase=0;
        data.generatedFrames=0;
        data.completedCallback=0;
        data.callbackAfterCompleted=0;
        err = Pa_StartStream(stream);
        checkErr(err);
        do{
            Pa_Sleep(100);
        }
        while (!data.callbackAfterCompleted);
    }
    
    err = Pa_StartStream(stream);
    checkErr(err);

    Pa_Sleep(2000);

    err = Pa_StopStream(stream);
    checkErr(err);

    err = Pa_CloseStream(stream);
    checkErr(err);
    return EXIT_SUCCESS;
}