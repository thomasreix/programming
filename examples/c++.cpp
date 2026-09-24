#include <iostream>
#include <vector>
#include <cmath>

namespace first {
int x = 1;
}

namespace second {
int x = 2;
}

typedef std::string text_t;
typedef std::vector<std::pair<std::string, int>> pairlist_t;

int main() {
  // this is a comment
  /*
    this
    is
    a
    multiline
    cmmment
  */

  std::cout << "hello world" << std::endl;
  std::cout << "newline:" << '\n';

  int x; // declaration
  x = 5; // initialization

  std::cout << "x = " << x << '\n';

  int age = 37;                    // int --> hole number
  double pi = 3.121592;            // double --> decimal number
  char grade = 'B';                // char --> single character
  bool lightswitch = true;         // bool --> boolean (true of false)
  std::string name = "programmer"; // string --> sequence of characters

  std::cout << "int: " << age << '\n';
  std::cout << "double: " << pi << '\n';
  std::cout << "char: " << grade << '\n';
  std::cout << "bool: " << lightswitch << '\n';
  std::cout << "string: " << name << '\n';

  const int LIGHT_SPEED = 299792458; // const --> declares a constant

  std::cout << '\n';

  std::cout << "local x: " << x << '\n';
  std::cout << "first x: " << first::x << '\n';

  // using namespace second;
  std::cout << "second x: " << second::x << '\n';

  std::cout << '\n';

  text_t tower = "eiffel";
  pairlist_t pairlist;

  // std::cout << '\n';

  // arthmetic operators --> returns the result of an opertatio
  //                          + - * /

  int a = 0;
  a += 5; // adition
  a -= 1; // substraction
  a *= 3; // multiplication
  a /= 2; // division
  a %= 4; // modulo

  std::cout << "a = " << a << '\n';

  // type conversion --> changes a value's datatype to an other
  //      - implicit --> automatic
  //      - explicit --> precede a value with a new datatype

  double fake_pi = (int)3.121592;
  std::cout << "fake pi = " << fake_pi << '\n';

  int character = 100;
  std::cout << "100th caracter = " << (char)character << '\n' << '\n';

  // cout << --> insertion operator
  // cin >> --> extraction operator

  std::string fruit;
  std::cout << "what is your favorite fruit: " << '\n';
  fruit = "gapple"; //std::cin >> fruit;
  std::cout << "your favorite fruit is " << fruit << '\n';

  std::string sentence;
  std::cout << "write any sentence :" << '\n';
  sentence = "the race hasn't started yet"; //std::getline(std::cin >> std::ws, sentence);
  std::cout << "sentence : " << sentence << '\n' << '\n';

  // useful math functions
  int numA = 5;
  int numB = 2;

  int numX = std::max(numA, numB);
  int numI = std::min(numA, numB);

  std::cout << numX << " is bigger than " << numI << '\n';

  // the folling functions are found with <cmath> header file
  int numP = pow(numB, numA);
  double numS = sqrt(numA);
  int numN = numA * -1;
  int numD = abs(numN);
  double numR = round(pi);
  double numC = ceil(pi);
  double numF = floor(pi);
  
  std::cout << numB << " to the power of " << numA << " is " << numP << '\n';
  std::cout << "the square root of " << numA << " is " << numS << '\n';
  std::cout << "absolute value of " << numN << " is " << numD << '\n';
  std::cout << pi << " rounded is " << numR << '\n';
  std::cout << "the ceilling of " << pi << " is " << numC << '\n';
  std::cout << "the floor of " << pi << " is " << numF << '\n';

  std::cout << '\n';


  double sideA = 2;
  double sideB = 5;
  double sideC = sqrt(pow(sideA, 2) + pow(sideB, 2));

  std::cout << "a right triangle with agasent sides lenth " << sideA << " and " << sideB << " has a hypotenus of " << sideC << '\n';

  
  std::cout << '\n';
  return 0;
}