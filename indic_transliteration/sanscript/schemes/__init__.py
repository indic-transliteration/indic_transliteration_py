
class Scheme(dict):
    """Represents all of the data associated with a given scheme. In addition
    to storing whether or not a scheme is roman, :class:`Scheme` partitions
    a scheme's characters into important functional groups.
  
    :class:`Scheme` is just a subclass of :class:`dict`.
  
    :param data: a :class:`dict` of initial values. Note that the particular characters present here are also assumed to be the _preferred_ transliterations when transliterating to this scheme. 
    :param synonym_map: A map from keys appearing in `data` to lists of symbols with equal meaning. For example: M -> ['.n', .'m'] in ITRANS. This synonym_map is not used in transliterating to this scheme.
    :param is_roman: `True` if the scheme is a romanization and `False`
                     otherwise.
    """

    def __init__(self, data=None, synonym_map=None, is_roman=True, name=None):
        super(Scheme, self).__init__(data or {})
        if synonym_map is None:
            synonym_map = {}
        self.synonym_map = synonym_map
        self.is_roman = is_roman
        self.name = name

    def fix_lazy_anusvaara(self, data_in):
        from indic_transliteration import sanscript
        data_itrans = sanscript.transliterate(data=data_in, _from=self.name, _to=sanscript.ITRANS)
        itrans_fixed = sanscript.SCHEMES[sanscript.ITRANS].fix_lazy_anusvaara(data_in=data_itrans)
        return sanscript.transliterate(data=itrans_fixed, _from=sanscript.ITRANS, _to=self.name)
    
    def from_devanagari(self, data):
        """A convenience method"""
        from indic_transliteration import sanscript
        return sanscript.transliterate(data=data, _from=sanscript.DEVANAGARI, _to=self.name)