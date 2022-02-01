import sys
import re
import argparse

__author__      = ["Nehal J Wani, Raveesh Motlani"]
__copyright__   = "Copyright 2015, Language Techonology Research Center, IIIT Hyderabad"
__maintainer__  = "Nehal J Wani"
__email__       = "nehaljw.kkd1@gmail.com"

k2u = [
   (u'\xf1', u'\u0970'),  #  ñ  ->  ॰
   (u'Q+Z', u'QZ+'),  #  Q+Z  ->  QZ+
   (u'sas', u'sa'),  #  sas  ->  sa
   (u'aa', u'a'),  #  aa  ->  a
   (u')Z', u'\u0930\u094d\u0926\u094d\u0927'),  #  )Z  ->  र्द्ध
   (u'ZZ', u'Z'),  #  ZZ  ->  Z
   (u'\u2018', u'"'),  #  ‘  ->  "
   (u'\u2019', u'"'),  #  ’  ->  "
   (u'\u201c', u"'"),  #  “  ->  '
   (u'\u201d', u"'"),  #  ”  ->  '
   (u'\xe5', u'\u0966'),  #  å  ->  ०
   (u'\u0192', u'\u0967'),  #  ƒ  ->  १
   (u'\u201e', u'\u0968'),  #  „  ->  २
   (u'\u2026', u'\u0969'),  #  …  ->  ३
   (u'\u2020', u'\u096a'),  #  †  ->  ४
   (u'\u2021', u'\u096b'),  #  ‡  ->  ५
   (u'\u02c6', u'\u096c'),  #  ˆ  ->  ६
   (u'\u2030', u'\u096d'),  #  ‰  ->  ७
   (u'\u0160', u'\u096e'),  #  Š  ->  ८
   (u'\u2039', u'\u096f'),  #  ‹  ->  ९
   (u'\xb6+', u'\u095e\u094d'),  #  ¶+  ->  फ़्
   (u'd+', u'\u0958'),  #  d+  ->  क़
   (u'[+k', u'\u0959'),  #  [+k  ->  ख़
   (u'[+', u'\u0959\u094d'),  #  [+  ->  ख़्
   (u'x+', u'\u095a'),  #  x+  ->  ग़
   (u'T+', u'\u091c\u093c\u094d'),  #  T+  ->  ज़्
   (u't+', u'\u095b'),  #  t+  ->  ज़
   (u'M+', u'\u095c'),  #  M+  ->  ड़
   (u'<+', u'\u095d'),  #  <+  ->  ढ़
   (u'Q+', u'\u095e'),  #  Q+  ->  फ़
   (u';+', u'\u095f'),  #  ;+  ->  य़
   (u'j+', u'\u0931'),  #  j+  ->  ऱ
   (u'u+', u'\u0929'),  #  u+  ->  ऩ
   (u'\xd9k', u'\u0924\u094d\u0924'),  #  Ùk  ->  त्त
   (u'\xd9', u'\u0924\u094d\u0924\u094d'),  #  Ù  ->  त्त्
   (u'\xe4', u'\u0915\u094d\u0924'),  #  ä  ->  क्त
   (u'\u2013', u'\u0926\u0943'),  #  –  ->  दृ
   (u'\u2014', u'\u0915\u0943'),  #  —  ->  कृ
   (u'\xe9', u'\u0928\u094d\u0928'),  #  é  ->  न्न
   (u'\u2122', u'\u0928\u094d\u0928\u094d'),  #  ™  ->  न्न्
   (u'=kk', u'=k'),  #  =kk  ->  =k
   (u'f=k', u'f='),  #  f=k  ->  f=
   (u'\xe0', u'\u0939\u094d\u0928'),  #  à  ->  ह्न
   (u'\xe1', u'\u0939\u094d\u092f'),  #  á  ->  ह्य
   (u'\xe2', u'\u0939\u0943'),  #  â  ->  हृ
   (u'\xe3', u'\u0939\u094d\u092e'),  #  ã  ->  ह्म
   (u'\xbaz', u'\u0939\u094d\u0930'),  #  ºz  ->  ह्र
   (u'\xba', u'\u0939\u094d'),  #  º  ->  ह्
   (u'\xed', u'\u0926\u094d\u0926'),  #  í  ->  द्द
   (u'{k', u'\u0915\u094d\u0937'),  #  {k  ->  क्ष
   (u'{', u'\u0915\u094d\u0937\u094d'),  #  {  ->  क्ष्
   (u'=', u'\u0924\u094d\u0930'),  #  =  ->  त्र
   (u'\xab', u'\u0924\u094d\u0930\u094d'),  #  «  ->  त्र्
   (u'N\xee', u'\u091b\u094d\u092f'),  #  Nî  ->  छ्य
   (u'V\xee', u'\u091f\u094d\u092f'),  #  Vî  ->  ट्य
   (u'B\xee', u'\u0920\u094d\u092f'),  #  Bî  ->  ठ्य
   (u'M\xee', u'\u0921\u094d\u092f'),  #  Mî  ->  ड्य
   (u'<\xee', u'\u0922\u094d\u092f'),  #  <î  ->  ढ्य
   (u'|', u'\u0926\u094d\u092f'),  #  |  ->  द्य
   (u'K', u'\u091c\u094d\u091e'),  #  K  ->  ज्ञ
   (u'}', u'\u0926\u094d\u0935'),  #  }  ->  द्व
   (u'J', u'\u0936\u094d\u0930'),  #  J  ->  श्र
   (u'V\xaa', u'\u091f\u094d\u0930'),  #  Vª  ->  ट्र
   (u'M\xaa', u'\u0921\u094d\u0930'),  #  Mª  ->  ड्र
   (u'<\xaa\xaa', u'\u0922\u094d\u0930'),  #  <ªª  ->  ढ्र
   (u'N\xaa', u'\u091b\u094d\u0930'),  #  Nª  ->  छ्र
   (u'\xd8', u'\u0915\u094d\u0930'),  #  Ø  ->  क्र
   (u'\xdd', u'\u092b\u094d\u0930'),  #  Ý  ->  फ्र
   (u'nzZ', u'\u0930\u094d\u0926\u094d\u0930'),  #  nzZ  ->  र्द्र
   (u'\xe6', u'\u0926\u094d\u0930'),  #  æ  ->  द्र
   (u'\xe7', u'\u092a\u094d\u0930'),  #  ç  ->  प्र
   (u'\xc1', u'\u092a\u094d\u0930'),  #  Á  ->  प्र
   (u'xz', u'\u0917\u094d\u0930'),  #  xz  ->  ग्र
   (u'#', u'\u0930\u0941'),  #  #  ->  रु
   (u':', u'\u0930\u0942'),  #  :  ->  रू
   (u'v\u201a', u'\u0911'),  #  v‚  ->  ऑ
   (u'vks', u'\u0913'),  #  vks  ->  ओ
   (u'vkS', u'\u0914'),  #  vkS  ->  औ
   (u'vk', u'\u0906'),  #  vk  ->  आ
   (u'v', u'\u0905'),  #  v  ->  अ
   (u'b\xb1', u'\u0908\u0902'),  #  b±  ->  ईं
   (u'\xc3', u'\u0908'),  #  Ã  ->  ई
   (u'bZ', u'\u0908'),  #  bZ  ->  ई
   (u'b', u'\u0907'),  #  b  ->  इ
   (u'm', u'\u0909'),  #  m  ->  उ
   (u'\xc5', u'\u090a'),  #  Å  ->  ऊ
   (u',s', u'\u0910'),  #  ,s  ->  ऐ
   (u',', u'\u090f'),  #  ,  ->  ए
   (u'_', u'\u090b'),  #  _  ->  ऋ
   (u'\xf4', u'\u0915\u094d\u0915'),  #  ô  ->  क्क
   (u'd', u'\u0915'),  #  d  ->  क
   (u'Dk', u'\u0915'),  #  Dk  ->  क
   (u'D', u'\u0915\u094d'),  #  D  ->  क्
   (u'[k', u'\u0916'),  #  [k  ->  ख
   (u'[', u'\u0916\u094d'),  #  [  ->  ख्
   (u'x', u'\u0917'),  #  x  ->  ग
   (u'Xk', u'\u0917'),  #  Xk  ->  ग
   (u'X', u'\u0917\u094d'),  #  X  ->  ग्
   (u'\xc4', u'\u0918'),  #  Ä  ->  घ
   (u'?k', u'\u0918'),  #  ?k  ->  घ
   (u'?', u'\u0918\u094d'),  #  ?  ->  घ्
   (u'\xb3', u'\u0919'),  #  ³  ->  ङ
   (u'pkS', u'\u091a\u0948'),  #  pkS  ->  चै
   (u'p', u'\u091a'),  #  p  ->  च
   (u'Pk', u'\u091a'),  #  Pk  ->  च
   (u'P', u'\u091a\u094d'),  #  P  ->  च्
   (u'N', u'\u091b'),  #  N  ->  छ
   (u't', u'\u091c'),  #  t  ->  ज
   (u'Tk', u'\u091c'),  #  Tk  ->  ज
   (u'T', u'\u091c\u094d'),  #  T  ->  ज्
   (u'>', u'\u091d'),  #  >  ->  झ
   (u'\xf7', u'\u091d\u094d'),  #  ÷  ->  झ्
   (u'\xa5', u'\u091e'),  #  ¥  ->  ञ
   (u'\xea', u'\u091f\u094d\u091f'),  #  ê  ->  ट्ट
   (u'\xeb', u'\u091f\u094d\u0920'),  #  ë  ->  ट्ठ
   (u'V', u'\u091f'),  #  V  ->  ट
   (u'B', u'\u0920'),  #  B  ->  ठ
   (u'\xec', u'\u0921\u094d\u0921'),  #  ì  ->  ड्ड
   (u'\xef', u'\u0921\u094d\u0922'),  #  ï  ->  ड्ढ
   (u'M+', u'\u0921\u093c'),  #  M+  ->  ड़
   (u'<+', u'\u0922\u093c'),  #  <+  ->  ढ़
   (u'M', u'\u0921'),  #  M  ->  ड
   (u'<', u'\u0922'),  #  <  ->  ढ
   (u'.k', u'\u0923'),  #  .k  ->  ण
   (u'.', u'\u0923\u094d'),  #  .  ->  ण्
   (u'r', u'\u0924'),  #  r  ->  त
   (u'Rk', u'\u0924'),  #  Rk  ->  त
   (u'R', u'\u0924\u094d'),  #  R  ->  त्
   (u'Fk', u'\u0925'),  #  Fk  ->  थ
   (u'F', u'\u0925\u094d'),  #  F  ->  थ्
   (u')', u'\u0926\u094d\u0927'),  #  )  ->  द्ध
   (u'n', u'\u0926'),  #  n  ->  द
   (u'/k', u'\u0927'),  #  /k  ->  ध
#   (u'\xe8k', u'\u0927'),  #  èk  ->  ध
   (u'/', u'\u0927\u094d'),  #  /  ->  ध्
   (u'\xcb', u'\u0927\u094d'),  #  Ë  ->  ध्
#   (u'\xe8', u'\u0927\u094d'),  #  è  ->  ध्
   (u'\xe8', u'\u0927'),  #  è  ->  ध
   (u'u', u'\u0928'),  #  u  ->  न
   (u'Uk', u'\u0928'),  #  Uk  ->  न
   (u'U', u'\u0928\u094d'),  #  U  ->  न्
   (u'i', u'\u092a'),  #  i  ->  प
   (u'Ik', u'\u092a'),  #  Ik  ->  प
   (u'I', u'\u092a\u094d'),  #  I  ->  प्
   (u'Q', u'\u092b'),  #  Q  ->  फ
   (u'\xb6', u'\u092b\u094d'),  #  ¶  ->  फ्
   (u'c', u'\u092c'),  #  c  ->  ब
   (u'Ck', u'\u092c'),  #  Ck  ->  ब
   (u'C', u'\u092c\u094d'),  #  C  ->  ब्
   (u'Hk', u'\u092d'),  #  Hk  ->  भ
   (u'H', u'\u092d\u094d'),  #  H  ->  भ्
   (u'e', u'\u092e'),  #  e  ->  म
   (u'Ek', u'\u092e'),  #  Ek  ->  म
   (u'E', u'\u092e\u094d'),  #  E  ->  म्
   (u';', u'\u092f'),  #  ;  ->  य
   (u'\xb8', u'\u092f\u094d'),  #  ¸  ->  य्
   (u'j', u'\u0930'),  #  j  ->  र
   (u'y', u'\u0932'),  #  y  ->  ल
   (u'Yk', u'\u0932'),  #  Yk  ->  ल
   (u'Y', u'\u0932\u094d'),  #  Y  ->  ल्
   (u'G', u'\u0933'),  #  G  ->  ळ
   (u'o', u'\u0935'),  #  o  ->  व
   (u'Ok', u'\u0935'),  #  Ok  ->  व
   (u'O', u'\u0935\u094d'),  #  O  ->  व्
   (u"'k", u'\u0936'),  #  'k  ->  श
   (u"'", u'\u0936\u094d'),  #  '  ->  श्
   (u'"k', u'\u0937'),  #  "k  ->  ष
   (u'"', u'\u0937\u094d'),  #  "  ->  ष्
   (u'l', u'\u0938'),  #  l  ->  स
   (u'Lk', u'\u0938'),  #  Lk  ->  स
   (u'L', u'\u0938\u094d'),  #  L  ->  स्
   (u'g', u'\u0939'),  #  g  ->  ह
   (u'\xc8', u'\u0940\u0902'),  #  È  ->  ीं
   (u'saz', u'\u094d\u0930\u0947\u0902'),  #  saz  ->  ्रें
   (u'z', u'\u094d\u0930'),  #  z  ->  ्र
   (u'\xcc', u'\u0926\u094d\u0926'),  #  Ì  ->  द्द
   (u'\xcd', u'\u091f\u094d\u091f'),  #  Í  ->  ट्ट
   (u'\xce', u'\u091f\u094d\u0920'),  #  Î  ->  ट्ठ
   (u'\xcf', u'\u0921\u094d\u0921'),  #  Ï  ->  ड्ड
   (u'\xd1', u'\u0915\u0943'),  #  Ñ  ->  कृ
   (u'\xd2', u'\u092d'),  #  Ò  ->  भ
   (u'\xd3', u'\u094d\u092f'),  #  Ó  ->  ्य
   (u'\xd4', u'\u0921\u094d\u0922'),  #  Ô  ->  ड्ढ
   (u'\xd6', u'\u091d\u094d'),  #  Ö  ->  झ्
   (u'\xd8', u'\u0915\u094d\u0930'),  #  Ø  ->  क्र
   (u'\xd9', u'\u0924\u094d\u0924\u094d'),  #  Ù  ->  त्त्
   (u'\xdck', u'\u0936'),  #  Ük  ->  श
   (u'\xdc', u'\u0936\u094d'),  #  Ü  ->  श्
   (u'\u201a', u'\u0949'),  #  ‚  ->  ॉ
   (u'kas', u'\u094b\u0902'),  #  kas  ->  ों
   (u'ks', u'\u094b'),  #  ks  ->  ो
   (u'kS', u'\u094c'),  #  kS  ->  ौ
   (u'\xa1k', u'\u093e\u0901'),  #  ¡k  ->  ाँ'
   (u'ak', u'k\u0902'),  #  ak  ->  k +  ं
   (u'k', u'\u093e'),  #  k  ->  ा
   (u'ah', u'\u0940\u0902'),  #  ah  ->  ीं
   (u'h', u'\u0940'),  #  h  ->  ी
   (u'aq', u'\u0941\u0902'),  #  aq  ->   ुं
   (u'q', u'\u0941'),  #  q  ->  ु
   (u'aw', u'\u0942\u0902'),  #  aw  ->  ूं
   (u'\xa1w', u'\u0942\u0901'),  #  ¡w  ->  ूँ
   (u'w', u'\u0942'),  #  w  ->  ू
   (u'`', u'\u0943'),  #  `  ->  ृ
   (u'\u0300', u'\u0943'),  #  ̀  ->  ृ
   (u'as', u'\u0947\u0902'),  #  as  ->  ें
   (u'\xb1s', u's\xb1'), #  ±s  ->  s±
   (u's', u'\u0947'),  #  s  ->  े
   (u'aS', u'\u0948\u0902'),  #  aS  ->  ैं
   (u'S', u'\u0948'),  #  S  ->  ै
   (u'a\xaa', u'\u094d\u0930\u0902'), #  aª  ->  ्र + ं
   (u'\xaa', u'\u094d\u0930'), #  ª  ->  ्र
   (u'fa', u'\u0902f'),  #  fa  ->  ं  + f
   (u'a', u'\u0902'),  #  a  ->  ं
   (u'\xa1', u'\u0901'),  #  ¡  ->  ँ
   (u'%', u':'),  #  %  ->  :
   (u'W', u'\u0945'),  #  W  ->  ॅ
   (u'\u2022', u'\u093d'),  #  •  ->  ऽ
   (u'\xb7', u'\u093d'),  #  ·  ->  ऽ
   (u'\u2219', u'\u093d'),  #  ∙  ->  ऽ
   (u'\xb7', u'\u093d'),  #  ·  ->  ऽ
   (u'~j', u'\u094d\u0930'),  #  ~j  ->  ्र
   (u'~', u'\u094d'),  #  ~  ->  ्
   (u'\\', u'?'),  #  \  ->  ?
   (u'+', u'\u093c'),  #  +  ->  ़
   (u'^', u'\u2018'),  #  ^  ->  ‘
   (u'*', u'\u2019'),  #  *  ->  ’
   (u'\xde', u'\u201c'),  #  Þ  ->  “
   (u'\xdf', u'\u201d'),  #  ß  ->  ”
   (u'(', u';'),  #  (  ->  ;
   (u'\xbc', u'('),  #  ¼  ->  (
   (u'\xbd', u')'),  #  ½  ->  )
   (u'\xbf', u'{'),  #  ¿  ->  {
   (u'\xc0', u'}'),  #  À  ->  }
   (u'\xbe', u'='),  #  ¾  ->  =
   (u'A', u'\u0964'),  #  A  ->  ।
   (u'-', u'.'),  #  -  ->  .
   (u'&', u'-'),  #  &  ->  -
   (u'&', u'\xb5'),  #  &  ->  µ
   (u'\u03bc', u'-'),  #  μ  ->  -
   (u'\u0152', u'\u0970'),  #  Œ  ->  ॰
   (u']', u','),  #  ]  ->  ,
   (u'~ ', u'\u094d '),  #  ~  ->  ् 
   (u'@', u'/'),  #  @  ->  /
   (u'\xae', u'\u0948\u0902'), #  ®  ->  ैं
#   (u'%', u'\u0903'),  #  %  ->  ः
#   (u' \u0903', u':'),  #   ः  ->  :
#   (u'\xc7', u'\u093f\u0902'), #  Ç  ->  िं
#   (u'\xca', u'\u0940Z'), #  Ê  ->  ीZ
#   (u'Z', u'\u0930\u094d'), #  Z  ->  र्
#   (u'f', u'\u093f'), #  f  ->  ि
#   (u'\xb1', u'Z\u0902'), #  ±  ->  Zं
#   (u'\xc6', u'\u0930\u094d\u093f'), #  Æ  ->  र्ि
#   (u'\xc9', u'\u0930\u094d\u093f\u0902'),  #  É  ->  र्ि'
]

unicode_vowel_signs = [
   u'\u0905', #  अ
   u'\u0906', #  आ
   u'\u0907', #  इ
   u'\u0908', #  ई
   u'\u0909', #  उ
   u'\u090a', #  ऊ
   u'\u090f', #  ए
   u'\u0910', #  ऐ
   u'\u0913', #  ओ
   u'\u0914', #  औ
   u'\u093e', #  ा
   u'\u093f', #  ि
   u'\u0940', #  ी
   u'\u0941', #  ु
   u'\u0942', #  ू
   u'\u0943', #  ृ
   u'\u0947', #  े
   u'\u0948', #  ै
   u'\u094b', #  ो
   u'\u094c', #  ौ
   u'\u0902', #  ं
   u'\u0903', #  ः
   u'\u0901', #  ँ
   u'\u0945', #  ॅ
]

unicode_unattached_vowel_signs = [
   u'\u093e', #  ा
   u'\u093f', #  ि
   u'\u0940', #  ी
   u'\u0941', #  ु
   u'\u0942', #  ू
   u'\u0943', #  ृ
   u'\u0947', #  े
   u'\u0948', #  ै
   u'\u094b', #  ो
   u'\u094c', #  ौ
   u'\u0902', #  ं
   u'\u0903', #  ः
   u'\u0901', #  ँ
   u'\u0945', #  ॅ
]

unicode_consonants = [
   u'\u0915', # क
   u'\u0916', # ख
   u'\u0917', # ग
   u'\u0918', # घ
   u'\u0919', # ङ
   u'\u091a', # च
   u'\u091b', # छ
   u'\u091c', # ज
   u'\u091d', # झ
   u'\u091e', # ञ
   u'\u091f', # ट
   u'\u0920', # ठ
   u'\u0921', # ड
   u'\u0922', # ढ
   u'\u0923', # ण
   u'\u0924', # त
   u'\u0925', # थ
   u'\u0926', # द
   u'\u0927', # ध
   u'\u0928', # न
   u'\u0929', # ऩ
   u'\u092a', # प
   u'\u092b', # फ
   u'\u092c', # ब
   u'\u092d', # भ
   u'\u092e', # म
   u'\u092f', # य
   u'\u0930', # र
   u'\u0931', # ऱ
   u'\u0932', # ल
   u'\u0933', # ळ
   u'\u0934', # ऴ
   u'\u0935', # व
   u'\u0936', # श
   u'\u0937', # ष
   u'\u0938', # स
   u'\u0939', # ह
   u'\u0958', # क़
   u'\u0959', # ख़
   u'\u095a', # ग़
   u'\u095b', # ज़
   u'\u095c', # ड़
   u'\u095d', # ढ़
   u'\u095e', # फ़
   u'\u095f', # य़
]

krutidev_consonants = [
   u'd', # क
   u'[k', # ख
   u'x', # ग
   u'?k', # घ
   u'\xb3', # ङ
   u'p', # च
   u'N', # छ
   u't', # ज
   u'>', # झ
   u'\xa5', # ञ
   u'V', # ट
   u'B', # ठ
   u'M', # ड
   u'<', # ढ
   u'.k', # ण
   u'r', # त
   u'Fk', # थ
   u'n', # द
   u'/k', # ध
   u'u', # न
   u'u', # ऩ
   u'i', # प
   u'Q', # फ
   u'c', # ब
   u'Hk', # भ
   u'e', # म
   u';', # य
   u'j', # र
   u'j', # ऱ
   u'y', # ल
   u'G', # ळ
   u'\u0934', # ऴ
   u'o', # व
   u"'k" , # श
   u'"k', # ष
   u'l', # स
   u'g', # ह
   u'd', # क़
   u'[k', # ख़
   u'x', # ग़
   u't', # ज़
   u'M+', # ड़
   u'<+', # ढ़
   u'Q', # फ़
   u';', # य़
   u'D',  # क्
   u'[',  # ख्
   u'X',  # ग्
   u'?',  # घ्
   u'\xb3~',  # ङ्
   u'P',  # च्
   u'N~',  # छ्
   u'T',  # ज्
   u'÷',  # झ्
   u'\xa5~',  # ञ्
   u'V~',  # ट्
   u'B~',  # ठ्
   u'M~',  # ड्
   u'<~',  # ढ्
   u'.',  # ण्
   u'R',  # त्
   u'F',  # थ्
   u'n~',  # द्
   u'/',  # ध्
   u'Ë',  # ध्
   u'è',  # ध्
   u'U',  # न्
   u'I',  # प्
   u'¶',  # फ्
   u'C',  # ब्
   u'H',  # भ्
   u'E',  # म्
   u'\xb8',  # य्
   u'Z',  # र्
   u'Y',  # ल्
   u'O',  # व्
   u"'",  # श्
   u"Ü",  # श्
   u'"',  # ष्
   u'L',  # स्
   u'\xba',  # ह्
]

krutidev_unattached_vowel_signs = [
   u'k', # ा
   u'f', # ि
   u'h', # ी
   u'q', # ु
   u'w', # ू
   u'`', # ृ
   u's', # े
   u'S', # ै
   u'ks', # ो
   u'kS', # ौ
   u'a', # ं
   u'%', # ः
   u'\xa1', # ँ
   u'W', # ॅ
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
    kru_text = kru_text.replace(u' \xaa', u'\xaa')
    kru_text = kru_text.replace(u' ~j', u'~j')
    kru_text = kru_text.replace(u' z', u'z')

    # – and — if not surrounded by krutidev consonants/matrās, change them to -
    misplaced = re.compile(ur'[\u2014\u2013]')
    for m in misplaced.finditer(kru_text):
        index = m.start()
        if index < len(kru_text) - 1 and kru_text[m.start() + 1] not in krutidev_consonants + krutidev_unattached_vowel_signs:
            kru_text = kru_text[ : index] + u'&' + kru_text[index + 1 : ]

    for mapping in k2u:
        kru_text = kru_text.replace(mapping[0], mapping[1])

    kru_text = kru_text.replace(u'\xb1', u'Z\u0902') #  ±  ->  Zं
    kru_text = kru_text.replace(u'\xc6', u'\u0930\u094df') #  Æ  ->  र्f

    #  f + ?  ->  ? + ि
    misplaced = re.search('f(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('f' + misplaced, misplaced + u'\u093f')
        misplaced = re.search('f(.?)', kru_text)

    kru_text = kru_text.replace(u'\xc7', u'fa') #  Ç  ->  fa
    kru_text = kru_text.replace(u'\xaf', u'fa') #  ¯  ->  fa
    kru_text = kru_text.replace(u'\xc9', u'\u0930\u094dfa') #  É  ->  र्fa

    #  fa?  ->  ? + िं
    misplaced = re.search('fa(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace('fa' + misplaced, misplaced + u'\u093f\u0902')
        misplaced = re.search('fa(.?)', kru_text)

    kru_text = kru_text.replace(u'\xca', u'\u0940Z') #  Ê  ->  ीZ

    #  ि्  + ?  ->  ्  + ? + ि
    misplaced = re.search(u'\u093f\u094d(.?)', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        kru_text = kru_text.replace(u'\u093f\u094d' + misplaced, u'\u094d' + misplaced + u'\u093f')
        misplaced = re.search(u'\u093f\u094d(.?)', kru_text)

    kru_text = kru_text.replace(u'\u094dZ', u'Z') #  ्  + Z ->  Z

    # र +  ्  should be placed at the right place, before matrās
    misplaced = re.search('(.?)Z', kru_text)
    while misplaced:
        misplaced = misplaced.group(1)
        index_r_halant = kru_text.index(misplaced + 'Z')
        while index_r_halant >= 0 and kru_text[index_r_halant] in unicode_vowel_signs:
            index_r_halant -= 1
            misplaced = kru_text[index_r_halant] + misplaced
        kru_text = kru_text.replace(misplaced + 'Z', u'\u0930\u094d' + misplaced)
        misplaced = re.search('(.?)Z', kru_text)

    # ' ', ',' and ्  are illegal characters just before a matrā
    for matra in unicode_unattached_vowel_signs:
        kru_text = kru_text.replace(' ' + matra, matra)
        kru_text = kru_text.replace(',' + matra, matra + ',')
        kru_text = kru_text.replace(u'\u094d' + matra, matra)

    kru_text = kru_text.replace(u'\u094d\u094d\u0930', u'\u094d\u0930')  #  ्  + ्  + र ->  ्  + र
    kru_text = kru_text.replace(u'\u094d\u0930\u094d', u'\u0930\u094d')  #  ्  + र + ्  ->  र + ्

    kru_text = kru_text.replace(u'\u094d\u094d', u'\u094d') #  ्  + ्  ->  ्

    # ्  at the ending of a consonant as the last character is illegal.
    # Uncomment, if input is Sanskrit
    kru_text = kru_text.replace(u'\u094d ', ' ')

    return kru_text.encode('utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Krutidev2Unicode Font Convertor')
    parser.add_argument('-i', '--input', type = argparse.FileType('r'), dest = 'input_file', help = 'Input File', default = sys.stdin)
    parser.add_argument('-o', '--output', type = argparse.FileType('w'), dest = 'output_file', help = 'Output File', default = sys.stdout)
    args = parser.parse_args()

    for line in args.input_file:
        args.output_file.write(kru2uni(line))