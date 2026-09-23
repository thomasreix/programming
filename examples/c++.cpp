#include <iostream>
#include <vector

namespace first {
int x = 1;
}

namespace second {
int x = 2;
}

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

  s

  return 0;
}