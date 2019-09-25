#include <stdio.h>
int main()
{
  FILE *fptr;
  fptr = fopen("../data/simple.txt","w");
 
  if(fptr == NULL)
    {
      printf("Error!");
      return 1;
    }
 
  fprintf(fptr,"%s","Hello World!");
  fclose(fptr);
   
  char c; 
  // Open file 
  fptr = fopen("../data/secret.txt", "r"); 
  if (fptr == NULL) { 
      printf("Cannot open file \n"); 
      return 1; 
  } 
  
  // Read contents from file 
  c = fgetc(fptr); 
  while (c != EOF) { 
    printf ("%c", c); 
    c = fgetc(fptr); 
  } 
  
  fclose(fptr);

  return 0;
}
