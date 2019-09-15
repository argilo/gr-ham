gr-ham
======

Author: Clayton Smith  
Email: <argilo@gmail.com>

This project includes several blocks that may be of use to amateur radio
operators. Currently it has a varicode encoder and decoder (useful for PSK31),
a decoder for the CHU time signal, and a partial decoder for D-STAR.

Build instructions:

    mkdir build
    cd build
    cmake ../
    make
    sudo make install

If your GNU Radio is installed in `/usr` (rather than `/usr/local`), then
replace the third line above with:

    cmake -DCMAKE_INSTALL_PREFIX=/usr ../
