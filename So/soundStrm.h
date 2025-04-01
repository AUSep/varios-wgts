#ifndef SOUNDSTRM_H
#define SOUNDSTRM_H
#include <portaudio.h>

enum StreamType {
    INPUT,
    OUTPUT
};

class Streamer {
    public:
        Streamer(double sampleRate, int framesPerBuffer);
        double sampleRate;
        int framesPerBuffer;
        static void dispĺayDeviceInfo();
        void initStreamParameters(PaStreamParameters streamParameters, int device, StreamType streamType);
    private:
        static void checkErr(PaError err);

};

#endif //SOUNDSTRM_H