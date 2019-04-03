#include <iostream>
#include <smpeg2/smpeg.h>

int main(int argc, char *args[])
{
    SMPEG_version v;
    SMPEG_VERSION(&v);
    std::cout << "SMPEG version: " << int(v.major) << "." << int(v.minor) << "." << int(v.patch) << std::endl;
    return 0;
}
