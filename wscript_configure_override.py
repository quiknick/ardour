# wscript_configure_override.py
# Place in Ardour root (same dir as wscript)
# Forces GCC, blocks MSVC, works with MSYS2 + MinGW-w64

import os
import sys
from waflib import Configure, Context

print(">>> FORCING MinGW GCC, BLOCKING MSVC <<<")

# === 1. Force compiler lists for 'win32' platform ===
from waflib.Tools import compiler_c, compiler_cxx

compiler_c.c_compiler['win32'] = ['gcc']
compiler_cxx.cxx_compiler['win32'] = ['g++']

# Remove all other compilers
compiler_c.c_compiler = {'win32': ['gcc'], 'default': ['gcc']}
compiler_cxx.cxx_compiler = {'win32': ['g++'], 'default': ['g++']}

# === 2. Block MSVC tool from being loaded at all ===
@Configure.conf
def load_msvc(conf, *k, **kw):
    print(">>> BLOCKED: load_msvc() called — MSVC disabled")
    return  # Do nothing — prevent MSVC from loading

# === 3. Force environment in configure ===
def options(opt):
    # Prevent option parsing from loading MSVC
    pass

def configure(conf):
    # Force GCC
    conf.env.CC = 'gcc'
    conf.env.CXX = 'g++'
    conf.env.LINK_CC = 'gcc'
    conf.env.LINK_CXX = 'g++'

    # Spoof platform
    if sys.platform == 'win32':
        sys.platform = 'linux'

    # Critical: prevent MSVC detection
    conf.env.DEST_OS = 'linux'
    conf.env['MSVC_COMPILER'] = False
    conf.env['MSVC_INSTALLED_VERSIONS'] = []
    conf.env['MSVC_TARGETS'] = []

    # Optional: force compiler names
    conf.env.CC_NAME = 'gcc'
    conf.env.CXX_NAME = 'g++'

    print(">>> GCC forced: CC=", conf.env.CC, "CXX=", conf.env.CXX)
