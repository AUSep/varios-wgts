#include <portaudio.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <math.h>

#define SAMPLE_RATE 44100.00
#define FRAMES_PER_BUFFER 512
#define SECONDS 1
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
        printf("PortAudio error: %s\n", Pa_GetErrorText(err));
        exit(EXIT_FAILURE);
    }
}
static void dispĺayDeviceInfo() {
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

static int TestCallback( const void *input, void *output,
    unsigned long frameCount,
    const PaStreamCallbackTimeInfo* timeInfo,
    PaStreamCallbackFlags statusFlags,
    void *userData ){
        AudioData *data = (AudioData*) userData;
        float *out = (float*) output;
        unsigned long i;
        float x;

        (void)input;
        (void)timeInfo;
        (void)statusFlags;

        for(i = 0; i<frameCount; i++){
            x=data->sine[data->phase++];
            if (data->phase>=PERIOD){
                data->phase-= PERIOD;
            }
            *out++ = x;
            *out++ = x;
        }
        data->generatedFrames+=frameCount;
        if(data->generatedFrames>=(SECONDS*SAMPLE_RATE)){
            data->completedCallback = 1;
            return paComplete;
        }
        else{
            return paContinue;
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

    dispĺayDeviceInfo();

    device = 0;
    
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
                        paClipOff,
                        TestCallback,
                        &data);
    checkErr(err);

    printf("Testing Loops\n");

    for (i = 0; i<=LOOPS; i++){
        data.phase=0;
        data.generatedFrames=0;
        data.completedCallback=0;
        err = Pa_StartStream(stream);
        checkErr(err);
        do{
            Pa_Sleep(100);
        }
        while (!data.completedCallback);

        err = Pa_StopStream(stream);
        checkErr(err);
    }

    err = Pa_CloseStream(stream);
    checkErr(err);

    err = Pa_Terminate();
    checkErr(err);
    return EXIT_SUCCESS;
}