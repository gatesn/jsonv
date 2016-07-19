import jsonv


def main():
    m = jsonv.loads("""
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
    """)
    print m.bind({
        "world": 12345,
        "hello": "abcd",
        "value": [1, 2, 3]
    })


if __name__ == "__main__":
    main()
