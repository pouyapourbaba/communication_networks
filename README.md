# Project Title

The course work of the Communication Networks, which simulates the situation where client and server define communication parameters using reliable TCP connection and then exchange data using UDP.
These files are for the client side.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project was done using python3. No additional plugin are required.

### Installing python3

On GNU/Linux :
Check if you have python3 installed with the following command.
```
python3 --version
```
If you have a result then you can proceed to the next section.
If not then you have to install python3.
On Debian based distribution (like Ubuntu) :
```
sudo apt-get update && sudo apt-get install python3
```
On windows :
Check if you have python3 installed.
You can use the program search and look for python3.
If not then you can install it from this link:
```
https://www.python.org/downloads/release/python-371/
You can use Windows x86-64 executable installer for example
Adding Python to path in the installer is recommended. This allow python to be called from windows command line.
```

## Using the program

Unzip the files to your favorite location.
Open a command line and move to the directory you extracted the files in
You can now launch the program using the following command
On GNU/Linux:
```
python3 network.py --host 87.92.113.80 --port 10000
```
On Windows:
```
python network.py --host 87.92.113.80 --port 10000
```

"--host" let you select the IP address of the server you want to connect to. In the above example we used the address of the haapa7 server we were given to practise.
"--port" let you select the port of the server you want to connect to. In the above example we used the port of the haapa7 server we were given to practise.


If you get the following results then everything went as intended:
```
You replied to 8 messages with 2 features. Bye.
```

For unknown reason, you might encounter an Error message. 
This is most likely due to an error from the server. An other group had this problem and could not solve it either.
This is due to the letter "e" at the end of the last word of the list, not being decrypted correctly.

## Authors

Pouya Pourbaba 2473693 pouya.pourbaba@student.oulu.fi
Maureen Boudart	2591892 maureen.boudart@student.oulu.fi
Guilhem Egrot 593081 gegrot18@student.oulu.fi
