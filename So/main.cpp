#include <stdlib.h>
#include <stdio.h>
#include <portaudio.h>
#include <cstring>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 512

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

static int paTestCallback(
    const void* inputBuffer, void* outputBuffer, unsigned long framesPerBuffer,
    const  PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlag,
    void* userData
) {

    float* in = (float*) inputBuffer;
    (void)outputBuffer;

    int dispSize = 100;
    printf("\r");

    float vol_r = 0;
    float vol_l = 0;
    
    for (unsigned long i = 0; i < framesPerBuffer * 2 ; i += 2 ) {
        vol_l = max(vol_l, std::abs(in[i]));
        vol_r = max(vol_r, std::abs(in[i+1]));
    }

    for (int i = 0; i < dispSize; i++) {
        float barProportion = i/(float)dispSize;
        if (barProportion <= vol_l && barProportion <= vol_r) {
            printf("█");
        }
        else if ( barProportion <= vol_l ) {
            printf("▀");
        }
        else if ( barProportion <= vol_r ) {
            printf("▄");
         }
        else {
            printf(" ");
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
        NULL
    );
    checkError(err);

    err = Pa_StartStream(stream);
    checkError(err);

    Pa_Sleep(10 * 1000);

    err = Pa_StopStream(stream);
    checkError(err);

    err = Pa_CloseStream(stream);
    checkError(err);

    /*Ends PortAudio*/
    err = Pa_Terminate();
    checkError(err);
    return EXIT_SUCCESS;
}



