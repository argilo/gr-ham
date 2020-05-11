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


from __future__ import print_function
import numpy
from gnuradio import gr


class dstar_rx(gr.sync_block):
    """
    docstring for block dstar_rx
    """

    VOICE_FRAME_LEN = 72
    DATA_FRAME_LEN = 24
    TOTAL_FRAME_LEN = 96
    INPUT_RATE = 4800
    OUTPUT_RATE = 8000

    bit_syn = numpy.array([1, 0]*16, dtype=numpy.int8).tostring()
    frame_syn = numpy.array([1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0], dtype=numpy.int8).tostring()
    data_sync = numpy.array([1, 0]*5 + [1, 1, 0, 1, 0, 0, 0]*2, dtype=numpy.int8).tostring()
    data_term = "10" * 16 + "000100110101111" + "0"

    HEADER_LEN = 660
    WHOLE_HEADER_LEN = HEADER_LEN + len(bit_syn) + len(frame_syn)

    DTMF_TONES = "123A456B789C*0#D"

    STATE_IDLE = 1
    STATE_RX_VOICE = 2

    current_state = STATE_IDLE

    def __init__(self):
        gr.sync_block.__init__(self,
                               name="dstar_rx",
                               in_sig=[numpy.int8],
                               out_sig=None)
        self.f = open("dstar-audio.dst", "wb")
        self.f.write(".dst".encode())

    def unscramble(self, header):
        state = 0b1111111  # Initial state
        poly = 0b10010001  # x^7 + x^4 + 1
        for x in range(len(header)):
            state <<= 1
            state |= ((state >> 7) & 1) ^ ((state >> 4) & 1)
            state &= 0b1111111
            header[x] ^= (state & 1)
        return header

    def deinterleave_header(self, header):
        out_header = numpy.array([0]*self.HEADER_LEN, dtype=numpy.int8)
        index = 0
        for row in range(24):
            for col in range(28 if row < 12 else 27):
                out_header[row + 24 * col] = header[index]
                index += 1
        return out_header

    def viterbi_header(self, header):
        # TODO: Implement proper Viterbi decode.
        out_header = numpy.array([0]*(len(header)//2 - 2), dtype=numpy.int8)
        prev = 0
        prev_prev = 0
        for x in range(len(out_header)):
            out_header[x] = prev_prev ^ prev ^ header[x*2]
            prev_prev = prev
            prev = out_header[x]
        return out_header

    def decode_header(self, header):
        header = self.unscramble(header)
        header = self.deinterleave_header(header)
        header = self.viterbi_header(header)
        header = self.reverse_bytes(header.tostring()).replace('\x00', '0').replace('\x01', '1')
        header_bytes = ''
        for x in range(0, len(header), 8):
            bits = header[x:x+8]
            header_bytes += chr(int(bits, 2))
        print("Destination repeater callsign: " + header_bytes[3:11])
        print("Departure repeater callsign: " + header_bytes[11:19])
        print("Companion callsign: " + header_bytes[19:27])
        print("Own callsign 1: " + header_bytes[27:35])
        print("Own callsign 2: " + header_bytes[35:39])
        print("CRC: " + header[-16:])

    def prng(self, i):
        mask = 0x800000
        prng = 0
        pr = i << 4

        for x in range(24):
            pr = ((173 * pr) + 13849) & 0xFFFF
            if ((pr & 0x8000) != 0):
                prng |= mask
            mask >>= 1

        return prng

    def reverse_bytes(self, bits):
        result = ""
        for x in range(0, len(bits), 8):
            result += bits[x:x+8][::-1]
        return result

    def deinterleave_voice(self, bits):
        return bits[0:72:6] + bits[1:73:6] + bits[2:74:6] + bits[3:75:6] + bits[4:76:6] + bits[5:77:6]

    def golay(self, bits):
        # TODO: Implement proper Golay
        return bits[0:12]

    def work(self, input_items, output_items):
        in0 = input_items[0]

        if self.current_state == self.STATE_IDLE:
            if len(in0) < self.WHOLE_HEADER_LEN:
                return 0

            index = in0.tostring().find(self.bit_syn + self.frame_syn, 0, -self.HEADER_LEN)
            if index == -1:
                self.consume(0, len(in0) - self.WHOLE_HEADER_LEN + 1)
                return 0

            # We found a header!
            start_index = index + len(self.bit_syn) + len(self.frame_syn)
            end_index = start_index + self.HEADER_LEN
            header = in0[start_index:end_index]
            self.decode_header(header)
            self.current_state = self.STATE_RX_VOICE
            self.consume(0, end_index)
            return 0

        elif self.current_state == self.STATE_RX_VOICE:
            if len(in0) < self.VOICE_FRAME_LEN + len(self.data_term):
                return 0

            # We have enough data for a voice frame & a data frame
            bits = in0[0:self.VOICE_FRAME_LEN + len(self.data_term)].tostring().replace('\x00', '0').replace('\x01', '1')
            bits = self.deinterleave_voice(self.reverse_bytes(bits[0:self.VOICE_FRAME_LEN])) + bits[self.VOICE_FRAME_LEN:]

            first_word = int(bits[0:12], 2)
            second_code_word = int(bits[24:48], 2) ^ self.prng(first_word)

            voice_bits = self.golay(bits[0:24]) + self.golay('{0:024b}'.format(second_code_word)) + bits[48:72]
            self.f.write(bytes([int(voice_bits[0:8], 2), int(voice_bits[8:16], 2), int(voice_bits[16:24], 2), int(voice_bits[24:32], 2), int(voice_bits[32:40], 2), int(voice_bits[40:48], 2)]))
            self.f.flush()
            data_bits = self.reverse_bytes(self.unscramble(in0[72:96]).tostring().replace('\x00', '0').replace('\x01', '1'))

            fund_freq = int(voice_bits[0:7], 2)
            if fund_freq == 124:
                fund_freq_text = "Silence"
            elif fund_freq == 126:
                dtmf_tone = self.DTMF_TONES[int(voice_bits[10:12] + voice_bits[41:43], 2)]
                dtmf_ampl = int(voice_bits[12:18] + voice_bits[43:45], 2)
                fund_freq_text = "DTMF: " + dtmf_tone + " Ampl: " + str(dtmf_ampl)
            else:
                fund_freq_text = '{0:03}'.format(fund_freq)

            print(voice_bits + " " + data_bits + " " + fund_freq_text)

            # Check whether we've reached the end of a transmission:
            if bits[self.VOICE_FRAME_LEN:] == self.data_term:
                self.consume(0, self.VOICE_FRAME_LEN + len(self.data_term))
                self.current_state = self.STATE_IDLE
                print("End of transmission.")
            else:
                self.consume(0, self.TOTAL_FRAME_LEN)
            return 160
