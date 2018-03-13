#! /usr/bin/env python
# encoding: utf-8

import os

# the following two variables are used by the target "waf dist"
VERSION='0.2'
APPNAME='nekobee'

# these variables are mandatory ('/' are converted automatically)
srcdir = '.'
blddir = 'build'

def options(opt):
    opt.load('compiler_c')

def configure(conf):
    conf.load('compiler_c')

    conf.check_cfg(package='dssi', args='--cflags --libs')
    conf.check_cfg(package='liblo', args='--cflags --libs')
    conf.check_cfg(package='gtk+-2.0', args='--cflags --libs')

    conf.env['DSSI_DIR'] = os.path.normpath(os.path.join(conf.env['PREFIX'], 'lib', 'dssi'))
    conf.env['INSTALL_DIR'] = os.path.join(conf.env['DSSI_DIR'], 'nekobee')
    conf.env.CPPFLAGS = ['-g']

    conf.define('INSTALL_DIR', conf.env['INSTALL_DIR'])
    conf.write_config_header('config.h')

def build(bld):
    # DSSI plugin
    plugin_dssi = bld(features='c cshlib')
    plugin_dssi.env.append_value("LINKFLAGS", "-lm")
    plugin_dssi.includes = ['.', 'src']
    plugin_dssi.defines = 'HAVE_CONFIG_H'
    plugin_dssi.source = [
	'src/nekobee-dssi.c',
	'src/nekobee_data.c',
	'src/nekobee_ports.c',
	'src/nekobee_synth.c',
	'src/nekobee_voice.c',
	'src/nekobee_voice_render.c',
	'src/minblep_tables.c',
        ]
    plugin_dssi.target = 'nekobee'
    plugin_dssi.install_path = '${DSSI_DIR}/'

    # DSSI UI executable
    gui_gtk = bld(features='c cprogram')
    gui_gtk.env.append_value("LINKFLAGS", "-lm")
    gui_gtk.includes = ['.', 'src']
    gui_gtk.defines = 'HAVE_CONFIG_H'
    gui_gtk.source = [
	'src/gui_callbacks.c',
	'src/gui_data.c',
	'src/gui_interface.c',
	'src/gtkknob.c',
#	'src/gtk/slider.c',
	'src/gui_main.c',
	'src/nekobee_data.c',
	'src/nekobee_ports.c',
        ]
    gui_gtk.uselib = 'GTK+-2.0 LIBLO'
    gui_gtk.target = 'nekobee_gtk'
    gui_gtk.install_path = '${INSTALL_DIR}/'

