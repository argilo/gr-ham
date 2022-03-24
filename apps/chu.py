#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Chu
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import ham
import osmosdr
import time

from gnuradio import qtgui

class chu(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Chu")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Chu")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "chu")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1200000
        self.upconverter_lo_freq = upconverter_lo_freq = 0
        self.space_tone = space_tone = 2025
        self.offset = offset = 100000
        self.mark_tone = mark_tone = 2225
        self.gain = gain = 10
        self.decimation = decimation = samp_rate // 48000
        self.chu_freq = chu_freq = 3330000
        self.channel_rate = channel_rate = 4800

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 50, 0.4, 10, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'RX gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._gain_win)
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                channel_rate,
                300,
                0.35,
                100))
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.osmosdr_source_1 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_1.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(chu_freq - offset + upconverter_lo_freq, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_gain(gain, 0)
        self.osmosdr_source_1.set_if_gain(20, 0)
        self.osmosdr_source_1.set_bb_gain(20, 0)
        self.osmosdr_source_1.set_antenna('', 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)
        self.low_pass_filter_1 = filter.fir_filter_ccf(
            10,
            firdes.low_pass(
                1000,
                samp_rate / 25,
                200,
                50,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decimation,
            firdes.low_pass(
                1,
                samp_rate,
                20000,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.ham_chu_decode_0 = ham.chu_decode()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_multiply_xx_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-1)
        self.band_pass_filter_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                samp_rate / decimation,
                200,
                2800,
                200,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate / decimation, analog.GR_COS_WAVE, -(space_tone + mark_tone) / 2, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -offset, 1, 0, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(channel_rate / (3.1416*(mark_tone - space_tone)))
        self.analog_pll_carriertracking_cc_0 = analog.pll_carriertracking_cc(3.1416 / 500, 1.8, -1.8)
        self.analog_agc_xx_0 = analog.agc_ff(1e-1, 0.02, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.low_pass_filter_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.ham_chu_decode_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_pll_carriertracking_cc_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.osmosdr_source_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "chu")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decimation(self.samp_rate // 48000)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate / self.decimation)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate / self.decimation, 200, 2800, 200, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 20000, 5000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1000, self.samp_rate / 25, 200, 50, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_upconverter_lo_freq(self):
        return self.upconverter_lo_freq

    def set_upconverter_lo_freq(self, upconverter_lo_freq):
        self.upconverter_lo_freq = upconverter_lo_freq
        self.osmosdr_source_1.set_center_freq(self.chu_freq - self.offset + self.upconverter_lo_freq, 0)

    def get_space_tone(self):
        return self.space_tone

    def set_space_tone(self, space_tone):
        self.space_tone = space_tone
        self.analog_quadrature_demod_cf_0.set_gain(self.channel_rate / (3.1416*(self.mark_tone - self.space_tone)))
        self.analog_sig_source_x_1.set_frequency(-(self.space_tone + self.mark_tone) / 2)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.analog_sig_source_x_0.set_frequency(-self.offset)
        self.osmosdr_source_1.set_center_freq(self.chu_freq - self.offset + self.upconverter_lo_freq, 0)

    def get_mark_tone(self):
        return self.mark_tone

    def set_mark_tone(self, mark_tone):
        self.mark_tone = mark_tone
        self.analog_quadrature_demod_cf_0.set_gain(self.channel_rate / (3.1416*(self.mark_tone - self.space_tone)))
        self.analog_sig_source_x_1.set_frequency(-(self.space_tone + self.mark_tone) / 2)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_1.set_gain(self.gain, 0)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate / self.decimation)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate / self.decimation, 200, 2800, 200, window.WIN_HAMMING, 6.76))

    def get_chu_freq(self):
        return self.chu_freq

    def set_chu_freq(self, chu_freq):
        self.chu_freq = chu_freq
        self.osmosdr_source_1.set_center_freq(self.chu_freq - self.offset + self.upconverter_lo_freq, 0)

    def get_channel_rate(self):
        return self.channel_rate

    def set_channel_rate(self, channel_rate):
        self.channel_rate = channel_rate
        self.analog_quadrature_demod_cf_0.set_gain(self.channel_rate / (3.1416*(self.mark_tone - self.space_tone)))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.channel_rate, 300, 0.35, 100))





def main(top_block_cls=chu, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
