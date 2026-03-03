CC=gcc
CFLAGS=-std=c99 -Werror -Wall -Wextra -Wvla -pedantic
LDLIBS=
SRC=src/evalexpr.c src/fifo_access.c src/fifo_setup_destroy.c src/stack.c src/main.c src/convert_std.c
OBJ=$(SRC:.c=.o)

all: $(OBJ) 
	$(CC) $(OBJ) -o evalexpr $(LDLIBS)

check:
	./tests/test_rpn.sh
	./tests/test_std.sh
	./tests/test_err.sh

clean:
	rm -f evalexpr
	rm -f src/*.o	
