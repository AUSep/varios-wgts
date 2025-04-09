#include "soundStrm.h"
#include <stdlib.h>
#include <stdio.h>
#include <portaudio.h>
#include <cstring>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 512

StreamHandler::StreamHandler(double sampleRate, int framesPerBuffer) {
    this->sampleRate = sampleRate;
    this->framesPerBuffer = framesPerBuffer;
    this->dispĺayDeviceInfo();
    this->device = Pa_GetDefaultOutputDevice();
}

/*Attribute setters*/
void StreamHandler::setDevice(PaDeviceIndex device){
    this->device = device;
}
void StreamHandler::setFamesPerBuffer(int framesPerBuffer){
    this->framesPerBuffer = framesPerBuffer;
}
void StreamHandler::setSampleRate(double sampleRate){
    this->sampleRate = sampleRate;
}

/*Error handler for Port Audio*/
void StreamHandler::checkErr(PaError err){
    if (err != paNoError) {
        printf("PortAudio error:%s\n", Pa_GetErrorText(err));
        exit(EXIT_FAILURE);
    }
}

/*Counts every audio device on the machine. Each device information is displayed using their indexes */
void StreamHandler::dispĺayDeviceInfo() {
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
/*Sets the parameters of a stream to initialize it*/
PaStreamParameters StreamHandler::initStreamParameters(int device, StreamType streamType){
    PaStreamParameters streamParameters;
    memset(&streamParameters, 0, sizeof(streamParameters));
    streamParameters.device = device;
    streamParameters.channelCount = 2;
    streamParameters.sampleFormat = paFloat32;
    streamParameters.hostApiSpecificStreamInfo = NULL;
    if ( streamType == INPUT) {
        streamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowInputLatency;
    }
    else if ( streamType == OUTPUT) {
        streamParameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowOutputLatency;
    }
    else {
        printf("Invalid stream type");
    }
    return streamParameters;
};

void StreamHandler::play(std::vector<float>& signal) {
    PaError err;
    PaStreamParameters parameters = this->initStreamParameters(this->device, OUTPUT);
    PaStream* stream = nullptr;
    err = Pa_OpenStream(
        &stream,
        NULL,
        &parameters,
        this->sampleRate,
        this->framesPerBuffer,
        paNoFlag,
        paOutCallback,
        reinterpret_cast<void*>(&signal)
    );

    err = Pa_StartStream(stream);
    this->checkErr(err);

    Pa_Sleep(static_cast<int>(signal.size() * 1000/this->sampleRate));

    err = Pa_StopStream(stream);
    this->checkErr(err);

    err = Pa_CloseStream(stream);
    this->checkErr(err);

}
int StreamHandler::paOutCallback(
    const void* inputBuffer, void* outputBuffer, unsigned long framesPerBuffer,
    const  PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlag,
    void* userData
) {
    AudioData* data = static_cast<AudioData*>(userData);
    float* out = static_cast<float*>(outputBuffer);

    if(data->signal == nullptr) {
        for (unsigned long i = 0; i < framesPerBuffer; i++){
            *out = 0.0f;
        }
    }
    return paContinue;

    size_t signalSize = data->signal->size();

    for (unsigned long i=0; i<framesPerBuffer;i++){
        if (data->position < signalSize){
            *out++=(*data->signal)[data->position++];
        }
        else {
            *out = 0.0f;
        }
    }
    if (data->position >= signalSize) {
        return paComplete;
    }
}