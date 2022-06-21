CC = gcc
OPTIONS = -fopenmp -O3
TARGETS = c_effects c_effectsV2


all: ${TARGETS}

c_effects: c_effects.c c_effects.h
	${CC} c_effects.c -o bin/c_effects
        
c_effectsV2: c_effectsV2.c c_effects.h
	${CC} ${OPTIONS} c_effectsV2.c -o bin/c_effectsV2

clean:
	rm -rf bin/*
