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

/*Sets Output and Input streams parameters to null or zero values*/
static void initStreamParameters(PaStreamParameters streamParameters, int device, bool in) {
    memset(&streamParameters, 0, sizeof(streamParameters));
    streamParameters.device = device;
    streamParameters.channelCount = 2;
    streamParameters.sampleFormat = paFloat32;
    streamParameters.hostApiSpecificStreamInfo = NULL;
    if (in == true) {
        streamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowInputLatency;
    }
    else {
        streamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowOutputLatency;
    }
}

static int paTestCallback(
    const void* inputBuffer, void* outputBuffer, unsigned long framesPerBuffer,
    const  PaStreamCallbackTimeInfo* timeInfo,PaStreamCallbackFlags statusFlag,
    void* userData
) {

}
int main(){
    /*Start PortAudio*/
    PaError err; 
    err = Pa_Initialize();
    checkError(err);

    /*Counts every audio deice on the machine. Each device information is displayed using their indexes */
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

    /*Selects an específic audio device and sets the parameters for the output and input
    streams to 0 */
    int device = 0;
    PaStreamParameters inStreamParameters;
    PaStreamParameters outStreamParameters;
    initStreamParameters(inStreamParameters, device, true);
    initStreamParameters(outStreamParameters, device, false);

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

    /*Ends PortAudio*/
    err = Pa_Terminate();
    checkError(err);
    return EXIT_SUCCESS;
}



