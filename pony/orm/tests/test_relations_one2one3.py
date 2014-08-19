from __future__ import absolute_import, print_function, division

import unittest

from pony.orm.core import *
from pony.orm.tests.testutils import *

class TestOneToOne3(unittest.TestCase):
    def setUp(self):
        self.db = Database('sqlite', ':memory:')

        class CommonItem(self.db.Entity):
            url = Required(unicode)
            act_item1 = Optional("ActItem1")

        class ActItem1(self.db.Entity):
            regnum = Required(unicode)
            common_item = Required("CommonItem")

        self.db.generate_mapping(create_tables=True)

        with db_session:
            c1 = CommonItem(url='http://example.com')
            a1 = ActItem1(regnum='r1', common_item=c1)

    def tearDown(self):
        self.db = None

    def test_1(self):
        with db_session:
            obj = select(r for r in self.db.CommonItem if r.act_item1.id).first()
            self.assertEqual(obj.url, 'http://example.com')
            self.assertEqual(obj.act_item1.regnum, 'r1')

if __name__ == '__main__':
    unittest.main()
