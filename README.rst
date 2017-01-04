JSONv
=====

A toy project to help learn ANTLR. JSONv is an extension to the JSON syntax which supports 'variables'.

JSONv makes it easy to template JSON files ensuring correct syntax and preserving non-string types.

Example
-------

.. code-block:: json

    {
      "hello": [foo, bar],
      "world": {
        "config": variable_dictionary,
        "something": [0, 1, "string literal", variable]
      }
    }

Python API
----------

.. code-block:: python

    from jsonv import jsonv

    jv = jsonv.loads('{"hello": [foo, bar]}')

    assert not jv.bound
    assert isinstance(jv, dict)
    assert 'hello' in jv

    jv.bind({'foo': 'world', 'bar': {'a nested': 'dictionary'}})
    assert jv.bound

    assert jsonv.dumps(jv) == '{"hello": ["world", {"a nested": "dictionary"}]}'

Installing
----------

.. code-block:: bash

    pip install .
