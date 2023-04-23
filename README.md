--------------------------------------------------------------------------------------------------------------
 							SECURED STORAGE
--------------------------------------------------------------------------------------------------------------

The application is working like peer-to-peer communication, but for the setting a comunication between clients
is used server. Server is working on virtual machine with a storage client. The storage can store files max. to 65kB 
and text files in format *.txt

--------------------------------------------------------------------------------------------------------------
Preparations

Application is programmed in a Python 3.11.

To run application, it is necessary to have two PCs in one network or have a Windows 11 virtual machine installed on your PC.
The PCs need to communicate between each other.

Steps to do:
1) Install a Python 3.11.
2) Optional - Install IDE (recommended PyCharm 2022.3.3)
3) Install all neccesarry libraries in the requirements.txt file
	- Win+R -> CMD -> pip install -r requirements.txt
4) Check the IPv4 of the second PC/virtual machine and noted it down
	- Win+R -> CMD -> ipconfig
	
Note: If the 3) does not work through command line try this bellow (for PyCharm) <br>
 - Open IDE -> File -> Settings -> Project:Project -> Python Interpereter -> "+" -> Type name of library -> Install Package

--------------------------------------------------------------------------------------------------------------

Setting up a communication

1) Start a server.py
2) Start a storage.py
	- there is neccesary to change the server address on line 20 with the IPv4 address from step 4)
3) Lastly start a App.py (this is client application)
	- now it is neccesarry to insert a IPv4 address of the server and experimental port "55555"
	- succesfull connection is after login form is displayed

--------------------------------------------------------------------------------------------------------------

Login to a storage

1) Once a login form is shown, there are two users that have access to the storage <br>
	 - username: Admin <br>
	 - password: admin <br><br>
	 - username: User <br>
	 - password: 123


--------------------------------------------------------------------------------------------------------------

Now you are signed in into a storage of one of the users. There are multiple functions that you can try!
In Client App/Test_files directory you can find testing files to test the storage functionality.

Note: To see changes in storage you need to double click "home" button after applying functions (upload or delete)


--------------------------------------------------------------------------------------------------------------

Logs

After every opperation every action is saved into a log file in admins storage. Hash of this log file(Logs.txt) is stored 
in another file (hash_logs.txt). Admin can easily verify and compare log file with hash of this file to see if there were any changes
in the log file

--------------------------------------------------------------------------------------------------------------
