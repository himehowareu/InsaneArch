# Memory

Memory is divided into 4 tapes. There are two tapes that are designed to be used for programable memory.The other two tapes are for data calculations, the first one is our ram tape, this is the tape that will be used by the program to do the math. The last tape will be used for interacting with the other modules and setting up the system.

## Program Memory
### Tape Layout 
The two tapes that make up the program tapes are both loaded from file on machine boot. These tapes can be loaded with data and/or the program.
### Program
The computer will have a bios that is loaded from the sd and will give a basic prompt for the user to load their program. This might be switch to load a main file by default. 

## Ram
The first half of the ram is used to run the system. The second half of the ram will be used for the users code. 

## registers
The registers are used to interact with the other modules.
The main thing that needs to be known is that when the processor sends a value out on a register there are two ways it can do it; blocking and non-blocking.
 
