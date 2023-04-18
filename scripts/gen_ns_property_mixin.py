import re
from dataclasses import fields

from docarray.score.data import NamedScoreData

with open('../docarray/score/mixins/property.py', 'w') as fp:
    fp.write(f'''# auto-generated from {__file__}
from typing import Optional

class PropertyMixin:
    ''')
    for f in fields(NamedScoreData):
        if f.name.startswith('_'):
            continue
        ftype = str(f.type).replace('typing.Dict', 'Dict').replace('typing.List', 'List').replace('datetime.datetime',
                                                                                                  '\'datetime\'')
        ftype = re.sub(r'typing.Union\[(.*), NoneType]', r'Optional[\g<1>]', ftype)
        ftype = re.sub(r'ForwardRef\((\'.*\')\)', r'\g<1>', ftype)
        ftype = re.sub(r'<class \'(.*)\'>', r'\g<1>', ftype)

        r_ftype = ftype
        if f.name == 'chunks':
            r_ftype = 'Optional[\'ChunkArray\']'
        elif f.name == 'matches':
            r_ftype = 'Optional[\'MatchArray\']'

        fp.write(f'''
    @property
    def {f.name}(self) -> {r_ftype}:
        self._data._set_default_value_if_none('{f.name}')
        return self._data.{f.name}
            ''')

        ftype = re.sub(r'Optional\[(.*)]', r'\g<1>', ftype)

        fp.write(f'''
    @{f.name}.setter
    def {f.name}(self, value: {ftype}):
        self._data.{f.name} = value
        ''')
