# Brainfuck Algorithms
In the interest of generality, the algorithms will use variable names in place of the < and > instructions.  Temporary cells are denoted "temp".  When using an algorithm in a program, replace the variable names with the correct number of < or > instructions to position the pointer at the desired memory cell.

Example:

If "a" is designated to be cell 1, "b" is cell 4, and the pointer is currently at cell 0, then:

```
a[b+a-]
```

becomes: 

```
>[>>>+<<<-]
```

If a particular algorithm requires cell value wrapping, this will be noted, along with a non-wrapping version, if known.  Certain assumptions, such as that a temporary memory cell is already zero, or that a variable used for computation can be left zeroed, are not made.  Some optimizations can therefore be performed when exact conditions are known.

## Comments

The usefulness of this type of comment is that instructions commonly used for   punctuation (such as "," and ".") may be used freely.  The use of "[" and "]" inside a comment should be avoided, unless they are matched. This commenting style does not work well for internal code comments, unless strategically placed where the cell value is known to be zero (or can be modified to be zero and restored)
```
[comment]
```

To make no assumption about the initial cell value, use

```
[-][comment]
```

Since loops only terminate when / if the current cell is zeroed, comments can safely be placed directly behind any other loop.

```
,[.,][comment]
```

## Read all characters into memory
```
,[>,]
```

## Read until newline/other char
```
----------[++++++++++>,----------]++++++++++
```

Adjust the number of +/- to the char code you want to match. Omit the final + block to drop the char. Requires wrapping.

## Read until any of multiple chars

```
+>[
   >,
   (-n1)[(+n1)[>+<-]]>[<+>-]<
   (-n2)[(+n2)[>+<-]]>[<+>-]<
   etc
 ]
```
(+/-n1)
means repeat that operator n1 times. n1, n2 etc are the char codes you want to match. One line for each.

## x = 0
```
x[-]
```

## x = y
```
 temp0[-]
 x[-]
 y[x+temp0+y-]
 temp0[y+temp0-]
 ```

## x = x + y
```
 temp0[-]
 y[x+temp0+y-]
 temp0[y+temp0-]
```

## x = x - y
```
 temp0[-]
 y[x-temp0+y-]
 temp0[y+temp0-]
```

## x = x * y
```
 temp0[-]
 temp1[-]
 x[temp1+x-]
 temp1[
  y[x+temp0+y-]temp0[y+temp0-]
 temp1-]
```

## x = x * x
```
 x[temp0+x-]
 temp0[-[temp1+x++temp0-]x+temp1[temp0+temp1-]temp0]
```

## x = x / y
```
 temp0[-]
 temp1[-]
 temp2[-]
 temp3[-]
 x[temp0+x-]
 temp0[
  y[temp1+temp2+y-]
  temp2[y+temp2-]
  temp1[
   temp2+
   temp0-[temp2[-]temp3+temp0-]
   temp3[temp0+temp3-]
   temp2[
    temp1-
    [x-temp1[-]]+
   temp2-]
  temp1-]
  x+
 temp0]
```

This algorithm will compute x / y, put the remainder into x and put the quotient into q

```
 x[
  temp1+[
   y[x-[temp1+†]temp1-temp0+y-]
   temp0[y+temp0-]q+temp1
  ]
 ]
 x[y[temp0+x+y-]temp0[y+temp0-]q-†]
```

## x = x ^ y
```
  temp0[-]
  x[temp0+x-]
  x+
  y[
    temp1[-]
    temp2[-]
    x[temp2+x-]
    temp2[
      temp0[x+temp1+temp0-]
      temp1[temp0+temp1-]
    temp2-]
  y-]
```

## swap x, y
```
 temp0[-]
 x[temp0+x-]
 y[x+y-]
 temp0[y+temp0-]
```
```
 x[-temp0+y-x]
 y[-x+y]
 temp0[-y+x+temp0]
```

## x = -x
```
 temp0[-]
 x[temp0-x-]
 temp0[x-temp0+]
```

## x = not x (bitwise)## 
```
 temp0[-]
 x-
 [temp0-x-]
 temp0[x+temp0-]
```
```
x-[[-]+y](y-1)
```

## Find a zeroed cell## 
### To the right
```
 [>]
```
### To the left
```
 [<]
```

## x(y) = z (1-d array) (2 cells/array element)

The cells representing x, temp0, and temp1 must be contiguous, with x being the leftmost cell and temp1 the rightmost, followed by adequate memory for the array.  Each array element requires 2 memory cells.  The pointer ends at x.
```
 temp0[-]
 temp1[-]
 temp2[-]
 y[temp1+temp2+y-]temp2[y+temp2-]
 z[temp0+temp2+z-]temp2[z+temp2-]
 x>>[[>>]+[<<]>>-]+
  [>>]<[-]<[<<]
  >[>[>>]<+<[<<]>-]
  >[>>]<<[-<<]
```

The code up through "-]+" creates a trail of 1's that the later loops will use to find the destination cell.  The cells are grouped as "data cell, 1-cell".  The destination cell is "data cell, 0-cell", so that the "[>>]" stops in a useful place.  The x cell is always 0, and serves as the left-side stop for the "[<<]" statements (notice that t1 is cleared by the first loop, but the loop's trailing "+" converts it to the first 1-cell in the trail).  Next, the trail is followed and "[-]" clears the destination cell.  The array is now prepared, so an add-to loop of the form "temp0[dest+temp0-]" moves the value in temp0 to the destination cell.  Finally, with ">[>>]" the trail of 1's is followed one last time forward, and cleared on the way back, ending at the left stop, x.  Contiguous memory required for the array is 3 + 2 * number of array elements.
 
## x = y(z) (1-d array) (2 cells/array element)

The cells representing y, temp0, and temp1 must be contiguous, with x being the leftmost cell and temp1 the rightmost, followed by adequate memory for the array. Each array element requires 2 memory cells. The pointer ends at y.
```
 x[-] 
 temp0[-]
 temp1[-]
 z[temp1+temp0+z-]temp0[z+temp0-]
 y>>[[>>]+[<<]>>-]+[>>]<[<[<<]>+< (pointer is at y)
  x+
 y>>[>>]<-]<[<<]>[>[>>]<+<[<<]>-]>[>>]<<[-<<]
```

## x(y) = z (1-d array) (1 cell/array element)

The cells representing space, index1, index2 and Data must be contiguous and initially empty (zeroed), with space being the leftmost cell and Data the rightmost, followed by adequate memory for the array. Each array element requires 1 memory cell. The pointer ends at space. index1, index2 and Data are zeroed at the end.
```
 z[-space+data+z]space[-z+space]
 y[-space+index1+y]space[-y+space]
 y[-space+index2+y]space[-y+space]
 >[>>>[-<<<<+>>>>]<[->+<]<[->+<]<[->+<]>-]
 >>>[-]<[->+<]<
 [[-<+>]<<<[->>>>+<<<<]>>-]<<
```

## x = y(z) (1-d array) (1 cell/array element)

The cells representing space, index1, index2 and Data must be contiguous and initially empty (zeroed), with space being the leftmost cell and Data the rightmost, followed by adequate memory for the array. Each array element requires 1 memory cell. The pointer ends at data. index1, index2 and Data are zeroed at the end.
```
 z[-space+index1+z]space[-z+space]
 z[-space+index2+z]space[-z+space]
 >[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]
 >>>[-<+<<+>>>]<<<[->>>+<<<]>
 [[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<
 x[-]
 data[-x+data]
```

## x = x == y

The algorithm returns either 0 (false) or 1 (true) and preserves y.
```
 temp0[-]
 temp1[-]
 x[temp1+x-]+
 y[temp1-temp0+y-]
 temp0[y+temp0-]
 temp1[x-temp1[-]]
```

And if you don't need to preserve x or y, the following does the task without requiring any temporary blocks. Returns 0 (false) or 1 (true).
```
 x[-y-x]+y[x-y[-]]
```

## x = x != y

The algorithm returns either 0 (false) or 1 (true).
```
 temp0[-]
 temp1[-]
 x[temp1+x-]
 y[temp1-temp0+y-]
 temp0[y+temp0-]
 temp1[x+temp1[-]]
```

Sets x to be 1 if x == y, 0 otherwise.
```
 x[
  y-x-]
 y[[-]
  x+y]
```

## x = x < y

x and y are unsigned.  temp1 is the first of three consecutive temporary cells.  The algorithm returns either 0 (false) or 1 (true).
```
 temp0[-]
 temp1[-] >[-]+ >[-] <<
 y[temp0+ temp1+ y-]
 temp0[y+ temp0-]
 x[temp0+ x-]+
 temp1[>-]> [< x- temp0[-] temp1>->]<+<
 temp0[temp1- [>-]> [< x- temp0[-]+ temp1>->]<+< temp0-]
```

## x = x <= y
x and y are unsigned.  temp1 is the first of three consecutive temporary cells.  The algorithm returns either 0 (false) or 1 (true).
```
 temp0[-]
 temp1[-] >[-]+ >[-] <<
 y[temp0+ temp1+ y-]
 temp1[y+ temp1-]
 x[temp1+ x-]
 temp1[>-]> [< x+ temp0[-] temp1>->]<+<
 temp0[temp1- [>-]> [< x+ temp0[-]+ temp1>->]<+< temp0-]
```

## z = x > y

This uses balanced loops only, and requires a wrapping implementation (and will be very slow with large numbers of bits, although the number of bits otherwise doesn't matter.) The temporaries and x are left at 0; y is set to y-x. (You could make a temporary copy of x via using another temporary that's incremented during the loop.)
```
 temp0[-]temp1[-]z[-]
 x[ temp0+
        y[- temp0[-] temp1+ y]
    temp0[- z+ temp0]
    temp1[- y+ temp1]
    y- x- ]
```

## z = sign(x-y)

This is a comparison of two numbers for non-wrapping implementations. The signs of the two numbers must be known. Part of it can also be used to find the sign of an unknown number if both it and its opposite are available. z and the four cells to its right must be free and clear (and will be again when the algorithm terminates), an assumption that must be made in a non-wrapping implementation, as the direction to clear these cells could not be known to this algorithm. The code blocks indicated by parenthetical comments could contain code which depends on the result of the comparison; there is no particular reason in practice to wait for the value of z to be set to one of {-1,0,1}.
```
 x[z>>+>-x-]†
 y[z>>->+y-]†
 z+>>
 [->-[>]<<]
 <[
   (y>=x)
   -
   >>[
     (y>x)
     <<+>>[+]
   ]<
 ]
 >>[
   (x>y)
   [+]
 ]
 <<<
 ```

 (put an {if 0, then do} algorithm here to run code conditional on y=x)


## x = not x (boolean, logical)

The algorithm returns either 0 (false) or 1 (true).
```
  temp0[-]
 x[temp0+x[-]]+
 temp0[x-temp0-]
```

Another version for when you can consume x (mutate its value). Also assumes that x is either 0 or 1. If you do not want to consume x, you can still use this algorithm. Just copy x to another cell, then apply the operation. The algorithm returns either 0 (false) or 1 (true).
```
 temp0[-]+
 x[-temp0-]temp0[x+temp0-]
```

Modification of Sunjay's version above.
```
 temp0[-]+
 x[[-]temp0-x]temp0[-x+temp0]
 ```
Then there's undoubtedly no mistake. When x>1, the result will be as same as x=1 .

Even another version that consumes x. Returns 0 (false) if x is 1 (true) and 1 if x is 0.
```
 temp0[-]
 x[temp0-x-]temp0+
```

A harder-to-understand version that actually is "y = not x", which preserves x but needs 3 continuous cells in total.
Maybe using it for calculating "y = not x" is not necessary, but I think this idea will be quite useful in some cases.
In fact the idea is also embodied in other codes in this page.

 #Define these 3 cells as x, y=1 and t=0.
 ```
 x>y[-]+>t[-]<<x
 [>y[-]]>[>t]
```
According to whether x==0 or not, there are two different run modes because the position of the pointer changes in the "[]" loop.
The following is the process of the second line, "*" means the pointer is here.
```
 If x==0:                           If x!=0:
                   x  y  t                            x  y  t
                  *0  1  0                           *1  1  0
 [>y[-]]          *0  1  0          [>y[-]]           1 *0  0
 [>y[-]]>          0 *1  0          [>y[-]]>          1  0 *0
 [>y[-]]>[>t]      0  1 *0          [>y[-]]>[>t]      1  0 *0
 ```
----
It is based on x=x## y, where I set y into 0.
```
 y+x[-y-x]+y[x-y[-]]x
```

## x = x and y (boolean, logical)

The algorithm returns either 0 (false) or 1 (true).
``` temp0[-]
 temp1[-]
 x[temp1+x-]
 temp1[
  temp1[-]
  y[temp1+temp0+y-]
  temp0[y+temp0-]
  temp1[x+temp1[-]]
 ]
```

Consumes x and y (leaves them as zero at the end of the algorithm) and stores the result in z. For short-circuit evaluation, don't evaluate x or y until just before they are used.

The algorithm returns either 0 (false) or 1 (true).
``` z[-]
 x[
  y[z+y-]
  x-
 ]
 y[-]
```

Consumes x and y and outputs 1 in z if both x and y are 1, else 0.
``` z[-]
 x[
  -y[-z+y]
  x]
```

## z = x or y (boolean, logical) (wrapping)

Required structure:
```
   0 0 x y
       ^
```
With the cursor pointing at x, the value of the logical operation x or y will be stored in the left most cell. The values of x and y will be preserved
```
   [<<->]<+[<]+>[-<->>+>[<-<<+>>]<[-<]]>
```
Shorter version:
```
   [<<+>]>[<<[>]<[-]+>]<[>>]
```

## z = x nand y (boolean, logical)

Consumes x and y and outputs 0 in z if both x and y are 1, else 1.
``` z[-]+
 x[
  y[z-y-]
  x-
 ]
 y[-]
```

## x = x or y (boolean, logical)
The algorithm returns either 0 (false) or 255 (true).
```
 temp0[-]
 temp1[-]
 x[temp1+x-]
 temp1[x-temp1[-]]
 y[temp1+temp0+y-]temp0[y+temp0-]
 temp1[x[-]-temp1[-]]
 ```

Returns 1 (x = 1) if either x or y are 1 (0 otherwise)If you use it in the case that x>1 or y>1,please make sure it won't cause overflow problem.
For example,if x=1 and y=255, than x will be 0.
```
 x[
  y+x-]
 y[
  x+y[-]
 ]
```

Consumes x and y (leaves them as zero at the end of the algorithm) and stores the result in z. For short-circuit evaluation, don't evaluate x or y until just before they are used.

If you don't care about short-circuit evaluation, temp0 can be removed completely. If temp0 is removed and both x and y are 1, z will be 2, not 1. This is usually not a problem since it is still non-zero, but you should keep that in mind.<br />
Or there's a way to fix it, add these codes to the end:
```
 z[x+z[-]]
 x[z+x-]
```
The algorithm returns either 0 (false) or 1 (true).
```
 z[-]
 temp0[-]+
 x[
  z+
  temp0-
  x-
 ]
 temp0[-
  y[
   z+
   y-
  ]
 ]
 y[-]
```

Consumes x and y, does not use a temporary cell. Makes z 1 (true) or 0 (false) if either x or y are one.
```
 z[-]
 x[y+x-]
 y[[-]
 z+y]
```

## x = x nor y (boolean, logical)

Consumes x and y and outputs 0 in x if both x and y are 1, else 1.
```
 x[z+x[-]]
 y[z+y[-]]
 z[x+z[-]]
```

## z = x xor y (boolean, logical)

Consumes x and y. Makes z 1 (true) or 0 (false) if x does not equal y.
Finishes at y.
```
 z[-]
 x[y-
  x-]
 y[z+
  y[-]]
```

## z = x xnor y (boolean, logical)

Consumes x and y. Makes z 1 (true) or 0 (false) if x equal y.
Finishes at y.
```
 z[-]+
 x[
   y-
   x-
 ]
 y[
   z-
   y[-]
 ]
```

## z = MUX(a, x, y) (boolean, logical)
If a is equal to 1, then z is equal to y. Otherwise, if a is equal to 0, z will be equal to x.
When done, a, x, and y will all be 0 regardless of their starting values.
e.g:
```
IN: x = 0, y = 1, a = 1
OUT: x = 0, y = 0, a = 0, z = 1 
```
```
 z[-]
 y[
  a[z+a-]
 y-]
 x[
  a-[
   [-]z[-]+
  a]
 x-]
 a[-]
```

## while (x) { code }

To implement a while loop, you need to evaluate the condition x both before the loop and at the end of the loop body.
```
 'evaluate x'
 x[
  'code'
  'evaluate x again'
  x
 ]
```

## break and continue

To implement break and continue statements in loops, consider that the following two pieces of pseudocode are functionally equivalent:
```
 while (foo) {
  if (bar == foo) {
   if (x > 2) {
    break;
   }
   else {
    // do stuff
   }
   // do stuff
  }
  // update foo for the next iteration
 }
 ```
 ```
 // Equivalent without break statement:
 while (foo) {
  shouldBreak = false
  if (bar == foo) {
   if (x > 2) {
    shouldBreak = true
   }
   else {
    // do stuff
   }
   
   // don't evaluate any more code in the loop after breaking
   if (!shouldBreak) {
    // do stuff
   }
  }
  if (shouldBreak) {
   // so that the loop stops
   foo = 0
  }
  else {
   // update foo for the next iteration
  }
 }
```

Notice that we need to guard '''all''' code ''after'' the break statement in the loop to prevent it from running. We don't need to guard in the else statement immediately after the break statement because that will never run after the break statement has run.

This approach allows us to implement break and continue statements in brainfuck despite the lack of sophisticated jump instructions. All we're doing is combining the concept of an if statement (defined below) with the while loop we just defined and applying it here.

Implementing a continue statement is the same thing except you never guard the loop updating code:
```
 while (foo) {
  if (bar == foo) {
   if (x > 2) {
    continue;
   }
   else {
    // do stuff
   }
   // do stuff
  }
  // update foo for the next iteration
 }
 ```
 ```
 // Equivalent without continue statement:
 while (foo) {
  shouldContinue = false
  if (bar == foo) {
   if (x > 2) {
    shouldContinue = true
   }
   else {
    // do stuff
   }
   
   // don't evaluate any more code in the loop after continuing
   if (!shouldContinue) {
    // do stuff
   }
  }
  
  // This code stays the same after a continue because we still want to move on to the next iteration of the loop
  // update foo for the next iteration
 }
```

To implement both break and continue, you can compose the concepts here and make any combination you want. You can consider break and continue statements to be "sugar" that needs to be "desugared" in your brainfuck code.

## if (x) { code }
```
 temp0[-]
 temp1[-]
 x[temp0+temp1+x-]temp0[x+temp0-]
 temp1[
  '''''code'''''
 temp1[-]]
or alternatively:
 temp0[-]
 x[
  '''''code'''''
  temp0
 ]x
 ``` 
or alternatively if you don't need x anymore:
```
 x[
  '''''code'''''
  x[-]
 ]
```

## if (x == 0) { code }


## if (x) { code1 } else { code2 }
```
 temp0[-]
 temp1[-]
 x[temp0+temp1+x-]temp0[x+temp0-]+
 temp1[
  '''''code1'''''
  temp0-
 temp1[-]]
 temp0[
  '''''code2'''''
 temp0-]
```
```
 temp0[-]+
 temp1[-]
 x[
  '''''code1'''''
  temp0-
  x[temp1+x-]
 ]
 temp1[x+temp1-]
 temp0[
  '''''code2'''''
 temp0-]
```

This is an alternate approach. It's more efficient since it doesn't require copying x, but it does require that temp0 and temp1 follow x consecutively in memory.

```
 temp0[-]+
 temp1[-]
 x[
  '''''code1'''''
  x>-]>
 [<
  '''''code2'''''
  x>->]<<
```

##  x = pseudo-random number

This algorithm employs a Linear congruential generator|linear congruential generator of the form:

``` V = (A * V + B) % M```

Where:
 A = 31821, B = 13849, M = period = 65536, V = initial seed
  
A and B values were obtained from the book:

Texas Instruments TMS320 DSP DESIGNER'S NOTEBOOK Number 43
Random Number Generation on a TMS320C5x, by Eric Wilbur

Assumes 8-bit cells.  After the code is executed, the variable "x" holds a pseudo-random number from 0 to 255 (the high byte of V, above).  The variable cells "randomh" and "randoml" are the internal random number seed and should not be altered while random numbers are being generated.
```
 temp0[-]
 temp1[-]
 temp2[-]
 temp3[-]
 temp4[-]
 temp5[-]
 randomh[temp0+randomh-]
 randoml[temp1+randoml-]
 temp3+++++++[temp2+++++++++++@temp3-]
 temp2[
  temp0[randomh+temp3+temp0-]
  temp3[temp0+temp3-]
  temp1[randomh+temp3+temp4+temp1-]
  temp4[temp1+temp4-]
  temp3[
   randoml+[temp4+temp5+randoml-]
   temp5[randoml+temp5-]+
   temp4[temp5-temp4[-]]
   temp5[randomh+temp5-]
  temp3-]
 temp2-]
 ++++++[temp3++++++++temp2-]
 temp3-[
  temp1[randomh+temp2+temp1-]
  temp2[temp1+temp2-]
 temp3-]
 temp0[-]temp1[-]+++++[temp0+++++temp1-]
 temp0[
  randoml+[temp1+temp2+randoml-]
  temp2[randoml+temp2-]+
  temp1[temp2-temp1[-]]
  temp2[randomh+temp2-]
 temp0-]
 ++++++[randomh+++++++++temp0-]
 randomh[x+temp0+randomh-]
 temp0[randomh+temp0-]
```
##  Divmod algorithm

A clever algorithm to compute div and mod at the same time:
```
 # >n 0 d
 [->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]
 # >0 n d-n%d n%d n/d
```
If one does not need to preserve n, use this variant:
```
 # >n d
 [->-[>+>>]>[+[-<+>]>+>>]<<<<<]
 # >0 d-n%d n%d n/d
```
This algorithm doesn't work when the divisor is 0 or 1.

Modification of the version above.
```
 # >n d
 [->[->+>>]>[<<+>>[-<+>]>+>>]<<<<<]
 >[>>>]>[[-<+>]>+>>]<<<<<
 # >0 d-n%d n%d n/d
```
It works when divisor >= 1, but doesn't preserve n.
I've tested it for times with n = 0 ~ 255 and d = 1 ~ 255, including extreme data.

Another version of divmod, does not preserve n. It uses 7 cells and more time to calculate, and contains 2 layers of If-Else Structure(may be optimized in future). However, it can deal with n, d = 0 ~ 255. Note that when d = 0, it returns n/d = 0 and n%d = n. All inputs have been tested out.
```
 # >n 1 d 1 0 0 0
 >+>>+<<<
 [
  [
   ->->>>>>+<<<<-[>-]>[
    >>+>[-<<<<+>>>>]<<
   ]<[-]+<<
  ]>>>[>]<<<[-]+<
 ]
 # >0 1 d-n%d 1 0 n/d n%d
```
The pictures showed its efficiency intuitively. It's obvious that versions above are faster than this. The second version's maximum number of operations is 2.30 times this.

## Fixed Version
```
 # >n d 1 0 0 0
 [->-[>+>>]>[[-<+>]+>+>>]<<<<<]
 # >0 d-n%d n%d+1 n/d 0 0
```
Works for all cell values. With division by zero treated as division by MaxCell+1.

##  Modulus algorithm

If we do not need to compute the quotient as well, the following approach is shorter than the divmod algorithm.
```
 # 0 >n 0 d 0 0 0
 [>+>->+<[>]>[<+>-]<<[<]>-]
 # 0 >0 n d-n%d n%d 0 0
```
As an additional advantage, this algorithm works even if the divisor is 1.

If n doesn't have to be preserved, the following variant can be used instead.
```
 # 0 >n d 0 0 0
 [>->+<[>]>[<+>-]<<[<]>-]
 # 0 >0 d-n%d n%d 0 0
```
## Print value of cell x as number (8-bit) 
```
 x >>++++++++++<<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>[-]>>>++++++++++<[->-[>+>>]>[+[-
 <+>]>+>>]<<<<<]>[-]>>[>++++++[-<++++++++>]<.<<+>+>[-]]<[<[->-<]++++++[->++++++++
 <]>.[-]]<<++++++[-<++++++++>]<.[-]<<[-<+>]<
```

## Summing 1~n

Copies n-1 to the cell to the right of n and n-2 to the cell to the right of that and so on until 0.
Then, sums from 1 to n.
Uses n+3 temp cells to the right of n
```
 [>+<-]>
 [[>+>+<<-]>>[-<<+>>]<-]<[[>[<+>-]]<<]
 >[<+>-]
 ```
Puts the sum from x to y(x should be set into 1) into a.

``` y[x[-a+x2+x]x2[-x+x2]x+y-]```

##  Print value of cell x as number for ANY sized cell (eg 8bit, 100000bit etc)

Improved version using updated division routine.
All used cells are cleared before and after use.
This code is a little faster than before and has been tested with very large values; but as the number of BF instructions is proportional to the number being printed anything over a couple of billion needs an interpreter that can recognise the ```[->-[>+>>]>[[-<+>]+>+>>]<<<<<]``` fragment as a divmod (taking care to ensure that the prerequisites are met).
```
 // Print value
 // Cells used: V Z n d 1 0 0 0
 // V is the value you need to print; it is not modified
 // Z is a zero sentinal and tmp
 // All cells Z and up are cleared by this routine
 
 >[-]>[-]+>[-]+<                         // Set n and d to one to start loop
 [                                       // Loop on 'n'
     >[-<-                               // On the first loop
         <<[->+>+<<]                     // Copy V into N (and Z)
         >[-<+>]>>                       // Restore V from Z
     ]
     ++++++++++>[-]+>[-]>[-]>[-]<<<<<    // Init for the division by 10
     [->-[>+>>]>[[-<+>]+>+>>]<<<<<]      // full division
     >>-[-<<+>>]                         // store remainder into n
     <[-]++++++++[-<++++++>]             // make it an ASCII digit; clear d
     >>[-<<+>>]                          // move quotient into d
     <<                                  // shuffle; new n is where d was and
                                         //   old n is a digit
     ]                                   // end loop when n is zero
 <[.[-]<]                                // Move to were Z should be and
                                         // output the digits till we find Z
 <                                       // Back to V
```

This alternative runs about a quarter as many BF instructions and is shorter. However, a normally optimising interpreter runs it at about the same speed. It requires about three times as many already cleaned cells two of which are to the left of the cell to be printed. All cells, including the value printed, are cleared after use.
```

 >> x
 >+
 [[-]<
   [->+<
     [->+<[->+<[->+<[->+<[->+<[->+<[->+<[->+<
       [->[-]>>+>+<<<]
     ]]]]]]]]<
   ]>>[>]++++++[-<++++++++>]>>
 ]<<<[.[-]<<<]
```
##  String to byte
Convert a string to a byte.
The string is a list of characters in the following format:
```
 0 0 49 48 48 0
 R ^
 R = Pointer at the end of the algoritm (Result)
 ^ = Pointer at the start of the algorithm
```
This algorithm will not check if the string is a number.
It supports up to 3 digits, but is modulair, allowing the programmer to easily support more digits.
Result will be placed one cell before the string.
```
 >------------------------------------------------[<<+>>-]>
 [
     <<<
     [<+>-]<
     [>++++++++++<-]>
     >>>
     ------------------------------------------------
     [<<<+>>>-]>
     [
         <<<<
         [<+>-]<
         [>++++++++++<-]>
         >>>>
         ------------------------------------------------
         [<<<<+>>>>-]
     ]
     <
 ]
 <<<
```
## Input a decimal number

Value is input into the current cell, uses three more cells to the right.
End of the number is a newline, or eof. All other character are treated the same as digits.
Works correctly with bignum cells.
```
    [-]>[-]+    // Clear sum
    [[-]                // Begin loop on first temp
    >[-],               // Clear the inp buffer to detect leave on eof and input
        [
            +[                          // Check for minus one on eof
                -----------[            // Check for newline
                    >[-]++++++[<------>-]       // Subtract 38 to get the char in zero to nine
                    <--<<[->>++++++++++<<]      // Multiply the existing value by ten
                    >>[-<<+>>]          // and add in the new char
                <+>]
            ]
        ]
    <]
    <
    // Current cell is the number input
```
## Count up with step x, from y to infinity
```
 x[[-y+temp+x]temp[-y+x+temp]x]
```
## while(c=getchar()!=X)
Uses X to represent the getchar-until char. Needs overflow and underflow in TIO.
Preserves result(equal 0, unequal 1)in t1. Preserves x and y.
```
yXx+[,[-t1+t3+x]y[-t2+t4+y]t1[-x+t1]t2[-y+t2]t3[-t4+t3]t4[++t3]t4[-t1+t4]t1]
```