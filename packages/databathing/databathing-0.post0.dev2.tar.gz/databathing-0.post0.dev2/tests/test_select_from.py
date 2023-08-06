from __future__ import absolute_import, division, unicode_literals

from unittest import TestCase
from mo_sql_parsing import parse

import json
from databathing.pipeline import Pipeline


# python -m unittest discover tests

class TestSelectFrom(TestCase):
    def test_decisive_equailty(self):

        sql = """
        SELECT a, b, c
        FROM Test
        """
        # parsed_whole_query = parse(sql)
        # parsed_json_whole_query = json.loads(json.dumps(parsed_whole_query, indent=4))

        pipeline = Pipeline(sql)
        ans = pipeline.parse()
        expected = """final_df = Test\\\n.selectExpr("a","b","c")\n\n"""
        self.assertEqual(ans, expected)