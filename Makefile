SOURCES=shell_chatgpt/main.py

all: $(SOURCES)
	pipenv run python shell_chatgpt/main.py

test: $(SOURCES)
	echo("Test some stuff!")

clean:
	rm -f *.pyc