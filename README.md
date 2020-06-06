# InsaneArch
The Insane CPU is a processor that is based on [BrainFuck](https://esolangs.org/wiki/Brainfuck). The main difference is that there are for instences of the interrupter that are interweved. This means that we are able to do more then normal BrainFuck.

For exampe the you could load the text:

```Hello World!```

Into the second program memory. Then load:

```{.>}```

Into the program tape it would print out the clasic Hello World. For those who aren't familiar with BrainFuck, the normal example Hello World program look like this: 

```++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.```

You can see the difference.

## Memory layout 

This CPU has four memory tapes. These tapes are axactly like the [memory tape](https://esolangs.org/wiki/Brainfuck#Memory_and_wrapping) that Brainfuck uses. The only werid thing is that we use two of the tapes as program memory. We run out of the one tape whlie the other remains editable.

## Opcodes

As you may have seen this CPU doesn't only use the opcodes that brainfuck, They are extended to add usefullness, this is done by allowing the user to edit the program memory along with adding an extra tape to do math with and interact with the outside world.

### Ram opcodes
| Command | Description |
|---|---|
| ```>``` | Move the pointer to the right |
| ```<``` | Move the pointer to the left |
| ```+``` | Increment the memory cell under the pointer |
| ```-``` | Decrement the memory cell under the pointer |
| ```.``` | Output the character signified by the cell at the pointer blocking |
| ```,``` | Input a character and store it in the cell at the pointer blocking |
| ```[``` | Jump past the matching ```]``` if the cell under the pointer is 0 |
| ```]``` | Jump back to the matching ```[``` if the cell under the pointer is nonzero |

### Reg Opcodes
| Command | Description |
|---|---|
| ```=``` | Move the pointer to the right |
| ```_``` | Move the pointer to the left |
| ```:``` | Increment the memory cell under the pointer |
| ```;``` | Decrement the memory cell under the pointer |
| ```?``` | Output the character signified by the cell at the pointer |
| ```!``` | Input a character and store it in the cell at the pointer |
| ```/``` | Output the character signified by the cell at the pointer blocking |
| ```\``` | Input a character and store it in the cell at the pointer blocking |
| ```(``` | Jump past the matching ```)``` if the cell under the pointer is 0 |
| ```)``` | Jump back to the matching ```(``` if the cell under the pointer is nonzero |

### Program Opcodes
| Command | Description |
|---|---|
| ```^``` | Move the pointer to the right |
| ```*``` | Move the pointer to the left |
| ```@``` | Increment the memory cell under the pointer |
| ```$``` | Decrement the memory cell under the pointer |
| ```{``` | Jump past the matching ```}``` if the cell under the pointer is 0 |
| ```}``` | Jump back to the matching ```{``` if the cell under the pointer is nonzero |
| ```%``` | Switch Program Tapes |
