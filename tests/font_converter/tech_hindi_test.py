from __future__ import unicode_literals

import logging

from indic_transliteration.font_converter import tech_hindi

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(filename)s:%(lineno)d %(message)s"
)

def test_dvt_vedic():
    # Note: Start chrome with: 
    # google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost &
    # To get the test working on travis ci, maybe pass debugger_address="127.0.0.1:9222" below.
    converter = tech_hindi.DVTTVedicConverter()
    text_in = "    +<=hÉÂ *1* +EòÉ®úÉä Ê´É´ÉÞiÉ ={ÉÊnù¹]õ& |ÉÉÊGòªÉÉnù¶ÉÉªÉÉÆ SÉäiªÉjÉ \"+ +' (ºÉÚ.8-4-68)  "
    output = converter.convert(text_in)
    expected = "    अइउण् ।1। अकारो विवृत उपदिष्टः प्राक्रियादशायां चेत्यत्र \"अ अ\" (सू.8-4-68)  "
    assert output == expected, u'%s == %s (%s in %s)' % (output, expected, text_in, converter.__class__)
