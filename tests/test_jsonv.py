import unittest
from jsonv import jsonv


class TestJsonV(unittest.TestCase):

    def test_loads(self):
        jv = jsonv.loads("""
            {"hello": world, "foo": [b, a, "r"]}
        """)
        self.assertFalse(jv.bound)
        self.assertIsInstance(jv, dict)
        self.assertIn("hello", jv)

        l = jv["foo"]
        self.assertIsInstance(l, list)
        self.assertFalse(l.bound)

    def test_binding(self):
        jv = jsonv.loads("""
            {"hello": world, "foo": [b, a, "r"]}
        """)
        self.assertFalse(jv.bound)

        v = jv["hello"]
        self.assertFalse(v.bound)

        v.bind({"world": 12345})
        self.assertTrue(v.bound)
        self.assertEqual(12345, v.value)

        l = jv["foo"]
        self.assertFalse(l.bound)

        l.bind({"b": 1, "a": 2})
        self.assertTrue(l.bound)

        self.assertEqual("[1, 2, \"r\"]", jsonv.dumps(l))
