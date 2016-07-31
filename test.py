#!/usr/bin/env python
import json
from jsonv import jsonv

SRC = """
    {
        "array": [hello, world],
        "key": value,
        "nothing": null,
        "truthy": true,
        "falsey": false,
        "number": 10,
        "floaty": 10.5,
        "stringy": "foo"
    }
    """

BINDINGS = {
    "world": 12345,
    "hello": "abcd",
    "value": [1, 2, 3]
}

BOUND = """
    {
        "array": ["abcd", 12345],
        "key": [1,2,3],
        "nothing": null,
        "truthy": true,
        "falsey": false,
        "number": 10,
        "floaty": 10.5,
        "stringy": "foo"
    }
    """


def main():
    print "JSONv:", SRC
    m = jsonv.loads(SRC)

    print "Bindings:", BINDINGS
    bound = m.bind(BINDINGS)

    print "Bound:", bound
    assert bound == json.loads(BOUND)


if __name__ == "__main__":
    main()
