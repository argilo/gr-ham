#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Chu
# Generated: Mon Feb 24 08:11:09 2014
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ham
import math
import osmosdr
import wx

class chu(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Chu")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1200000
        self.upconverter_lo_freq = upconverter_lo_freq = 125000000
        self.space_tone = space_tone = 2025
        self.offset = offset = 100000
        self.mark_tone = mark_tone = 2225
        self.gain = gain = 10
        self.decimation = decimation = samp_rate / 48000
        self.chu_freq = chu_freq = 3330000
        self.channel_rate = channel_rate = 4800

        ##################################################
        # Blocks
        ##################################################
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "48 kHz")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "4.8 kHz")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "Data scope")
        self.GridAdd(self.nb, 2, 0, 1, 1)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="USB tuner gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=50,
        	num_steps=125,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_gain_sizer, 1, 0, 1, 1)
        self._chu_freq_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.chu_freq,
        	callback=self.set_chu_freq,
        	label="CHU frequency",
        	choices=[3330000, 7850000, 14670000],
        	labels=['3.33 MHz', '7.85 MHz', '14.67 MHz'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._chu_freq_chooser, 0, 0, 1, 1)
        self.wxgui_waterfallsink2_1 = waterfallsink2.waterfall_sink_c(
        	self.nb.GetPage(1).GetWin(),
        	baseband_freq=(mark_tone + space_tone) / 2,
        	dynamic_range=50,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=channel_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.nb.GetPage(1).Add(self.wxgui_waterfallsink2_1.win)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.nb.GetPage(0).GetWin(),
        	baseband_freq=chu_freq,
        	dynamic_range=50,
        	ref_level=-60,
        	ref_scale=2.0,
        	sample_rate=samp_rate / decimation,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        	win=window.hamming,
        )
        self.nb.GetPage(0).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.nb.GetPage(2).GetWin(),
        	title="Scope Plot",
        	sample_rate=channel_rate,
        	v_scale=1,
        	v_offset=0,
        	t_scale=0.050,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=2,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.nb.GetPage(2).Add(self.wxgui_scopesink2_0.win)
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(1, firdes.root_raised_cosine(
        	1, channel_rate, 300, 0.35, 100))
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(chu_freq - offset + upconverter_lo_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(0, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_1 = filter.fir_filter_ccf(10, firdes.low_pass(
        	1000, samp_rate / 25, 200, 50, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(decimation, firdes.low_pass(
        	1, samp_rate, 20000, 5000, firdes.WIN_HAMMING, 6.76))
        self.ham_chu_decode_0 = ham.chu_decode()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_multiply_xx_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 0.5)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.band_pass_filter_0 = filter.fir_filter_ccc(1, firdes.complex_band_pass(
        	1, samp_rate / decimation, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0_0 = audio.sink(48000, "", True)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate / decimation, analog.GR_COS_WAVE, -(space_tone + mark_tone) / 2, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -offset, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(channel_rate / (3.1416*(mark_tone - space_tone)))
        self.analog_pll_carriertracking_cc_0 = analog.pll_carriertracking_cc(3.1416 / 500, 1.8, -1.8)
        self.analog_agc_xx_0 = analog.agc_ff(1e-1, 0.02, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_pll_carriertracking_cc_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.wxgui_waterfallsink2_1, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.low_pass_filter_1, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.wxgui_scopesink2_0, 1))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.ham_chu_decode_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.root_raised_cosine_filter_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decimation(self.samp_rate / 48000)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate / self.decimation)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate / self.decimation, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate / self.decimation)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1000, self.samp_rate / 25, 200, 50, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 20000, 5000, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_upconverter_lo_freq(self):
        return self.upconverter_lo_freq

    def set_upconverter_lo_freq(self, upconverter_lo_freq):
        self.upconverter_lo_freq = upconverter_lo_freq
        self.osmosdr_source_0.set_center_freq(self.chu_freq - self.offset + self.upconverter_lo_freq, 0)

    def get_space_tone(self):
        return self.space_tone

    def set_space_tone(self, space_tone):
        self.space_tone = space_tone
        self.analog_sig_source_x_1.set_frequency(-(self.space_tone + self.mark_tone) / 2)
        self.wxgui_waterfallsink2_1.set_baseband_freq((self.mark_tone + self.space_tone) / 2)
        self.analog_quadrature_demod_cf_0.set_gain(self.channel_rate / (3.1416*(self.mark_tone - self.space_tone)))

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.analog_sig_source_x_0.set_frequency(-self.offset)
        self.osmosdr_source_0.set_center_freq(self.chu_freq - self.offset + self.upconverter_lo_freq, 0)

    def get_mark_tone(self):
        return self.mark_tone

    def set_mark_tone(self, mark_tone):
        self.mark_tone = mark_tone
        self.analog_sig_source_x_1.set_frequency(-(self.space_tone + self.mark_tone) / 2)
        self.wxgui_waterfallsink2_1.set_baseband_freq((self.mark_tone + self.space_tone) / 2)
        self.analog_quadrature_demod_cf_0.set_gain(self.channel_rate / (3.1416*(self.mark_tone - self.space_tone)))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate / self.decimation)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate / self.decimation, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate / self.decimation)

    def get_chu_freq(self):
        return self.chu_freq

    def set_chu_freq(self, chu_freq):
        self.chu_freq = chu_freq
        self._chu_freq_chooser.set_value(self.chu_freq)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.chu_freq)
        self.osmosdr_source_0.set_center_freq(self.chu_freq - self.offset + self.upconverter_lo_freq, 0)

    def get_channel_rate(self):
        return self.channel_rate

    def set_channel_rate(self, channel_rate):
        self.channel_rate = channel_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.channel_rate)
        self.wxgui_waterfallsink2_1.set_sample_rate(self.channel_rate)
        self.analog_quadrature_demod_cf_0.set_gain(self.channel_rate / (3.1416*(self.mark_tone - self.space_tone)))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.channel_rate, 300, 0.35, 100))

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = chu()
    tb.Start(True)
    tb.Wait()

