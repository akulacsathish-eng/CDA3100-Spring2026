CC := gcc
CFLAGS := -Wall -Wextra -std=c11

# Target to build the executable
all: vault

vault: main.o vault_gen.o seed_util.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: main.c vault_gen.h seed_util.h
	$(CC) $(CFLAGS) -c main.c

vault_gen.o: vault_gen.c vault_gen.h seed_util.h
	$(CC) $(CFLAGS) -c vault_gen.c

seed_util.o: seed_util.c seed_util.h
	$(CC) $(CFLAGS) -c seed_util.c

run: vault
	./vault

clean:
	rm -f *.o vault

.PHONY: all run clean
