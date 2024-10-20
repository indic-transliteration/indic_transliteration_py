import regex

def soften(text, pattern):
  text = regex.sub(pattern.format("क"), r"ग", text)
  text = regex.sub(pattern.format("च"), r"ज", text)
  text = regex.sub(pattern.format("ट"), r"ड", text)
  text = regex.sub(pattern.format("त"), r"द", text)
  text = regex.sub(pattern.format("प"), r"ब", text)
  return text


def harden(text, pattern):
  text = regex.sub(pattern.format("ग"), r"क", text)
  text = regex.sub(pattern.format("ज"), r"च", text)
  text = regex.sub(pattern.format("ड"), r"ट", text)
  text = regex.sub(pattern.format("द"), r"त", text)
  text = regex.sub(pattern.format("ब"), r"प", text)
  return text



def set_tamil_soft_consonants(text):
  # Compare with https://github.com/virtualvinodh/aksharamukha-python/blob/5690ffb246e4c427bc937ed1cc3c7823ce37db10/aksharamukha/PreProcess.py#L1670
  text = soften(text=text, pattern="(?<=[ऩ][ा-्]?)({})(?!्)")
  text = soften(text=text, pattern="(?<=[ऱ][ा-ौ]?)({})(?!्)")
  # text = soften(text=text, pattern="(?<=[अ-औकचटतपयरलवशषसहळ][ा-ौ]?)({})(?!् *\\1)")
  return text


def fix_naive_ta_transliterations(text):
  text = harden(text=text, pattern="(?<=[ऩ][ा-्]?)({})(?=् )")
  text = harden(text=text, pattern="(?<=[ऱ][ा-ौ]?)({})(?=् )")
  text = regex.sub("म्([सव])", r"ं\1", text)
  text = regex.sub("ट्र", r"ऱ्ऱ", text)
  text = regex.sub("ण्ड्र", r"ऩ्ऱ", text)
  text = regex.sub("न्न", r"ऩ्ऩ", text)
  text = regex.sub("न(्?)(?![ं-०])", r"ऩ\1", text)
  text = regex.sub("ेऩ(?![ं-०])", r"ेन", text) # प्रसादेन
  text = regex.sub("न्ग(?!ळ)", "ऩ्ग", text)
  text = regex.sub("दिक(?=ळ)", "दिग", text)
  return text
