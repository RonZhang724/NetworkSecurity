#include <unistd.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#define PORT 8080

int main(){
  char string[1000] = "attack_string";

  //create a socket
  int network_socket;
  network_socket=socket(AF_INET,SOCK_STREAM,0);

  //specify an address for the socket
  struct sockaddr_in server_address;
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(9999);
  server_address.sin_addr.s_addr=INADDR_ANY;
  
  // keep establishing connection and send messages to server
  while(1) {
    // send the user input to server
    // printf("Sending stuff");
    connect(network_socket, (struct sockaddr *) & server_address, sizeof(server_address));
    // send(network_socket, string, sizeof(string), 0);
    //receive data from the server
    // char response[256];
    // recv(network_socket, &response, sizeof(response), 0);
    
    //print out the server's response
    // printf("Here is the message from the server: %s\n\n", response);
  }

  //close the socket
  close(network_socket);
	
  return 0;
}
