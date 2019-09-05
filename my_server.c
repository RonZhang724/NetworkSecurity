#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include <string.h>
#include <ctype.h>

int main()
{
    char string[1000];

    // create the server socket
    int server_socket;
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    
    // define the server address
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(9999);
    server_addr.sin_addr.s_addr = INADDR_ANY;
    
    //bind the socket to the specified IP addr and port
    bind(server_socket, (struct sockaddr*) &server_addr, sizeof(server_addr));
    
    listen(server_socket, 3);
    
    int client_socket;
    while(1) {
      // accept new connection on socket
      client_socket = accept(server_socket, NULL, NULL);
    
      // recieve the message from client 
      recv(client_socket, string, sizeof(string), 0);
    
      // convert the message to uppercase 
      int i = 0;
  
      while(string[i]) {
        string[i] = toupper(string[i]);
        i++;
      }
 
      // send the message
      send(client_socket, string, sizeof(string), 0);
    }
    // close the socket
    // close(server_socket);
 
    return  0;
}
