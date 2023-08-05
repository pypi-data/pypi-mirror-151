# -*- coding: utf-8 -*-

import csv
import re
import pkg_resources

class INEMapingTugesto():
    """
    Reads a CSV file (ine_maping_tugesto.csv) delimited by ; that contains a list of cities with those columns:
    - ine_code (int):  INE code of the city (can be black).
    - city_name (string): Name of the city from Tugesto.
    - county_id (int): official INE code of the county  (ES: provincia) casted to integer.
    - tugesto_id (int): custom Tugesto ID of the city.

    The class provides this method:s
    - get_tugesto_id(self, ine_code, city_name, county_id) --> returns tugesto_id or None

    Caution: The official INE city name of the city "L'Albiol" is "Albiol, L'", but tne related Tugesto name is 'Albiol (L')",
    so this class take it in consideration to be able to find "Albiol (L')" when the given city_name is "Albiol, L'". It is also
    applicable to the list of special cases that reflects the class attribute: __special_tugesto_city_name_patterns, (ex: 'Tuna, Sa' or 'Madrigueiras, O',...)
    """

    __special_tugesto_city_name_patterns = ['l\'','els','les','las','los','la','el','es','sa','en','na','o','a']

    def __init__(self):

        self._rows = []
        csv_path = pkg_resources.resource_filename('ine_tugesto_somenergia', 'csv/ine_maping_tugesto.csv')
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                self._rows.append(row)

        assert self._rows, 'Unable to load the listo of Tugesto cities'

        self._special_tugesto_city_name_pairs_dict = dict(list(map(lambda x: (', %s'%x,' (%s)'%x),INEMapingTugesto.__special_tugesto_city_name_patterns)))
        self._p = re.compile(r'(?:{})'.format('|'.join(map(re.escape, list(map(lambda x: ', %s'%x, INEMapingTugesto.__special_tugesto_city_name_patterns))))))

    def _filter_rows(self, rgx, county_id):
        return list(filter(lambda x: (
                ((county_id and int(x['county_id'])==county_id) and rgx.findall(x['city_name'].lower()))
                or
                (not county_id and rgx.findall(x['city_name'].lower()))
                ), self._rows))

    def get_tugesto_id(self, city_name, county_id=None, ine_code=None):

        tg_ids, res = [], None
        assert city_name and type(city_name) in (str, unicode), 'The type of the provided city_name is not allowed'

        if ine_code:
            try:
                ine_code = int(ine_code)
            except:
                raise Exception('The type of the provided ine_code is not allowed')

            tg_ids = list(filter(lambda x: (int(x['ine_code']) if x['ine_code'] != '' else False) == ine_code, self._rows))
            res = (tg_ids and tg_ids[0]['tugesto_id']) or None

        if not res:
            if county_id:
                try:
                    county_id = int(county_id)
                except:
                    pass # do not raise any excepction, instead discart county_id usage
                    county_id = None

            rgx = re.compile(r'\b{}\b'.format(re.escape(city_name.lower())))
            tg_ids = self._filter_rows(rgx, county_id)

            if (not tg_ids) and self._p.findall(city_name.lower()):

                pattern_found = self._p.findall(city_name.lower())[0]
                target_tugesto_city_name = city_name.lower().replace(pattern_found,self._special_tugesto_city_name_pairs_dict[pattern_found])

                rgx = re.compile(r'{}'.format(re.escape(target_tugesto_city_name)))
                tg_ids = self._filter_rows(rgx, county_id)

            res = (tg_ids and tg_ids[0]['tugesto_id']) or None

        return res
