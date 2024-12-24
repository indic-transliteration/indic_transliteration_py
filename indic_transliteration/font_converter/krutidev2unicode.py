import sys
import re
import argparse

__author__      = ["Nehal J Wani, Raveesh Motlani"]
__copyright__   = "Copyright 2015, Language Techonology Research Center, IIIT Hyderabad"
__maintainer__  = "Nehal J Wani"
__email__       = "nehaljw.kkd1@gmail.com"

k2u = [
   ('\xf1', '\u0970'),  #  ñ  ->  ॰
   ('Q+Z', 'QZ+'),  #  Q+Z  ->  QZ+
   ('sas', 'sa'),  #  sas  ->  sa
   ('aa', 'a'),  #  aa  ->  a
   (')Z', '\u0930\u094d\u0926\u094d\u0927'),  #  )Z  ->  र्द्ध
   ('ZZ', 'Z'),  #  ZZ  ->  Z
   ('\u2018', '"'),  #  ‘  ->  "
   ('\u2019', '"'),  #  ’  ->  "
   ('\u201c', u"'"),  #  “  ->  '
   ('\u201d', u"'"),  #  ”  ->  '
   ('\xe5', '\u0966'),  #  å  ->  ०
   ('\u0192', '\u0967'),  #  ƒ  ->  १
   ('\u201e', '\u0968'),  #  „  ->  २
   ('\u2026', '\u0969'),  #  …  ->  ३
   ('\u2020', '\u096a'),  #  †  ->  ४
   ('\u2021', '\u096b'),  #  ‡  ->  ५
   ('\u02c6', '\u096c'),  #  ˆ  ->  ६
   ('\u2030', '\u096d'),  #  ‰  ->  ७
   ('\u0160', '\u096e'),  #  Š  ->  ८
   ('\u2039', '\u096f'),  #  ‹  ->  ९
   ('\xb6+', '\u095e\u094d'),  #  ¶+  ->  फ़्
   ('d+', '\u0958'),  #  d+  ->  क़
   ('[+k', '\u0959'),  #  [+k  ->  ख़
   ('[+', '\u0959\u094d'),  #  [+  ->  ख़्
   ('x+', '\u095a'),  #  x+  ->  ग़
   ('T+', '\u091c\u093c\u094d'),  #  T+  ->  ज़्
   ('t+', '\u095b'),  #  t+  ->  ज़
   ('M+', '\u095c'),  #  M+  ->  ड़
   ('<+', '\u095d'),  #  <+  ->  ढ़
   ('Q+', '\u095e'),  #  Q+  ->  फ़
   (';+', '\u095f'),  #  ;+  ->  य़
   ('j+', '\u0931'),  #  j+  ->  ऱ
   ('u+', '\u0929'),  #  u+  ->  ऩ
   ('\xd9k', '\u0924\u094d\u0924'),  #  Ùk  ->  त्त
   ('\xd9', '\u0924\u094d\u0924\u094d'),  #  Ù  ->  त्त्
   ('\xe4', '\u0915\u094d\u0924'),  #  ä  ->  क्त
   ('\u2013', '\u0926\u0943'),  #  –  ->  दृ
   ('\u2014', '\u0915\u0943'),  #  —  ->  कृ
   ('\xe9', '\u0928\u094d\u0928'),  #  é  ->  न्न
   ('\u2122', '\u0928\u094d\u0928\u094d'),  #  ™  ->  न्न्
   ('=kk', '=k'),  #  =kk  ->  =k
   ('f=k', 'f='),  #  f=k  ->  f=
   ('\xe0', '\u0939\u094d\u0928'),  #  à  ->  ह्न
   ('\xe1', '\u0939\u094d\u092f'),  #  á  ->  ह्य
   ('\xe2', '\u0939\u0943'),  #  â  ->  हृ
   ('\xe3', '\u0939\u094d\u092e'),  #  ã  ->  ह्म
   ('\xbaz', '\u0939\u094d\u0930'),  #  ºz  ->  ह्र
   ('\xba', '\u0939\u094d'),  #  º  ->  ह्
   ('\xed', '\u0926\u094d\u0926'),  #  í  ->  द्द
   ('{k', '\u0915\u094d\u0937'),  #  {k  ->  क्ष
   ('{', '\u0915\u094d\u0937\u094d'),  #  {  ->  क्ष्
   ('=', '\u0924\u094d\u0930'),  #  =  ->  त्र
   ('\xab', '\u0924\u094d\u0930\u094d'),  #  «  ->  त्र्
   ('N\xee', '\u091b\u094d\u092f'),  #  Nî  ->  छ्य
   ('V\xee', '\u091f\u094d\u092f'),  #  Vî  ->  ट्य
   ('B\xee', '\u0920\u094d\u092f'),  #  Bî  ->  ठ्य
   ('M\xee', '\u0921\u094d\u092f'),  #  Mî  ->  ड्य
   ('<\xee', '\u0922\u094d\u092f'),  #  <î  ->  ढ्य
   ('|', '\u0926\u094d\u092f'),  #  |  ->  द्य
   ('K', '\u091c\u094d\u091e'),  #  K  ->  ज्ञ
   ('}', '\u0926\u094d\u0935'),  #  }  ->  द्व
   ('J', '\u0936\u094d\u0930'),  #  J  ->  श्र
   ('V\xaa', '\u091f\u094d\u0930'),  #  Vª  ->  ट्र
   ('M\xaa', '\u0921\u094d\u0930'),  #  Mª  ->  ड्र
   ('<\xaa\xaa', '\u0922\u094d\u0930'),  #  <ªª  ->  ढ्र
   ('N\xaa', '\u091b\u094d\u0930'),  #  Nª  ->  छ्र
   ('\xd8', '\u0915\u094d\u0930'),  #  Ø  ->  क्र
   ('\xdd', '\u092b\u094d\u0930'),  #  Ý  ->  फ्र
   ('nzZ', '\u0930\u094d\u0926\u094d\u0930'),  #  nzZ  ->  र्द्र
   ('\xe6', '\u0926\u094d\u0930'),  #  æ  ->  द्र
   ('\xe7', '\u092a\u094d\u0930'),  #  ç  ->  प्र
   ('\xc1', '\u092a\u094d\u0930'),  #  Á  ->  प्र
   ('xz', '\u0917\u094d\u0930'),  #  xz  ->  ग्र
   ('#', '\u0930\u0941'),  #  #  ->  रु
   (':', '\u0930\u0942'),  #  :  ->  रू
   ('v\u201a', '\u0911'),  #  v‚  ->  ऑ
   ('vks', '\u0913'),  #  vks  ->  ओ
   ('vkS', '\u0914'),  #  vkS  ->  औ
   ('vk', '\u0906'),  #  vk  ->  आ
   ('v', '\u0905'),  #  v  ->  अ
   ('b\xb1', '\u0908\u0902'),  #  b±  ->  ईं
   ('\xc3', '\u0908'),  #  Ã  ->  ई
   ('bZ', '\u0908'),  #  bZ  ->  ई
   ('b', '\u0907'),  #  b  ->  इ
   ('m', '\u0909'),  #  m  ->  उ
   ('\xc5', '\u090a'),  #  Å  ->  ऊ
   (',s', '\u0910'),  #  ,s  ->  ऐ
   (',', '\u090f'),  #  ,  ->  ए
   ('_', '\u090b'),  #  _  ->  ऋ
   ('\xf4', '\u0915\u094d\u0915'),  #  ô  ->  क्क
   ('d', '\u0915'),  #  d  ->  क
   ('Dk', '\u0915'),  #  Dk  ->  क
   ('D', '\u0915\u094d'),  #  D  ->  क्
   ('[k', '\u0916'),  #  [k  ->  ख
   ('[', '\u0916\u094d'),  #  [  ->  ख्
   ('x', '\u0917'),  #  x  ->  ग
   ('Xk', '\u0917'),  #  Xk  ->  ग
   ('X', '\u0917\u094d'),  #  X  ->  ग्
   ('\xc4', '\u0918'),  #  Ä  ->  घ
   ('?k', '\u0918'),  #  ?k  ->  घ
   ('?', '\u0918\u094d'),  #  ?  ->  घ्
   ('\xb3', '\u0919'),  #  ³  ->  ङ
   ('pkS', '\u091a\u0948'),  #  pkS  ->  चै
   ('p', '\u091a'),  #  p  ->  च
   ('Pk', '\u091a'),  #  Pk  ->  च
   ('P', '\u091a\u094d'),  #  P  ->  च्
   ('N', '\u091b'),  #  N  ->  छ
   ('t', '\u091c'),  #  t  ->  ज
   ('Tk', '\u091c'),  #  Tk  ->  ज
   ('T', '\u091c\u094d'),  #  T  ->  ज्
   ('>', '\u091d'),  #  >  ->  झ
   ('\xf7', '\u091d\u094d'),  #  ÷  ->  झ्
   ('\xa5', '\u091e'),  #  ¥  ->  ञ
   ('\xea', '\u091f\u094d\u091f'),  #  ê  ->  ट्ट
   ('\xeb', '\u091f\u094d\u0920'),  #  ë  ->  ट्ठ
   ('V', '\u091f'),  #  V  ->  ट
   ('B', '\u0920'),  #  B  ->  ठ
   ('\xec', '\u0921\u094d\u0921'),  #  ì  ->  ड्ड
   ('\xef', '\u0921\u094d\u0922'),  #  ï  ->  ड्ढ
   ('M+', '\u0921\u093c'),  #  M+  ->  ड़
   ('<+', '\u0922\u093c'),  #  <+  ->  ढ़
   ('M', '\u0921'),  #  M  ->  ड
   ('<', '\u0922'),  #  <  ->  ढ
   ('.k', '\u0923'),  #  .k  ->  ण
   ('.', '\u0923\u094d'),  #  .  ->  ण्
   ('r', '\u0924'),  #  r  ->  त
   ('Rk', '\u0924'),  #  Rk  ->  त
   ('R', '\u0924\u094d'),  #  R  ->  त्
   ('Fk', '\u0925'),  #  Fk  ->  थ
   ('F', '\u0925\u094d'),  #  F  ->  थ्
   (')', '\u0926\u094d\u0927'),  #  )  ->  द्ध
   ('n', '\u0926'),  #  n  ->  द
   ('/k', '\u0927'),  #  /k  ->  ध
#   ('\xe8k', '\u0927'),  #  èk  ->  ध
   ('/', '\u0927\u094d'),  #  /  ->  ध्
   ('\xcb', '\u0927\u094d'),  #  Ë  ->  ध्
#   ('\xe8', '\u0927\u094d'),  #  è  ->  ध्
   ('\xe8', '\u0927'),  #  è  ->  ध
   ('u', '\u0928'),  #  u  ->  न
   ('Uk', '\u0928'),  #  Uk  ->  न
   ('U', '\u0928\u094d'),  #  U  ->  न्
   ('i', '\u092a'),  #  i  ->  प
   ('Ik', '\u092a'),  #  Ik  ->  प
   ('I', '\u092a\u094d'),  #  I  ->  प्
   ('Q', '\u092b'),  #  Q  ->  फ
   ('\xb6', '\u092b\u094d'),  #  ¶  ->  फ्
   ('c', '\u092c'),  #  c  ->  ब
   ('Ck', '\u092c'),  #  Ck  ->  ब
   ('C', '\u092c\u094d'),  #  C  ->  ब्
   ('Hk', '\u092d'),  #  Hk  ->  भ
   ('H', '\u092d\u094d'),  #  H  ->  भ्
   ('e', '\u092e'),  #  e  ->  म
   ('Ek', '\u092e'),  #  Ek  ->  म
   ('E', '\u092e\u094d'),  #  E  ->  म्
   (';', '\u092f'),  #  ;  ->  य
   ('\xb8', '\u092f\u094d'),  #  ¸  ->  य्
   ('j', '\u0930'),  #  j  ->  र
   ('y', '\u0932'),  #  y  ->  ल
   ('Yk', '\u0932'),  #  Yk  ->  ल
   ('Y', '\u0932\u094d'),  #  Y  ->  ल्
   ('G', '\u0933'),  #  G  ->  ळ
   ('o', '\u0935'),  #  o  ->  व
   ('Ok', '\u0935'),  #  Ok  ->  व
   ('O', '\u0935\u094d'),  #  O  ->  व्
   (u"'k", '\u0936'),  #  'k  ->  श
   (u"'", '\u0936\u094d'),  #  '  ->  श्
   ('"k', '\u0937'),  #  "k  ->  ष
   ('"', '\u0937\u094d'),  #  "  ->  ष्
   ('l', '\u0938'),  #  l  ->  स
   ('Lk', '\u0938'),  #  Lk  ->  स
   ('L', '\u0938\u094d'),  #  L  ->  स्
   ('g', '\u0939'),  #  g  ->  ह
   ('\xc8', '\u0940\u0902'),  #  È  ->  ीं
   ('saz', '\u094d\u0930\u0947\u0902'),  #  saz  ->  ्रें
   ('z', '\u094d\u0930'),  #  z  ->  ्र
   ('\xcc', '\u0926\u094d\u0926'),  #  Ì  ->  द्द
   ('\xcd', '\u091f\u094d\u091f'),  #  Í  ->  ट्ट
   ('\xce', '\u091f\u094d\u0920'),  #  Î  ->  ट्ठ
   ('\xcf', '\u0921\u094d\u0921'),  #  Ï  ->  ड्ड
   ('\xd1', '\u0915\u0943'),  #  Ñ  ->  कृ
   ('\xd2', '\u092d'),  #  Ò  ->  भ
   ('\xd3', '\u094d\u092f'),  #  Ó  ->  ्य
   ('\xd4', '\u0921\u094d\u0922'),  #  Ô  ->  ड्ढ
   ('\xd6', '\u091d\u094d'),  #  Ö  ->  झ्
   ('\xd8', '\u0915\u094d\u0930'),  #  Ø  ->  क्र
   ('\xd9', '\u0924\u094d\u0924\u094d'),  #  Ù  ->  त्त्
   ('\xdck', '\u0936'),  #  Ük  ->  श
   ('\xdc', '\u0936\u094d'),  #  Ü  ->  श्
   ('\u201a', '\u0949'),  #  ‚  ->  ॉ
   ('kas', '\u094b\u0902'),  #  kas  ->  ों
   ('ks', '\u094b'),  #  ks  ->  ो
   ('kS', '\u094c'),  #  kS  ->  ौ
   ('\xa1k', '\u093e\u0901'),  #  ¡k  ->  ाँ'
   ('ak', 'k\u0902'),  #  ak  ->  k +  ं
   ('k', '\u093e'),  #  k  ->  ा
   ('ah', '\u0940\u0902'),  #  ah  ->  ीं
   ('h', '\u0940'),  #  h  ->  ी
   ('aq', '\u0941\u0902'),  #  aq  ->   ुं
   ('q', '\u0941'),  #  q  ->  ु
   ('aw', '\u0942\u0902'),  #  aw  ->  ूं
   ('\xa1w', '\u0942\u0901'),  #  ¡w  ->  ूँ
   ('w', '\u0942'),  #  w  ->  ू
   ('`', '\u0943'),  #  `  ->  ृ
   ('\u0300', '\u0943'),  #  ̀  ->  ृ
   ('as', '\u0947\u0902'),  #  as  ->  ें
   ('\xb1s', 's\xb1'), #  ±s  ->  s±
   ('s', '\u0947'),  #  s  ->  े
   ('aS', '\u0948\u0902'),  #  aS  ->  ैं
   ('S', '\u0948'),  #  S  ->  ै
   ('a\xaa', '\u094d\u0930\u0902'), #  aª  ->  ्र + ं
   ('\xaa', '\u094d\u0930'), #  ª  ->  ्र
   ('fa', '\u0902f'),  #  fa  ->  ं  + f
   ('a', '\u0902'),  #  a  ->  ं
   ('\xa1', '\u0901'),  #  ¡  ->  ँ
   ('%', ':'),  #  %  ->  :
   ('W', '\u0945'),  #  W  ->  ॅ
   ('\u2022', '\u093d'),  #  •  ->  ऽ
   ('\xb7', '\u093d'),  #  ·  ->  ऽ
   ('\u2219', '\u093d'),  #  ∙  ->  ऽ
   ('\xb7', '\u093d'),  #  ·  ->  ऽ
   ('~j', '\u094d\u0930'),  #  ~j  ->  ्र
   ('~', '\u094d'),  #  ~  ->  ्
   ('\\', '?'),  #  \  ->  ?
   ('+', '\u093c'),  #  +  ->  ़
   ('^', '\u2018'),  #  ^  ->  ‘
   ('*', '\u2019'),  #  *  ->  ’
   ('\xde', '\u201c'),  #  Þ  ->  “
   ('\xdf', '\u201d'),  #  ß  ->  ”
   ('(', ';'),  #  (  ->  ;
   ('\xbc', '('),  #  ¼  ->  (
   ('\xbd', ')'),  #  ½  ->  )
   ('\xbf', '{'),  #  ¿  ->  {
   ('\xc0', '}'),  #  À  ->  }
   ('\xbe', '='),  #  ¾  ->  =
   ('A', '\u0964'),  #  A  ->  ।
   ('-', '.'),  #  -  ->  .
   ('&', '-'),  #  &  ->  -
   ('&', '\xb5'),  #  &  ->  µ
   ('\u03bc', '-'),  #  μ  ->  -
   ('\u0152', '\u0970'),  #  Œ  ->  ॰
   (']', ','),  #  ]  ->  ,
   ('~ ', '\u094d '),  #  ~  ->  ् 
   ('@', '/'),  #  @  ->  /
   ('\xae', '\u0948\u0902'), #  ®  ->  ैं
#   ('%', '\u0903'),  #  %  ->  ः
#   (' \u0903', ':'),  #   ः  ->  :
#   ('\xc7', '\u093f\u0902'), #  Ç  ->  िं
#   ('\xca', '\u0940Z'), #  Ê  ->  ीZ
#   ('Z', '\u0930\u094d'), #  Z  ->  र्
#   ('f', '\u093f'), #  f  ->  ि
#   ('\xb1', 'Z\u0902'), #  ±  ->  Zं
#   ('\xc6', '\u0930\u094d\u093f'), #  Æ  ->  र्ि
#   ('\xc9', '\u0930\u094d\u093f\u0902'),  #  É  ->  र्ि'
]

unicode_vowel_signs = [
   '\u0905', #  अ
   '\u0906', #  आ
   '\u0907', #  इ
   '\u0908', #  ई
   '\u0909', #  उ
   '\u090a', #  ऊ
   '\u090f', #  ए
   '\u0910', #  ऐ
   '\u0913', #  ओ
   '\u0914', #  औ
   '\u093e', #  ा
   '\u093f', #  ि
   '\u0940', #  ी
   '\u0941', #  ु
   '\u0942', #  ू
   '\u0943', #  ृ
   '\u0947', #  े
   '\u0948', #  ै
   '\u094b', #  ो
   '\u094c', #  ौ
   '\u0902', #  ं
   '\u0903', #  ः
   '\u0901', #  ँ
   '\u0945', #  ॅ
]

unicode_unattached_vowel_signs = [
   '\u093e', #  ा
   '\u093f', #  ि
   '\u0940', #  ी
   '\u0941', #  ु
   '\u0942', #  ू
   '\u0943', #  ृ
   '\u0947', #  े
   '\u0948', #  ै
   '\u094b', #  ो
   '\u094c', #  ौ
   '\u0902', #  ं
   '\u0903', #  ः
   '\u0901', #  ँ
   '\u0945', #  ॅ
]

unicode_consonants = [
   '\u0915', # क
   '\u0916', # ख
   '\u0917', # ग
   '\u0918', # घ
   '\u0919', # ङ
   '\u091a', # च
   '\u091b', # छ
   '\u091c', # ज
   '\u091d', # झ
   '\u091e', # ञ
   '\u091f', # ट
   '\u0920', # ठ
   '\u0921', # ड
   '\u0922', # ढ
   '\u0923', # ण
   '\u0924', # त
   '\u0925', # थ
   '\u0926', # द
   '\u0927', # ध
   '\u0928', # न
   '\u0929', # ऩ
   '\u092a', # प
   '\u092b', # फ
   '\u092c', # ब
   '\u092d', # भ
   '\u092e', # म
   '\u092f', # य
   '\u0930', # र
   '\u0931', # ऱ
   '\u0932', # ल
   '\u0933', # ळ
   '\u0934', # ऴ
   '\u0935', # व
   '\u0936', # श
   '\u0937', # ष
   '\u0938', # स
   '\u0939', # ह
   '\u0958', # क़
   '\u0959', # ख़
   '\u095a', # ग़
   '\u095b', # ज़
   '\u095c', # ड़
   '\u095d', # ढ़
   '\u095e', # फ़
   '\u095f', # य़
]

krutidev_consonants = [
   'd', # क
   '[k', # ख
   'x', # ग
   '?k', # घ
   '\xb3', # ङ
   'p', # च
   'N', # छ
   't', # ज
   '>', # झ
   '\xa5', # ञ
   'V', # ट
   'B', # ठ
   'M', # ड
   '<', # ढ
   '.k', # ण
   'r', # त
   'Fk', # थ
   'n', # द
   '/k', # ध
   'u', # न
   'Uk', # ऩ
   'i', # प
   'Q', # फ
   'c', # ब
   'Hk', # भ
   'e', # म
   ';', # य
   'j', # र
   'j', # ऱ
   'y', # ल
   'G', # ळ
   '\u0934', # ऴ
   'o', # व
   "'k" , # श
   '"k', # ष
   'l', # स
   'g', # ह
   'd', # क़
   '[k', # ख़
   'x', # ग़
   't', # ज़
   'M+', # ड़
   '<+', # ढ़
   'Q', # फ़
   ';', # य़
   'D',  # क्
   '[',  # ख्
   'X',  # ग्
   '?',  # घ्
   '\xb3~',  # ङ्
   'P',  # च्
   'N~',  # छ्
   'T',  # ज्
   '÷',  # झ्
   '\xa5~',  # ञ्
   'V~',  # ट्
   'B~',  # ठ्
   'M~',  # ड्
   '<~',  # ढ्
   '.',  # ण्
   'R',  # त्
   'F',  # थ्
   'n~',  # द्
   '/',  # ध्
   'Ë',  # ध्
   'è',  # ध्
   'U',  # न्
   'I',  # प्
   '¶',  # फ्
   'C',  # ब्
   'H',  # भ्
   'E',  # म्
   '\xb8',  # य्
   'Z',  # र्
   'Y',  # ल्
   'O',  # व्
   u"'",  # श्
   u"Ü",  # श्
   '"',  # ष्
   'L',  # स्
   '\xba',  # ह्
]

krutidev_unattached_vowel_signs = [
   'k', # ा
   'f', # ि
   'h', # ी
   'q', # ु
   'w', # ू
   '`', # ृ
   's', # े
   'S', # ै
   'ks', # ो
   'kS', # ौ
   'a', # ं
   '%', # ः
   '\xa1', # ँ
   'W', # ॅ
]

def getUnicode(unk_txt):
    try:
        return unk_txt.decode('utf-8')
    except UnicodeDecodeError:
        return unk_txt.decode('unicode_escape')

def kru2uni(kru_text):
    """Convert the KrutiDev text to Unicode text.

    Args:
        kru_text: Text in KrutiDev.
    Returns:
        Text converted into Unicode.

    NOTE :  The assumption is that the input text is 100% Krutidev. If it
            contains any other Latin characters, then they will be converted
            according to the KrutiDev 2 Unicode mapping.
            Example:
            "(i) egkfuns'kky; dh osclkbV (www.shipping.gov.in) ij gS"
            will become...
            ";पद्ध महानिदेशालय की वेबसाइट ;ूूूणेीपचचपदहण्हवअण्पदद्ध पर है"

            Therefore, check the input text before passing it to this function.

    """
    kru_text = getUnicode(kru_text)

    # space +  ्र  ->   ्र
    kru_text = kru_text.replace(' \xaa', '\xaa')
    kru_text = kru_text.replace(' ~j', '~j')
    kru_text = kru_text.replace(' z', 'z')

    # – and — if not surrounded by krutidev consonants/matrās, change them to -
    misplaced = re.compile('[\u2014\u2013]')
    for m in misplaced.finditer(kru_text):
        index = m.start()
        if index < len(kru_text) - 1 and kru_text[m.start() + 1] not in krutidev_consonants + krutidev_unattached_vowel_signs:
            kru_text = kru_text[ : index] + '&' + kru_text[index + 1 : ]

    for mapping in k2u:
        kru_text = kru_text.replace(mapping[0], mapping[1])

    kru_text = kru_text.replace('\xb1', 'Z\u0902') #  ±  ->  Zं
    kru_text = kru_text.replace('\xc6', '\u0930\u094df') #  Æ  ->  र्f

    #  f + ?  ->  ? + ि
    misplaced = re.search('f(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('f' + misplaced, misplaced + '\u093f')
        misplaced = re.search('f(.?)', kru_text)

    kru_text = kru_text.replace('\xc7', 'fa') #  Ç  ->  fa
    kru_text = kru_text.replace('\xaf', 'fa') #  ¯  ->  fa
    kru_text = kru_text.replace('\xc9', '\u0930\u094dfa') #  É  ->  र्fa

    #  fa?  ->  ? + िं
    misplaced = re.search('fa(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('fa' + misplaced, misplaced + '\u093f\u0902')
        misplaced = re.search('fa(.?)', kru_text)

    kru_text = kru_text.replace('\xca', '\u0940Z') #  Ê  ->  ीZ

    #  ि्  + ?  ->  ्  + ? + ि
    misplaced = re.search('\u093f\u094d(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('\u093f\u094d' + misplaced, '\u094d' + misplaced + '\u093f')
        misplaced = re.search('\u093f\u094d(.?)', kru_text)

    kru_text = kru_text.replace('\u094dZ', 'Z') #  ्  + Z ->  Z

    # र +  ्  should be placed at the right place, before matrās
    misplaced = re.search('(.?)Z', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        index_r_halant = kru_text.index(misplaced + 'Z')
        while index_r_halant > 0 and kru_text[index_r_halant] in unicode_vowel_signs:
            index_r_halant -= 1
            misplaced = kru_text[index_r_halant] + misplaced
        kru_text = kru_text.replace(misplaced + 'Z', '\u0930\u094d' + misplaced)
        misplaced = re.search('(.?)Z', kru_text)

    # ' ', ',' and ्  are illegal characters just before a matrā
    for matra in unicode_unattached_vowel_signs:
        kru_text = kru_text.replace(' ' + matra, matra)
        kru_text = kru_text.replace(',' + matra, matra + ',')
        kru_text = kru_text.replace('\u094d' + matra, matra)

    kru_text = kru_text.replace('\u094d\u094d\u0930', '\u094d\u0930')  #  ्  + ्  + र ->  ्  + र
    kru_text = kru_text.replace('\u094d\u0930\u094d', '\u0930\u094d')  #  ्  + र + ्  ->  र + ्

    kru_text = kru_text.replace('\u094d\u094d', '\u094d') #  ्  + ्  ->  ्

    # ्  at the ending of a consonant as the last character is illegal.
    # Uncomment, if input is Sanskrit
    kru_text = kru_text.replace('\u094d ', ' ')

    return kru_text.encode('utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Krutidev2Unicode Font Convertor')
    parser.add_argument('-i', '--input', type = argparse.FileType('r'), dest = 'input_file', help = 'Input File', default = sys.stdin)
    parser.add_argument('-o', '--output', type = argparse.FileType('w'), dest = 'output_file', help = 'Output File', default = sys.stdout)
    args = parser.parse_args()

    for line in args.input_file:
        args.output_file.write(kru2uni(line))