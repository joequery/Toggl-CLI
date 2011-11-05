# TODO

This file contains a list of all the changes/improvements I would like to make to the CLI by category.

## Interface
* Get rid of ~/.toggl and ~/.toggl_project files entirely.
* Allow for login via command line arguments
* If no recent tasks/entries, don't display
* Make menus scrollable via j and k (like VIM)
* Allow for "Return to (m)enu" option when choosing recent entry
* Live Timer
* Allow user to select project and client from interface

## Exception Handling
* Invalid selection in recent entries shouldn't exit the program
* Invalid menu selection shouldn't exit program
* Catch keyboard interrupts in the following places
    * New Time Entry



## Back-end
* Immediately check login credentials when program starts
* To avoid lost data, send data to server every X minutes
* Modularization of Code

