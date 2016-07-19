grammar JSONv;

/** Taken from "The Definitive ANTLR 4 Reference" by Terence Parr */
// Derived from http://json.org

jsonv
   : value
   ;

jsonObject
   : '{' pair (',' pair)* '}'
   | '{' '}'
   ;

pair
   : string ':' value
   ;

jsonArray
   : '[' value (',' value)* ']'
   | '[' ']'
   ;

unbound: UNBOUND;

true: 'true';
false: 'false';
null: 'null';

number: NUMBER;
string: STRING;

value
   : string
   | number
   | jsonObject
   | jsonArray
   | unbound
   | true
   | false
   | null
   ;

STRING
   : '"' STRING_CHAR* '"'
   ;

UNBOUND
   : [a-zA-Z] [a-zA-Z0-9]*
   ;

fragment STRING_CHAR
    : (ESC | ~ ["\\])
    ;

fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;

fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;

fragment HEX
   : [0-9a-fA-F]
   ;

NUMBER
   : '-'? INT '.' [0-9] + EXP? | '-'? INT EXP | '-'? INT
   ;

fragment INT
   : '0' | [1-9] [0-9]*
   ;
// no leading zeros

fragment EXP
   : [Ee] [+\-]? INT
   ;
// \- since - means "range" inside [...]

WS
   : [ \t\n\r] + -> skip
   ;
