JSONv
=====

A toy project to help learn ANTLR JSONv is an extension to the JSON syntax which supports 'variables'.

Example
-------

.. code-block:: python
    from jsonv import jsonv

    jv = jsonv.loads('{"hello": [foo, bar]}')

    assert not jv.bound
    assert isinstance(jv, dict)
    assert 'hello' in jv

    jv.bind({'foo': 'world', 'bar': 'universe'})
    assert jv.bound

    assert jsonv.dumps(jv) == '{"hello": ["world", "universe"]}'

Installing
----------

`pip install .`
