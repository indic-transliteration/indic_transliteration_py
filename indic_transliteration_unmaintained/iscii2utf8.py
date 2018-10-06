#!/usr/bin/env python

# released under BSD License

# mary <mary@sarai.net> aka meyarivan <self@meyarivan.org>

# inspired by ICU [ http://oss.software.ibm.com/icu/ ]

# code still in alpha stage.. lots of redundant code.. and probably incorrect
# if ya find errors, pls submit bug reports at indlinux

# for usage, either run the script or scroll down to end of the script

import sys
import array
import logging

# Generic Constants

ISCII_ATR                 = 0x00EF
DEV_ABBR_SIGN             = 0x0970
ATR_MASK                  = 0x004F
DANDA                     = 0x0964
DELTA                     = 0x0080
DEV_SVARITA               = 0x0951
DEV_ANUDATTA              = 0x0952
DOUBLE_DANDA              = 0x0965                   
ISCII_EXT                 = 0x00F0
EXT_RANGE_BEGIN           = 0x00A1
EXT_RANGE_END             = 0x00EE
HALANT                    = 0x094d
INDIC_BLOCK_BEGIN         = 0x0900
INDIC_BLOCK_END           = 0x0D7F
INVALID_CHAR              = 0xFFFF
ISCII_BEGIN               = 0x00A0
ISCII_DANDA               = 0x00EA
ISCII_HALANT              = 0x00E8
ISCII_INV                 = 0x00D9
ISCII_NUKTA               = 0x00E9
LF                        = 0x000A
NO_CHAR                   = 0xFFFE
UNI_BEGIN                 = 0x0900
UNI_END                   = 0x097F
ZWJ                       = 0x200d
ZWNJ                      = 0x200c


# map between the ISCII scripts as specified via the ATR switch
# and the script in unicode

# bengali and assamese have same script except for two characters
# (according to ISCII 91

ISCII_SCRIPTS = {
    0x40 : -1, # DEFAULT
    0x42 : 0,  # DEVNAG
    0x43 : 1,  # BENGALI
    0x44 : 5,  # TAMIL
    0x45 : 6,  # TELUGU
    0x46 : 1,  # ASSAMESE
    0x47 : 4,  # ORIYA 
    0x48 : 7,  # KANNADA
    0x49 : 8,  # MALAYALAM
    0x4A : 3,  # GUJARATI
    0x4B : 2   # PUNJABI
    }

# ISCII_SPECIAL CHARS

ISCII_SPECIALS = [ISCII_ATR, ISCII_EXT, ISCII_INV]

iscii_to_unicode = {
    0xa0 : 0x900,
    0xa1 : 0x901,
    0xa2 : 0x902,
    0xa3 : 0x903,
    0xa4 : 0x905,
    0xa5 : 0x906,
    0xa6 : 0x907,
    0xa7 : 0x908,
    0xa8 : 0x909,
    0xa9 : 0x90a,
    0xaa : 0x90b,
    0xab : 0x90e,
    0xac : 0x90f,
    0xad : 0x910,
    0xae : 0x90d,
    0xaf : 0x912,
    0xb0 : 0x913,
    0xb1 : 0x914,
    0xb2 : 0x911,
    0xb3 : 0x915,
    0xb4 : 0x916,
    0xb5 : 0x917,
    0xb6 : 0x918,
    0xb7 : 0x919,
    0xb8 : 0x91a,
    0xb9 : 0x91b,
    0xba : 0x91c,
    0xbb : 0x91d,
    0xbc : 0x91e,
    0xbd : 0x91f,
    0xbe : 0x920,
    0xbf : 0x921,
    0xc0 : 0x922,
    0xc1 : 0x923,
    0xc2 : 0x924,
    0xc3 : 0x925,
    0xc4 : 0x926,
    0xc5 : 0x927,
    0xc6 : 0x928,
    0xc7 : 0x929,
    0xc8 : 0x92a,
    0xc9 : 0x92b,
    0xca : 0x92c,
    0xcb : 0x92d,
    0xcc : 0x92e,
    0xcd : 0x92f,
    0xce : 0x95f,
    0xcf : 0x930,
    0xd0 : 0x931,
    0xd1 : 0x932,
    0xd2 : 0x933,
    0xd3 : 0x934,
    0xd4 : 0x935,
    0xd5 : 0x936,
    0xd6 : 0x937,
    0xd7 : 0x938,
    0xd8 : 0x939,
    0xd9 : 0x200d,
    0xda : 0x93e,
    0xdb : 0x93f,
    0xdc : 0x940,
    0xdd : 0x941,
    0xde : 0x942,
    0xdf : 0x943,
    0xe0 : 0x946,
    0xe1 : 0x947,
    0xe2 : 0x948,
    0xe3 : 0x945,
    0xe4 : 0x94a,
    0xe5 : 0x94b,
    0xe6 : 0x94c,
    0xe7 : 0x949,
    0xe8 : 0x94d,
    0xe9 : 0x93c,
    0xea : 0x964,
    0xeb : 0xffff,
    0xec : 0xffff,
    0xed : 0xffff,
    0xee : 0xffff,
    0xef : 0xffff,
    0xf0 : 0xffff,
    0xf1 : 0x966,
    0xf2 : 0x967,
    0xf3 : 0x968,
    0xf4 : 0x969,
    0xf5 : 0x96a,
    0xf6 : 0x96b,
    0xf7 : 0x96c,
    0xf8 : 0x96d,
    0xf9 : 0x96e,
    0xfa : 0x96f,
    0xfb : 0xffff,
    0xfc : 0xffff,
    0xfd : 0xffff,
    0xfe : 0xffff,
    0xff : 0xffff
    }


"""
# code to generate the validation_table
  ( ya ya .. agreed that it is kludgy)

# need python 2.3

import unicodedata

UNI_BEGIN = 0x0900
UNI_END = 0x097F
DELTA = 0x80
SCRS = 9

table = []

for char in range(UNI_END - UNI_BEGIN + 1):
    res = [0] * SCRS
    for scr in range(0, SCRS):
        val = unichr(UNI_BEGIN + (scr * DELTA) + char)
        res[scr] = int(unicodedata.name(val, None) is not None)

    table.append(res)

"""

validation_table = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #    0x0      0
    [1, 1, 0, 1, 1, 0, 1, 0, 0], #    0x1      1
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0x2      2
    [1, 1, 0, 1, 1, 1, 1, 1, 1], #    0x3      3
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #    0x4      4
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0x5      5
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0x6      6
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0x7      7
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0x8      8
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0x9      9
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0xa     10
    [1, 1, 0, 1, 1, 0, 1, 1, 1], #    0xb     11
    [1, 1, 0, 0, 1, 0, 1, 1, 1], #    0xc     12
    [1, 0, 0, 1, 0, 0, 0, 0, 0], #    0xd     13
    [1, 0, 0, 0, 0, 1, 1, 1, 1], #    0xe     14
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #    0xf     15
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x10     16
    [1, 0, 0, 1, 0, 0, 0, 0, 0], #   0x11     17
    [1, 0, 0, 0, 0, 1, 1, 1, 1], #   0x12     18
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x13     19
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x14     20
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x15     21
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x16     22
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x17     23
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x18     24
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x19     25
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x1a     26
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x1b     27
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x1c     28
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x1d     29
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x1e     30
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x1f     31
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x20     32
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x21     33
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x22     34
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x23     35
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x24     36
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x25     37
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x26     38
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x27     39
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x28     40
    [1, 0, 0, 0, 0, 1, 0, 0, 0], #   0x29     41
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x2a     42
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x2b     43
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x2c     44
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x2d     45
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x2e     46
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x2f     47
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x30     48
    [1, 0, 0, 0, 0, 1, 1, 1, 1], #   0x31     49
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x32     50
    [1, 0, 1, 1, 1, 1, 1, 1, 1], #   0x33     51
    [1, 0, 0, 0, 0, 1, 0, 0, 1], #   0x34     52
    [1, 0, 1, 1, 0, 1, 1, 1, 1], #   0x35     53
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x36     54
    [1, 1, 0, 1, 1, 1, 1, 1, 1], #   0x37     55
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x38     56
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x39     57
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x3a     58
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x3b     59
    [1, 1, 1, 1, 1, 0, 0, 0, 0], #   0x3c     60
    [1, 0, 0, 1, 1, 0, 0, 0, 0], #   0x3d     61
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x3e     62
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x3f     63
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x40     64
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x41     65
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x42     66
    [1, 1, 0, 1, 1, 0, 1, 1, 1], #   0x43     67
    [1, 1, 0, 1, 0, 0, 1, 1, 0], #   0x44     68
    [1, 0, 0, 1, 0, 0, 0, 0, 0], #   0x45     69
    [1, 0, 0, 0, 0, 1, 1, 1, 1], #   0x46     70
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x47     71
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x48     72
    [1, 0, 0, 1, 0, 0, 0, 0, 0], #   0x49     73
    [1, 0, 0, 0, 0, 1, 1, 1, 1], #   0x4a     74
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x4b     75
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x4c     76
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x4d     77
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x4e     78
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x4f     79
    [1, 0, 0, 1, 0, 0, 0, 0, 0], #   0x50     80
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x51     81
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x52     82
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x53     83
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x54     84
    [0, 0, 0, 0, 0, 0, 1, 1, 0], #   0x55     85
    [0, 0, 0, 0, 1, 0, 1, 1, 0], #   0x56     86
    [0, 1, 0, 0, 1, 1, 0, 0, 1], #   0x57     87
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x58     88
    [1, 0, 1, 0, 0, 0, 0, 0, 0], #   0x59     89
    [1, 0, 1, 0, 0, 0, 0, 0, 0], #   0x5a     90
    [1, 0, 1, 0, 0, 0, 0, 0, 0], #   0x5b     91
    [1, 1, 1, 0, 1, 0, 0, 0, 0], #   0x5c     92
    [1, 1, 0, 0, 1, 0, 0, 0, 0], #   0x5d     93
    [1, 0, 1, 0, 0, 0, 0, 1, 0], #   0x5e     94
    [1, 1, 0, 0, 1, 0, 0, 0, 0], #   0x5f     95
    [1, 1, 0, 1, 1, 0, 1, 1, 1], #   0x60     96
    [1, 1, 0, 0, 1, 0, 1, 1, 1], #   0x61     97
    [1, 1, 0, 0, 0, 0, 0, 0, 0], #   0x62     98
    [1, 1, 0, 0, 0, 0, 0, 0, 0], #   0x63     99
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x64    100
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #   0x65    101
    [1, 1, 1, 1, 1, 0, 1, 1, 1], #   0x66    102
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x67    103
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x68    104
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x69    105
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x6a    106
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x6b    107
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x6c    108
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x6d    109
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x6e    110
    [1, 1, 1, 1, 1, 1, 1, 1, 1], #   0x6f    111
    [1, 1, 1, 0, 1, 1, 0, 0, 0], #   0x70    112
    [0, 1, 1, 0, 0, 1, 0, 0, 0], #   0x71    113
    [0, 1, 1, 0, 0, 1, 0, 0, 0], #   0x72    114
    [0, 1, 1, 0, 0, 0, 0, 0, 0], #   0x73    115
    [0, 1, 1, 0, 0, 0, 0, 0, 0], #   0x74    116
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #   0x75    117
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #   0x76    118
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #   0x77    119
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #   0x78    120
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #   0x79    121
    [0, 1, 0, 0, 0, 0, 0, 0, 0], #   0x7a    122
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x7b    123
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x7c    124
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x7d    125
    [0, 0, 0, 0, 0, 0, 0, 0, 0], #   0x7e    126
    [0, 0, 0, 0, 0, 0, 0, 0, 0]  #   0x7f    127
    ]

# special characters formed by combination of consonants and nukta

nukta_specials = {
    0xA6 : 0x090c,
    0xEA : 0x093D,
    0xDF : 0x0944,
    0xA1 : 0x0950,
    0xB3 : 0x0958,
    0xB4 : 0x0959,
    0xB5 : 0x095A,
    0xBA : 0x095B,
    0xBF : 0x095C,
    0xC0 : 0x095D,
    0xC9 : 0x095E,
    0xAA : 0x0960,
    0xA7 : 0x0961,
    0xDB : 0x0962,
    0xDC : 0x0963
    }
    

special_maps = {
    ## the two points which are different between assamese and bengali
    ## (according to the charts in ISCII-91 documentation)
    (5, 0xCF) : 0x09F0,
    (5, 0xD4) : 0x09F1,
    }



def make_script_maps():
    _invalid_range = list(range(0xEB, 0xF1)) + list(range(0xFB, 0xFF + 1))
    scripts = {}
    
    for i in range(9):
        curr_scr = {}

        for ch in range(0xA0):
            curr_scr[ch] = ch


        for ch in range(0xA0, 0xFF + 1):
                
            if (ch in _invalid_range):
                continue
            
            t = iscii_to_unicode[ch]
            
            if validation_table[t & 0xFF][i]:
                curr_scr[ch] = t

                curr_scr[ch] += (i * 0x80)

            
        scripts[i] = curr_scr

    for i in special_maps:
        scripts[i[0]][i[1]] = special_maps[i]

    return scripts

## setup the script map  (iscii -> unicode) for all the supported scripts
## hope it speeds up things

script_maps = make_script_maps()

####

def make_invalid_maps():
    maps = {}

    for i in range(9):
        curr_map = {}
        
        for j in range(0xFF + 1):
            curr_map[j] = (j not in script_maps[i]) and \
                          (j not in ISCII_SPECIALS)
        maps[i] = curr_map
        
    return maps

## setup the map of invalid characters for each script

invalid_chars = make_invalid_maps()

## tmp code

iscii_modifying = {}
_tmp = ISCII_SPECIALS + [ISCII_HALANT, ISCII_NUKTA, ISCII_DANDA]

for i in range(0xFF + 1):
    iscii_modifying[i] = int(i in _tmp)

## end of tmp code

def to_utf8(y):
    """
    converts an array of integers to utf8 string
    """

    out = []

    for x in y:

        if x < 0x080:
            out.append(x)
        elif x < 0x0800:
            out.append((x >> 6) | 0xC0)
            out.append((x & 0x3F) | 0x80)
        elif x < 0x10000:
            out.append((x >> 12) | 0xE0)
            out.append(((x >> 6) & 0x3F) | 0x80)
            out.append((x & 0x3F) | 0x80)
        else:
            out.append((x >> 18) | 0xF0)
            out.append((x >> 12) & 0x3F)
            out.append(((x >> 6) & 0x3F) | 0x80)
            out.append((x & 0x3F) | 0x80)

    return ''.join(map(chr, out))
        
    
class IllegalInput(Exception):
    def __init__(self, e):
        self.exception = e

    def __str__(self):
        return repr(self.exception)
    

class Parser:
    def __init__(self):

        self.delta = 0
        self.curr_mask = 0 # current mask to unicode

        self.prev_char = self.src_char = self.dest_char = NO_CHAR

        self.dest = []
        self.pos = 0

        self.stat = [0] * 10

    def write_output(self):

        out = to_utf8(self.dest)
        sys.stdout.write(out)

        self.dest = []
        
                       

    def set_script(self, i):
        """
        set the value of delta to reflect the current codepage
        
        """

        if i in range(1, 10):
            n = i - 1
        else:
            raise IllegalInput("Invalid Value for ATR %s" % (hex(i)))

        if n > -1: # n = -1 is the default script ..
            self.curr_script = n
            self.delta = n * DELTA
        
        return
    

    def isvalid(self, i):

        return validation_table[i & 0xFF][self.curr_script]
    

    def isvalid_iscii(self, x):

        return x not in invalid_chars[self.curr_script]


    def is_nukta_special(self, i):

        x = nukta_specials.get(i, None)

        return x


    def handle_ext(self, curr_char):

        self.pos += 1 # for EXT
        
        for a in range(1):
            
            if not ((EXT_RANGE_END >= curr_char) and
                    (EXT_RANGE_BEGIN <= curr_char)):
                break
            
            if curr_char not in [0xBF, 0xB5, 0xB8]:
                break
            
            if curr_char == 0xBF:
                dest_char = DEV_ABBR_SIGN
            elif curr_char == 0xB5:
                dest_char = DEV_SVARITA
            else:
                dest_char = DEV_ANUDATTA
                    
            if self.isvalid(dest_char):
                return dest_char


        logging.info(sys.stderr, "Invalid input after EXT %s" % (hex(i)))
        return None
    

    def handle_atr(self, i):

        logging.info(sys.stderr, "Handling ATR:",)
        if i in ISCII_SCRIPTS.keys():
            self.set_script(ISCII_SCRIPTS[i])
            logging.info(sys.stderr, "setting script to", i)
        else:
            # ignore all other ATR markers
            logging.info(sys.stderr, "ignored")
            pass
        
        self.pos += 2 # for ATR and the following char
        
        return None

    def handle_inv(self, i):

        if i == ISCII_HALANT:
            ret = 0x0020
        else:
            ret = ZWJ

        self.pos += 1 # for INV

        return ret
        

    def post_analysis(self, prev_char, src_char):
        ret = None
        if prev_char == ISCII_ATR:
            ret = self.handle_atr(src_char)
                
        elif prev_char == ISCII_EXT:
                
            ret = self.handle_ext(src_char)
            
        elif prev_char == ISCII_INV:
            
            ret = self.handle_inv(src_char)
            
        return ret



    def iscii2utf8(self, src, flush = 0):

        dest = self.dest
        src = array.array('B', src).tolist()

        
        curr_char = prev_char = NO_CHAR
        n = len(src)
        self.pos = 0

        stat = self.stat
        
        for i in range(n):
            curr_char = src[i]
            dest_char = NO_CHAR
            add_prev = 0
            
            if invalid_chars[self.curr_script][curr_char]:
                # just ignore the invalid iscii characters
                logging.info(sys.stderr, 'ignoring invalid iscii char',
                      hex(curr_char))
                self.pos += 1
                continue
            
            if flush and (i == (n - 1)):
                dest_char = curr_char
            
            elif (prev_char == NO_CHAR):
                prev_char = curr_char
                continue
            
            elif prev_char in ISCII_SPECIALS:
                ret = self.post_analysis(prev_char, curr_char)

                if ret is not None:
                    dest_char = ret
                    
                prev_char = NO_CHAR

            elif not iscii_modifying[curr_char]:
                pass
                
            elif curr_char in ISCII_SPECIALS:
                dest_char = prev_char
                prev_char = curr_char
            
            elif (curr_char == ISCII_DANDA) and (prev_char == ISCII_DANDA):
                dest_char = DOUBLE_DANDA
                prev_char = NO_CHAR
                self.pos += 1
                    
            elif (curr_char == ISCII_HALANT) and (prev_char == ISCII_HALANT):
                dest_char = ZWNJ
                add_prev = 1

            elif curr_char == ISCII_NUKTA:
                if prev_char == ISCII_HALANT:
                    dest_char = ZWJ
                    add_prev = 1

                else:
                    tmp = self.is_nukta_special(prev_char)
                    
                    if tmp: # nukta special
                        dest_char = tmp
                        prev_char = NO_CHAR
                        self.pos += 1

            to_add = []
            
            if add_prev == 1:
                to_add.append(prev_char)
                prev_char = NO_CHAR
                              
            if dest_char != NO_CHAR:
                to_add.append(dest_char)

            elif prev_char != NO_CHAR:
                to_add.append(prev_char)
                prev_char = curr_char

            for ch in to_add:
                if (ch <= 0xFF):
                    m = script_maps[self.curr_script][ch]
                else:
                    m = ch

                    # end of mapping
                    
                self.pos += 1
                self.dest.append(m)


        return self.pos
    

def show_usage(name):
    usage = """
    Usage:

    %s script

    where script is a number between 1-9

    1 - devnag
    2 - bengali / assamese
    3 - punjabi
    4 - gujarati
    5 - oriya
    6 - tamil
    7 - telugu
    8 - kannada
    9 - malayalam

    the program reads from stdin and writes to stdout

    any msgs to the user (error msgs etc) are printed on stderr
    """ % (name)
    
    logging.info(sys.stderr,  usage)
    sys.exit(1)


chunk_size = 4096

if __name__ == '__main__':

    i = 0
    try:
        
        i = int(sys.argv[1])
        
        if i not in range(1, 10):
            raise ValueError
    
    except (ValueError, IndexError):
        show_usage(sys.argv[0])
    
    mypar = Parser()
    mypar.set_script(i)

    y = ''
    flush = 0
    
    while 1:
        
        if flush:
            break
        
        x = sys.stdin.read(chunk_size)
        
        if not x:
            flush = 1

        x = y + x
        
        n = mypar.iscii2utf8(x, flush)
        y = x[n:]

        mypar.write_output()
