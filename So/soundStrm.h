#ifndef SOUNDSTRM_H
#define SOUNDSTRM_H
#include <portaudio.h>
#include <vector>

enum StreamType {
    INPUT,
    OUTPUT
};

class StreamHandler {
    public:
        StreamHandler(double sampleRate, int framesPerBuffer);
        void setDevice(PaDeviceIndex device);
        void setFamesPerBuffer(int framesPerBuffer);
        void setSampleRate(double sampleRate);
        static void dispĺayDeviceInfo();
        void play(std::vector<float>& signal);
    private:
        static void checkErr(PaError err);
        PaStreamParameters initStreamParameters(int device, StreamType streamType);
        double sampleRate;
        int framesPerBuffer;
        PaStream* Stream;
        PaDeviceIndex device;
        static int paOutCallback(
            const void* inputBuffer, void* outputBuffer, unsigned long framesPerBuffer,
            const  PaStreamCallbackTimeInfo* timeInfo, PaStreamCallbackFlags statusFlag,
            void* userData
        );
};

#endif //SOUNDSTRM_H