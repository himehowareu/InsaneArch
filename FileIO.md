# File IO
## Hardweare
There will be a SD card attached to the board. this will be used for storage. It will be accessed through a register, using the SD card api. This api will be handed with a small subsystem that will talk to the SD card and future storage devices. Having a storage system that can be used to save and load data from will allow us to write larger programs as they can be dynamically loaded as well as let us write a native compiler.
## SD Card API
### System
On start up of the computer the sd card will be setup. The api will wait for a command packet to be sent from the register that it is listening on. 
### Commands
Commands will be sent in bites to the api. This way I can send arguments to the commands.


| OP | Command | Description |
|---|---|---|
| 1 | [NEW](#NEW) | Make a  new file or folder |
| 2 | [DELETE](#DELETE) | Deletes a file or folder |
| 3 | [LIST](#LIST) | Returns the number of file and folders in the current dir|
| 4 | [NAME](#NAME) | Gets the name of a File or folder |
| 5 | [WRITE](#WRITE) | Writes to a file|
| 6 | [READ](#READ) | Reads a file |
| 7 | [RENAME](#RENAME) | Rename a file or folder|
| 8 | [PWD](#PWD)| Returns the file path |
| 9 | [CD](#CD) | changer dir

For Example:

```
example filesystem
-john
-bill
-bin
test.exe
ls.exe
notes.txt
edit.exe


3 -> 3 4
when 3 is places to the port it returns the number of folders and files 
there are 3 folders and 4 files 

```

The filesystem would look like this:
|index|name|type|
|-|-|-|
| 1 | john | (1) folder |
| 2 | bill | (1) folder |
| 3 | bin | (1)folder |
| 4 | test.exe | (4) app |
| 5 | ls.exe | (4)  app |
| 6 | notes.txt | (2) text |
| 7 | edit.exe | (4) app |

## indexing 

indexing numbers are formatted as followed:

number of bytes needed to show value

```
3 200 20 2

this would return the value 135,350

```


## NEW
The new command lets me make a new file or folder on the drive in the current dir.
It takes two arguments

| Type |Number|
|------|------|
|Folder|   1  |
| File |   2  |
| Link |   3  |
| APP  |   4  |

```
 NEW  NAME LENGTH 
   V   v
   1 1 4 test
     ^     ^
  FOLDER  NAME
```
## DELETE

The delete command lets me delete a file or folder on the drive in the current dir.
It takes one arguments

```
 DELETE
   V   
   2 4
     ^
  OBJECT NUMBER
```
## LIST

The list command lets me list the number of file and folders in the current folder.

```
 list
   V   
   2

returns the listing in this format 

folders
V
2 4
  ^
files 
```

## NAME
The name commands returns the name of the target that was passed 

```
 NAME
   V
   4 1
     ^
  TARGET

Returns the name in this format 
4 john

```
## WRITE
the write command lets me either write to the start end or middle of a file.

| write to  |Number|
|------|------|
|start|   1  |
| end  |   2  |
| middle |   3  |

```
write 
V
5 1 4 < file number
  ^
start

write 
V
5 2 4 < file number
  ^
 end


write file number
  V   V
  5 3 4 2 ....
    ^   ^
  start index 

```

## READ

| write to  |Number|
|------|------|
|start|   1  |
| middle |   2  |

```
read 
V
6 1 4 < file number
  ^
 start


read file number
  V   V
  6 3 4 2 ....
    ^   ^
  middle index 

```

## RENAME
The rename command lets me rename a file or folder on the drive in the current dir.
It takes two arguments

```
 RENAME NAME
   V     V
   2 4 test
     ^
  NAME LENGTH
```
## PWD
The PWD commands returns the tree 
## CD
The CD command lets you change the dir you are in 