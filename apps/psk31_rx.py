#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Psk31 Rx
# Generated: Fri Jan  3 22:50:49 2014
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import digital;import cmath
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import termsink
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ham
import osmosdr
import wx

class psk31_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Psk31 Rx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.psk_offset = psk_offset = 843
        self.center_freq = center_freq = 441000000
        self.variable_text_box_0 = variable_text_box_0 = psk_offset
        self.samp_rate = samp_rate = 960000
        self.psk_center = psk_center = center_freq + 125000
        self.int_rate = int_rate = 48000
        self.gain = gain = 40
        self.corr = corr = 0
        self.audio_rate = audio_rate = 8000

        ##################################################
        # Message Queues
        ##################################################
        blocks_message_sink_0_msgq_out = wxgui_termsink_0_msgq_in = gr.msg_queue(2)

        ##################################################
        # Blocks
        ##################################################
        _psk_offset_sizer = wx.BoxSizer(wx.VERTICAL)
        self._psk_offset_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_psk_offset_sizer,
        	value=self.psk_offset,
        	callback=self.set_psk_offset,
        	label="PSK offset",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._psk_offset_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_psk_offset_sizer,
        	value=self.psk_offset,
        	callback=self.set_psk_offset,
        	minimum=0,
        	maximum=3000,
        	num_steps=300,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_psk_offset_sizer, 1, 0, 1, 2)
        _psk_center_sizer = wx.BoxSizer(wx.VERTICAL)
        self._psk_center_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_psk_center_sizer,
        	value=self.psk_center,
        	callback=self.set_psk_center,
        	label="Tuning",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._psk_center_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_psk_center_sizer,
        	value=self.psk_center,
        	callback=self.set_psk_center,
        	minimum=center_freq - (samp_rate / 2),
        	maximum=center_freq + (samp_rate / 2),
        	num_steps=192,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_psk_center_sizer, 0, 0, 1, 2)
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "960 kHz")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "48 kHz")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "4 kHz")
        self.GridAdd(self.nb, 3, 0, 1, 2)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=49.6,
        	num_steps=124,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_gain_sizer, 2, 0, 1, 1)
        _corr_sizer = wx.BoxSizer(wx.VERTICAL)
        self._corr_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	label='corr',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._corr_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	minimum=-150,
        	maximum=150,
        	num_steps=300,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_corr_sizer, 2, 1, 1, 1)
        self.wxgui_waterfallsink2_2 = waterfallsink2.waterfall_sink_f(
        	self.nb.GetPage(2).GetWin(),
        	baseband_freq=0,
        	dynamic_range=30,
        	ref_level=-40,
        	ref_scale=2.0,
        	sample_rate=audio_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        	win=window.blackmanharris,
        	size=((800,400)),
        )
        self.nb.GetPage(2).Add(self.wxgui_waterfallsink2_2.win)
        def wxgui_waterfallsink2_2_callback(x, y):
        	self.set_psk_offset(x)
        
        self.wxgui_waterfallsink2_2.set_callback(wxgui_waterfallsink2_2_callback)
        self.wxgui_waterfallsink2_1 = waterfallsink2.waterfall_sink_c(
        	self.nb.GetPage(1).GetWin(),
        	baseband_freq=psk_center,
        	dynamic_range=30,
        	ref_level=-30,
        	ref_scale=2.0,
        	sample_rate=int_rate,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        	size=((800,400)),
        )
        self.nb.GetPage(1).Add(self.wxgui_waterfallsink2_1.win)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.nb.GetPage(0).GetWin(),
        	baseband_freq=center_freq,
        	dynamic_range=30,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        	size=((800,400)),
        )
        self.nb.GetPage(0).Add(self.wxgui_waterfallsink2_0.win)
        def wxgui_waterfallsink2_0_callback(x, y):
        	self.set_psk_center(x)
        
        self.wxgui_waterfallsink2_0.set_callback(wxgui_waterfallsink2_0_callback)
        self.wxgui_termsink_0 = termsink.termsink(
        	parent=self.GetWin(),
        	msgq=wxgui_termsink_0_msgq_in,
        )
        self.Add(self.wxgui_termsink_0)
        self._variable_text_box_0_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.variable_text_box_0,
        	callback=self.set_variable_text_box_0,
        	label="Frequency",
        	converter=forms.float_converter(),
        )
        self.Add(self._variable_text_box_0_text_box)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(0, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.ham_varicode_rx_0 = ham.varicode_rx()
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(16, (firdes.low_pass(1, audio_rate, 31.25, 10, firdes.WIN_HAMMING, 6.76)), psk_offset, audio_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(samp_rate / int_rate, (firdes.low_pass(1, samp_rate, 12000, 12000, firdes.WIN_HAMMING, 6.76)), round(psk_center - center_freq,-3), samp_rate)
        self.digital_mpsk_receiver_cc_0 = digital.mpsk_receiver_cc(2, 0, cmath.pi/100.0, -0.1, 0.1, 0.25, 0.01, 16, 0.001, 0.001)
        self.digital_diff_phasor_cc_0 = digital.diff_phasor_cc()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_message_sink_0 = blocks.message_sink(gr.sizeof_char*1, blocks_message_sink_0_msgq_out, True)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter_0 = filter.fir_filter_ccc(int_rate / audio_rate, firdes.complex_band_pass(
        	1, int_rate, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(audio_rate, "plughw:0,0", True)
        self.analog_agc2_xx_1 = analog.agc2_ff(1e-1, 1e-2, 0.1, 1.0)
        self.analog_agc2_xx_1.set_max_gain(0.0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_1, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.ham_varicode_rx_0, 0), (self.blocks_message_sink_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.ham_varicode_rx_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.digital_diff_phasor_cc_0, 0))
        self.connect((self.digital_diff_phasor_cc_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.digital_mpsk_receiver_cc_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.analog_agc2_xx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.analog_agc2_xx_1, 0))
        self.connect((self.band_pass_filter_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.wxgui_waterfallsink2_2, 0))


# QT sink close method reimplementation

    def get_psk_offset(self):
        return self.psk_offset

    def set_psk_offset(self, psk_offset):
        self.psk_offset = psk_offset
        self._psk_offset_slider.set_value(self.psk_offset)
        self._psk_offset_text_box.set_value(self.psk_offset)
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.psk_offset)
        self.set_variable_text_box_0(self.psk_offset)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_psk_center(self.center_freq + 125000)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.center_freq)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(round(self.psk_center - self.center_freq,-3))

    def get_variable_text_box_0(self):
        return self.variable_text_box_0

    def set_variable_text_box_0(self, variable_text_box_0):
        self.variable_text_box_0 = variable_text_box_0
        self._variable_text_box_0_text_box.set_value(self.variable_text_box_0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 12000, 12000, firdes.WIN_HAMMING, 6.76)))

    def get_psk_center(self):
        return self.psk_center

    def set_psk_center(self, psk_center):
        self.psk_center = psk_center
        self._psk_center_slider.set_value(self.psk_center)
        self._psk_center_text_box.set_value(self.psk_center)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(round(self.psk_center - self.center_freq,-3))
        self.wxgui_waterfallsink2_1.set_baseband_freq(self.psk_center)

    def get_int_rate(self):
        return self.int_rate

    def set_int_rate(self, int_rate):
        self.int_rate = int_rate
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.int_rate, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.wxgui_waterfallsink2_1.set_sample_rate(self.int_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_corr(self):
        return self.corr

    def set_corr(self, corr):
        self.corr = corr
        self._corr_slider.set_value(self.corr)
        self._corr_text_box.set_value(self.corr)
        self.osmosdr_source_0.set_freq_corr(self.corr, 0)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.freq_xlating_fir_filter_xxx_1.set_taps((firdes.low_pass(1, self.audio_rate, 31.25, 10, firdes.WIN_HAMMING, 6.76)))
        self.wxgui_waterfallsink2_2.set_sample_rate(self.audio_rate)

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = psk31_rx()
    tb.Start(True)
    tb.Wait()

