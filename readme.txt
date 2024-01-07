This set of python programs will run client and server processes for a TFTP 
implementation over TCP. The client and server programs have file reading and 
writing capabilities between the two. The user will select a file to be written/read 
to/from the server from the client side. The server will be run first, waiting 
for a client connection. After a connection is established, the client will run 
the desired function with the server, either reading and copying a file from 
the server, or writing a file to the server. The client and server programs are 
executed over the command line with flag arguments. The server only needs a port
number to be passed in, along with the "&" symbol at the end to run the server 
process in the background. The client program takes in a port number, filename,
mode for reading/writing, and the clinet-side IP. The desired file to be read/written
must be in the same directory as the client and server program files. The client
or server will make a copy of the file used under an altered name.

The flags for each argument passed to the programs are: 
	"-p" for port number
	"-f" for filename
	"-m" for mode, "r" for reading from the server, "w" for writing to the server
	"-i" for the client's IP

Here is an example for running the client and server programs...
First: Compile the Packet.py class
	>>> python Packet.py
Second: Run the server with the desired port in the background
	>>> python TFTPServer.py -p 12001 &
Third: Run the client with the same port as the server, the desired file to be 
	read/written, the mode, and the client-side IP
	>>> python TFTPClient.py -p 12001 -f filename -m r -i (your IP)