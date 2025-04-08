#ifndef SOUNDSTRM_H
#define SOUNDSTRM_H
#include <portaudio.h>

enum StreamType {
    INPUT,
    OUTPUT
};

class StreamHandler {
    public:
        StreamHandler(double sampleRate, int framesPerBuffer);
        static void dispĺayDeviceInfo();
        void startStream(StreamType StreamType);
        void setDevice(PaDeviceIndex device);
    private:
        static void checkErr(PaError err);
        void initStreamParameters(PaStreamParameters streamParameters, int device, StreamType streamType);
        double sampleRate;
        int framesPerBuffer;
        PaStream* Stream;
        PaDeviceIndex device;
};

#endif //SOUNDSTRM_H