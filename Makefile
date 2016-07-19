

build:
	@java -Xmx500M -cp "/usr/local/lib/antlr-4.5.3-complete.jar:$CLASSPATH" org.antlr.v4.Tool JSONv.g4 -o jsonv_parser -Dlanguage=Python2 -visitor -no-listener

install:
	curl -O http://www.antlr.org/download/antlr-4.5.3-complete.jar

testpy:
	@python test.py
