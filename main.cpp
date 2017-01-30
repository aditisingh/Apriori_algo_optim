#include <fstream>
#include <iostream>
#include <stdio.h>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <ctime>
#include <vector>
#include <algorithm>

using namespace std;

int main(int argc, char* argv[])
{
  
  if(argc != 4) //there should be three arguments
  {
    cout<<" program_name image_name num_superpixels control_constant"<<endl;
    return 1; 
  }//

  int min_sup=atoi(argv[1]);
  int k=atoi(argv[2]);

  string line;
  string word;
  ifstream myfile (argv[3]);
  
  if (myfile.is_open())
  {
    while ( getline (myfile,line) )
    {
      cout << line << '\n';
      istringstream iss(line);
      iss>>word;
      while(iss)
      {
        cout<<word<<" \t";
        iss>>word;
      }
      cout<<"\n";
    }
    myfile.close();
  }

  else cout << "Unable to open file"; 


  return 0;
}
