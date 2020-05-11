#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014,2020 Clayton Smith.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


from __future__ import division
from __future__ import print_function
import numpy
from gnuradio import gr

class chu_decode(gr.sync_block):
    """
    docstring for block chu_decode
    """

    start_of_data = numpy.array([1] * 533 + [0], dtype=numpy.int8).tostring() # Preamble
    samples_per_bit = 4800 // 300 # Sample rate / baud rate
    samples_in_message = 110 * samples_per_bit

    def __init__(self):
        gr.sync_block.__init__(self,
            name="chu_decode",
            in_sig=[numpy.int8],
            out_sig=None)

    def work(self, input_items, output_items):
        in0 = input_items[0]

        # Wait until we have enough data for a whole packet
        if len(in0) < len(self.start_of_data) + self.samples_in_message:
            return 0

        index = in0.tostring()[0:len(in0) - self.samples_in_message].find(self.start_of_data)
        if index != -1:
            # We found a preamble!
            startoffset = index + len(self.start_of_data)
            databits = ''
            for bit in range(110):
                offset = startoffset + self.samples_per_bit * bit
                bitsamples = in0[offset : offset + self.samples_per_bit]
                disc = 0
                for sample in bitsamples:
                    disc = disc - 1 + 2 * sample
                if disc >= 0:
                    databits += '1'
                else:
                    databits += '0'

            # Decode bytes
            tenbytes = []
            for x in range(0,110,11):
                byte = databits[x:x+11]
                if byte[0] == '0' and byte[9] == '1' and byte[10] == '1':
                    byteord = 0
                    for bit in byte[4:0:-1]:
                        byteord *= 2
                        if bit == '1':
                            byteord += 1
                    for bit in byte[8:4:-1]:
                        byteord *= 2
                        if bit == '1':
                            byteord += 1
                    tenbytes.append(byteord)
                else:
                    print('error', end=" ")
                    tenbytes.append(-1)

            # Decode data
            if tenbytes[0:5] == tenbytes[5:10] and tenbytes[0] >> 4 == 6:
                day = (tenbytes[0] & 0x0f) * 100 + (tenbytes[1] >> 4) * 10 + (tenbytes[1] & 0x0f)
                hour = (tenbytes[2] >> 4) * 10 + (tenbytes[2] & 0x0f)
                minute = (tenbytes[3] >> 4) * 10 + (tenbytes[3] & 0x0f)
                second = (tenbytes[4] >> 4) * 10 + (tenbytes[4] & 0x0f)
                print("A frame:")
                print(" Day of year: " + str(day))
                print(" Current Time: " + str(hour) + ":" + str(minute) + ":" + str(second) + " UTC")
                print()
            elif tenbytes[0:5] == [x ^ 0xff for x in tenbytes[5:10]]:
                dut = (tenbytes[0] & 0x0f) / 10.0
                if (tenbytes[0] & 0x10):
                    dut = -dut
                lsw = 0
                if (tenbytes[0] & 0x20):
                    lsw = 1
                if (tenbytes[0] & 0x40):
                    lsw = -1
                year = (tenbytes[1] >> 4) * 1000 + (tenbytes[1] & 0x0f) * 100 + (tenbytes[2] >> 4) * 10 + (tenbytes[2] & 0x0f)
                tt = (tenbytes[3] >> 4) * 10 + (tenbytes[3] & 0x0f)
                aa = (tenbytes[4] >> 4) * 10 + (tenbytes[4] & 0x0f)
                print("B frame:")
                print(" Year: " + str(year))
                print(" Leap second warning: " + str(lsw))
                print(" Difference between UTC and UT1: " + str(dut) + " seconds")
                print(" Difference between TAI and UTC: " + str(tt) + " seconds")
                print(" Daylight saving time pattern: " + str(aa))
                print()
            else:
                print("Decoding error.")
                print()

            return index + len(self.start_of_data) + self.samples_in_message

        # We didn't find a preamble
        return len(in0) - len(self.start_of_data) - self.samples_in_message
