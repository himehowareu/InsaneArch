# File IO
## Hardweare
There will be a SD CArd attached to the board. this will be used for storage. It will be accessed through a register, using the SD card api. This api will be handed with a small subsystem that will talk to the SD card and future storage devices. Having a storage system that can be used to save and load data from will allow us to write larger programs as they can be dynamically loaded as well as let us write a native compiler.
## SD Card API
### System
On start up of the computer the sd card will be setup. The api will wait for a command packet to be sent from the register that it is listening on. 
### Commands
Commands will be sent in  two bite pairs, i have desired  if i want to use two registers or one yet. 

| OP | Command | Description |
|---|---|---|
| 1 | NEW FILE | Make a  new file |
| 2 | DELETE FILE | Deletes a file |
| 3 | NEW FOLDER | Make a  new folder |
| 4 | DELETE FOLDER | Deletes a folder |
| 5| LIST | Returns the number of file and folders in the current dir|
| 6 | NAME | Gets the name of a File |
| 7 | APPEND | Adds to the end of a file | 
| 8 | WRITE | Starts writing text to a file|
| 9 | RENAME | Rename a file or folder|
| 10| PWD| Returns the file path |
| 11| CD | changer dir

For Example:

``` 5 0 ```

 5 lists the dir and 0 tells  it to  list the current dir. This would return two numbers between 0-255.
This tells us how many folds and files are in the current dir.