// C programming tutorial, full course by Bro Code
// https://www.youtube.com/watch?v=xND0t1pr3KY

#include "strutils.h"
#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

void routine() {
  printf("\nbreath in");
  printf("\nbreath out");
}

void hello(char name[]) { printf("\nhello %s", name); }

int square(int n) {
  int square_n = pow(n, 2);
  return square_n;
}

void sort(int array[], int size) {
  for (int i = 0; i < size - 1; i++) {
    for (int j = 0; j < size - 1; j++) {
      if (array[j] > array[j + 1]) {
        int temp = array[j];
        array[j] = array[j + 1];
        array[j + 1] = temp;
      }
    }
  }
}

void printArray(int array[], int size) {
  for (int i = 0; i < size; i++) {
    printf("%d ", array[i]);
  }
}

void printCharArray(int array[], int size) {
  for (int i = 0; i < size; i++) {
    printf("%c ", array[i]);
  }
}

struct Player {
  char name[16];
  int score;
};

typedef char user[25];

typedef struct {
  char name[25];
  char password[16];
  int id;
} User;

struct Student {
  char name[16];
  float gpa;
};

enum Day { Mon = 1, Tue = 2, Wed = 3, Thu = 4, Fri = 5, Sat = 6, Sun = 0 };

int main() {
  // this is a comment
  /*
      this
      is
      a
      multiline
      cmmment
  */

  printf("hello world \n");
  printf("newline: \n");                    // add a newline with \n
  printf("tab_1:\ttab_2:\ttab_3:\t \n");    // add a tab with \t
  printf("\"quote\" is quoted \n");         // add a quote with \"
  printf("nul character: \0 \n\n\n\n\n\n"); // add a nul character with \0"

  int x;     // declaration
  x = 1;     // initialization
  int y = 2; // declaration and initialization

  char language = 'C';     // single character      %c
  char compiler[] = "gcc"; // array of characters   %s

  printf("\n\nyou compile %c with %s \n", language, compiler);

  bool b = true;             // 1 byte (true or false)       %d
  char c = 100;              // 1 byte (-128 to +127)        %d or %c
  unsigned char uc = 255;    // 1 byte (0 to +255)           %d or %c
  short s = 32767;           // 2 bytes (-32768 to +32767)   %d
  unsigned short us = 65535; // 2 bytes (0 to +65535 x
  float f = 3.121592; // 4 bytes (32 bits of precision) 6 - 7 digits      %f
  double d =
      3.121592653589793; // 8 bytes (64 bits of precision) 15 - 16 digits %lf
  int i = 2147483647;    // 4 bytes (-2147483648 to +2147483647)             %d
  unsigned int ui = 4294967295; // 4 bytes (0 to +4294967295) %d
  long long int l =
      9223372036854775087; // 8 bytes (-9quintillion to +9quintillion) %lld
  unsigned long long int ul =
      18446744073709551615U; // 8 bytes (0 to +18 quintillion) %llu

  printf("float: %f \n", f);
  printf("double: %0.15lf \n", d);
  printf("boolean: %d\n", b);
  printf("ascii of %c is %d \n", c, c);
  printf("float: %f \n", f);
  printf("double: %0.15lf \n", d);
  printf("short: %d \n", s);
  printf("unsigned short: %d \n", us);
  printf("integer: %d \n", i);
  printf("unsigned integer: %d \n", ui);
  printf("long:%lld \n", l);
  printf("unsigned long:%llu \n\n", ul);

  const float PI = 3.121592; // when const is used the variable can't be changed

  float item1 = 5.75;
  float item2 = 10.00;
  float item3 = 21.20;

  printf("item 1: $%-.2f \n", item1);   //%.1 = deciaml precision
  printf("item 2: $%-.2f \n", item2);   //%1 = minimul field width
  printf("item 3: $%-.2f \n\n", item3); //%- = left align
  printf("item 1: %5.2f€ \n", item1);   //  right when none specified
  printf("item 2: %5.2f€ \n", item2);
  printf("item 3: %5.2f€ \n", item3);

  int calc_x = 5;
  int calc_y = 2;

  int calc_c =
      calc_x / (float)calc_y; // have to use float to get decimal precision
  float calc_d = calc_x / (float)calc_y;

  printf("\nint division %-d\n", calc_c);
  printf("float division %-.1f\n", calc_d);

  calc_x += 7;
  calc_x *= 4;
  calc_x -= 3;
  calc_x /= 5;
  calc_x %= 6;

  printf("augmented assignment aperators result: %d\n", calc_x);

  //     int age;
  //     char name[16]; // 16 bytes
  //
  // 	fgets(name, 16, stdin);
  // 	name[strlen(name)-1] = '\0';
  //
  //     printf("\ntype your age: ");
  //     scanf("%d", &age);
  //     printf(", you are %d years old", age);
  //
  //     printf("\ntype your name: ");
  //     scanf("%s", &name);
  //     printf(", your name is %s", name);

  double N = -16.0;
  double S = sqrt(N);
  double P = pow(N, 4);
  double R = round(PI);
  int C = ceil(PI);
  int F = floor(PI);
  double A = fabs(N);
  double L = log(N);

  printf("\nthe sqrt of %.2lf is %.2lf", N, S);
  printf("\n%.2lf to the fourth power is %.2lf", N, P);
  printf("\n%.2lf is rounded to %.2lf", PI, R);
  printf("\nthe ceilling of %.2lf is %d", PI, C);
  printf("\nthe floor of %.2lf is %d", PI, F);
  printf("\nthe obsolute value of %lf is %lf", N, A);
  printf("\nlog of %lf is %lf\n", N, L);

  double radius;
  double circonference;
  double area;

  printf("\nenter the radius of a circle: ");
  // scanf("%lf", &radius);
  radius = 1;
  printf("%lf", radius);

  circonference = 2 * PI * radius;
  area = PI * radius * radius;

  printf("\ncircumference: %lf", circonference);
  printf("\narea: %lf\n", area);

  double sideA = 5;
  double sideB = 10;
  double sideC;

  sideC = sqrt(pow(sideA, 2) + pow(sideB, 2));

  printf("a right triangle with %lf and %lf as adjacent sides has %lf as "
         "hypotenus\n",
         sideA, sideB, sideC);

  int insects = 6;
  int spiders = 8;
  int crustaceans = 10;

  int arthropodA = 10;
  int arthropodB = 6;
  int arthropodC = 8;

  int legs;

  if (arthropodA == insects) {
    printf("\narthropodA is an insect");
  } else if (arthropodA == spiders) {
    printf("\narthropodA is a spider");
  } else {
    printf("\narthropodA is a crustacean");
  }
  if (arthropodB == insects) {
    printf("\narthropodB is an insect");
  } else if (arthropodB == spiders) {
    printf("\narthropodB is a spider");
  } else {
    printf("\narthropodB is a crustacean");
  }
  if (arthropodC == insects) {
    printf("\narthropodC is an insect");
  } else if (arthropodC == spiders) {
    printf("\narthropodC is a spider");
  } else {
    printf("\narthropodC is a crustacean");
  }

  printf("\n");

  // switch is a more efficient alternative to using many "else if"
  // statements it allows a value to be tested foe equality againt many
  // cases

  char grade;
  grade = 'C';

  printf("\nyour grade is ");

  switch (grade) {
  case 'A':
    printf("perfect");
    break;
  case 'B':
    printf("good");
    break;
  case 'C':
    printf("okay");
    break;
  case 'D':
    printf("disapointing");
    break;
  case 'F':
    printf("failed");
    break;
  default:
    printf("not valid");
    break;
  }

  printf("\n");

  char unit;
  float temperatureC;
  float temperatureF;

  unit = 'c';
  unit = toupper(unit); // turns any carracter uppercase

  temperatureC = 100;
  temperatureF = 100;

  if (unit == 'C') {
    temperatureF = (temperatureC * 9 / 5) + 32;
    printf("\n%.2fF in celcus is %.2fC", temperatureF, temperatureC);
  } else { // unit == 'F'
    temperatureC = ((temperatureF - 32) * 5) / 9;
    printf("\n%.2fC in farenheit is %.2fF", temperatureC, temperatureF);
  }

  printf("\n");

  char operator;
  double num1;
  double num2;
  double result;

  operator = '/';

  num1 = 40;
  num2 = 9;

  switch (operator) {
  case '+':
    result = num1 + num2;
    printf("\n%.2lf + %.2lf = %.2lf", num1, num2, result);
    break;
  case '-':
    result = num1 - num2;
    printf("\n%.2lf - %.2lf = %.2lf", num1, num2, result);
    break;
  case '*':
    result = num1 * num2;
    printf("\n%.2lf * %.2lf = %.2lf", num1, num2, result);
    break;
  case '/':
    result = num1 / num2;
    printf("\n%.2lf / %.2lf = %.2lf", num1, num2, result);
    break;
  default:
    printf("\n%c is not valid", operator);
  }

  printf("\n");

  // logical operators :
  // 		and: && --> checks if two conditions are true
  // 		or:  || --> checks if at least one condition is true
  // 		not: !  --> reverses the state of a condition

  float habitable_zone_start = 138;
  float habitable_zone_end = 161;

  float planetA = 129;
  float atmosphereA = true;
  float planetB = 154;
  float atmosphereB = true;
  float planetC = 192;
  float atmosphereC = false;

  if (planetA > habitable_zone_start && planetA < habitable_zone_end &&
      atmosphereA == true) {
    printf("\nplanetA is habitable");
  } else {
    printf("\nplanetA is not habitable");
  }
  if (planetB > habitable_zone_start && planetB < habitable_zone_end &&
      !!atmosphereA == 1) {
    printf("\nplanetB is habitable");
  } else {
    printf("\nplanetB is not habitable");
  }

  if (planetC < habitable_zone_start ||
      planetC > habitable_zone_end && !atmosphereA) {
    printf("\nplanetC is habitable");
  } else {
    printf("\nplanetC is not habitable");
  }

  printf("\n");

  routine();
  routine();
  routine();

  printf("\n");

  char name[] = "michael";
  hello(name);

  printf("\n");

  // return: returns a value back to a calling function

  int n = 8;
  int square_n = square(n);
  printf("\nthe square of %d is %d", n, square_n);

  printf("\n");

  // ternary operator: shortcut to if/else when assigning/returning a value
  //	(condition) ? value if true : value if false

  x = 5;
  y = 8;

  int max = (x > y) ? x : y;
  int min = (x < y) ? x : y;

  printf("\n%d is bigger than %d", max, min);

  printf("\n");

  char stringA[16] = "baguette";
  char stringB[16] = "PIZZA";

  char uppercase[16];
  strcpy(uppercase, stringA); // strcpy(str2, str1) --> copy str2 to str1
  strupr(uppercase);          // strupr(str) --> converts a str to uppercase
  printf("\nuppercase: %s", uppercase);

  char lowercase[16];
  strcpy(lowercase, stringB);
  strlwr(lowercase); // strlwr(str) --> converts a str to lowercase
  printf("\nlowercase: %s", lowercase);

  char appended[16];
  strcpy(appended, stringA);
  strcat(appended,
         stringB); // strcat(str1, str2) --> appends str2 at the end of str1
  printf("\nappended strings: %s", appended);

  char appended_n[16];
  n = 4;
  strcpy(appended_n, stringA);
  strncat(
      appended_n, stringB,
      n); // strcat(str1, str2, n) --> appends n carracters from str2 to str1
  printf("\n%d carracters have been happended to %s", n, appended_n);

  char copy_n[16];
  strcpy(copy_n, stringA);
  strncpy(copy_n, stringB,
          n); // strncpy(str1, str2, n) --> copy n carracters of str2 to str1
  printf("\n%d carracters have been copied to %s", n, copy_n);

  char set[16];
  char character = '?';
  strcpy(set, stringA);
  strset(set, character); // strset(str, char) --> sets all characters of a
                          // string to char
  printf("\nevery character of %s have been replaced with %c to get %s",
         stringA, character, set);

  char set_n[16];
  character = '!';
  strcpy(set_n, stringA);
  strnset(set_n, character, n); // strnset(str, char, n) --> sets the first n
                                // characters of str to char
  printf("\nthe first %d character of %s have been replaced with %c to get %s",
         n, stringA, character, set_n);

  char reversed[16];
  strcpy(reversed, stringA);
  strrev(reversed); // strrev(str) --> reverses str
  printf("\n%s in reversed is %s", stringA, reversed);

  int lenth =
      strlen(stringA); // strlen(str) --> returns the lenth of str as an int
  printf("\n%s is %d characters long", stringA, lenth);

  int compare = strcmp(
      stringA, stringB); // strcmp(str1, str2) --> compares all characters
  if (compare == 0) {
    printf("\n%s and %s are the same string", stringA, stringB);
  } else {
    printf("\n%s and %s are not the same string", stringA, stringB);
  }

  int compare_n = strncmp(stringA, stringB,
                          n); // strcmp(str1, str2, n) --> compares n characters
  if (compare_n == 0) {
    printf("\nthe %d starting characters of %s and %s are the same\n", n,
           stringA, stringB);
  } else {
    printf("\nthe %d starting characters of %s and %s are not the same\n", n,
           stringA, stringB);
  }

  printf("\n");

  // for loop --> repeats a section of code a limited amout of times

  for (int i = 0; i < 10; i += 2) {
    printf("%d ", i);
  }

  printf("\n");

  // while loop --> repeats a section of code possibly unlimited times

  i = 0;
  while (i < 10) {
    printf("%d ", i);
    i += 2;
  }

  printf("\n");

  // do while loop --> executes the block of code before checking the
  // condition

  i = 0;
  do {
    printf("\%d ", i);
    i += 2;
  } while (i < 10);

  printf("\n\n");

  // nested loop --> a loop inside of an other loop

  int rows = 4;
  int cols = 7;
  for (int x = 0; x < rows; x++) {
    for (int y = x; y < cols + x; y++) {
      printf("%d ", y);
    }
    printf("\n");
  }

  printf("\n");

  // continue --> skips the rest of the code and forces the rest iteration of
  // the loop break --> exits a loop/switch

  for (int i = 1; i <= 20; i++) {
    if (i % 4 == 3) {
      continue;
    }
    if (i == 13) {
      break;
    }
    printf("%.2d ", i);
  }

  printf("\n");

  // array --> data structure that can store many values of the same data type

  char label[] = "potatoes";

  double prices[5] = {5.0, 10.0, 25.0};
  prices[4] = 100.0;
  prices[5] = 115.0;

  printf("\nthe size of prices is %ld bytes",
         sizeof(prices)); // sizeof() --> gets the size in bytes

  int len_prices = sizeof(prices) / sizeof(prices[0]);
  printf("\nthe lenth of prices is %d\n", len_prices);

  for (int i = 0; i < len_prices; i++) {
    printf("$%.1lf ", prices[i]);
  }

  printf("\n");

  // 2D array --> an array where each element is an other array

  int numbers[2][3] = {{1, 0, 3}, {4, 5}};
  numbers[0][1] = 2;
  numbers[1][2] = 6;

  rows = sizeof(numbers) / sizeof(numbers[0]);
  cols = sizeof(numbers[0]) / sizeof(numbers[0][0]);

  printf("\nour 2D array has %d rows and %d cols\n\t", rows, cols);

  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      printf("%d ", numbers[i][j]);
    }
    printf("\n\t");
  }

  // string arrays

  char cars[][10] = {"Mustang", "Corvette", "Camaro"};
  strcpy(cars[0], "Tesla");

  for (int i = 0; i < sizeof(cars) / sizeof(cars[0]); i++) {
    printf("\n%s", cars[i]);
  }

  printf("\n");

  // swaping the values of two variables

  char varA = 'A';
  char varB = 'B';

  printf("\nvarA is %c and varB is %c", varA, varB);

  char temp;
  temp = varA;
  varA = varB;
  varB = temp;

  printf("\nvarA is %c and varB is %c", varA, varB);

  printf("\n\n");

  // sorting array elements

  int array[] = {9, 1, 8, 2, 7, 3, 6, 4, 5};
  int arraySize = sizeof(array) / sizeof(array[0]);

  sort(array, arraySize);
  printArray(array, arraySize);

  printf("\n");

  int charArray[] = {'D', 'G', 'V', 'Q', 'M', 'A', 'P', 'N', 'Y'};
  int charArraySize = sizeof(charArray) / sizeof(charArray[0]);

  sort(charArray, charArraySize);
  printCharArray(charArray, charArraySize);

  printf("\n");

  // struct

  struct Player player1;
  struct Player player2;

  strcpy(player1.name, "jeremiah");
  player1.score = 44;

  strcpy(player2.name, "yahweh");
  player2.score = 70;

  printf("\n%s has %d points", player1.name, player1.score);
  printf("\n%s has %d points", player2.name, player2.score);

  printf("\n");

  // typedef --> reseved keyword that gives an existing datatype a "nickname"

  char user1[25] = "donald";
  user user2 = "elson";

  User user3 = {"flunted", "Password123.", 86};

  printf("\n%s's password is %s, his id is %d", user3.name, user3.password,
         user3.id);

  printf("\n");

  // struct array

  struct Student studentA = {"alpam", 4.2};
  struct Student studentB = {"brice", 2.2};
  struct Student studentC = {"clian", 2.8};
  struct Student studentD = {"dungo", 1.5};

  struct Student students[] = {studentA, studentB, studentC, studentD};

  int sizeOfStudents = sizeof(students) / sizeof(students[0]);
  struct Student student;
  for (int i = 0; i < sizeOfStudents; i++) {
    student = students[i];
    printf("\n%s has a gpa of %.1f", student.name, student.gpa);
  }

  printf("\n");

  // enum --> a user difined typr of named integer identifiers
  // 			short for enumerator it helps to make a code clean

  enum Day today = Wed;

  char days[][16] = {"monday", "tuesday",  "wednesday", "thursday",
                     "friday", "saturday", "sunday"};

  if (today == Sun || today == Sat) {
    printf("\n%s is a good day", days[today - 1]);
  } else {
    printf("\n%s id a bad day", days[today - 1]);
  }

  printf("\n");

  // pseudo random numbers --> A set of values or elements that are
  // statistically random

  srand(time(0));

  // rand() --> gives a random number from 0 to 32767
  int rollA = (rand() % 6) + 1;
  int rollB = (rand() % 6) + 1;
  int rollC = (rand() % 6) + 1;

  printf("\ndiceA = %d", rollA);
  printf("\ndiceB = %d", rollB);
  printf("\ndiceC = %d", rollC);

  printf("\n");
  int z;

  // BITWISE operators --> special operators used in bit level programming
  //		&  --> and
  //		|  --> or
  //		^  --> xor
  //		<< --> left shift
  //		>> --> right shift

  x = 6;  // 6  = 00000110
  y = 12; // 12 = 00001100
  z = 0;  // 0  = 00000000

  z = x & y; // 00000100
  printf("\n%d and %d is %d", x, y, z);

  z = x | y; // 00001110
  printf("\n%d or %d is %d", x, y, z);

  z = x ^ y; // 00001010
  printf("\n%d xor %d is %d", x, y, z);

  z = x << 1; // 00001100
  printf("\n%d shifted left by one is %d", x, z);

  z = x << 2; // 00011000
  printf("\n%d shifted left by two is %d", x, z);

  z = x >> 1; // 00011000
  printf("\n%d shifted right by one is %d", x, z);

  z = x >> 2; // 00011000
  printf("\n%d shifted right by two is %d", x, z);

  printf("\n");

  // address

  char nA = 'A';
  char nB = 'B';
  char nC = 'C';

  printf("\naddress of a is %p", &nA);
  printf("\naddress of b is %p", &nB);
  printf("\naddress of c is %p", &nC);

  printf("\n");

  // pointers
  // & --> used to get the address
  // * --> used to get the value at address

  int networth = 840;
  int *pNetworth = &networth;

  printf("\nnetworth value: %dM", networth);
  printf("\naddress of networth: %p", &networth);
  printf("\nnetworth value at address: %dM", *pNetworth);

  printf("\n\n");

  // write to a file
  // w --> write
  // a --> append
  // r --> read

  FILE *pF = fopen("text.txt", "w");

  fprintf(pF, "first line\n");

  fclose(pF);

  pF = fopen("text.txt", "a");

  fprintf(pF, "second line");

  fclose(pF);

  pF = fopen("text.txt", "r");
  char buffer[255];

  while (fgets(buffer, 255, pF) != NULL) {
    printf("%s", buffer);
  }

  fclose(pF);

  printf("\n");

  if (remove("text.txt") == 0) {
    printf("\ntext.txt was removed");
  } else {
    printf("\ntext.txt doesnt exist");
  }

  printf("\n");

  // malloc() --> a function in C that dynamically allocates
  //              a specified number of bytes in memory

  int wheels = 4;
  char *vehicule = malloc(wheels * sizeof(char));

  if (vehicule == NULL) {
    printf("memory allocation failed");
    return 1;
  }

  free(vehicule);  // returns space back
  vehicule = NULL; // avoids dangling pointers

  // calloc() --> allocates memory dynamicly and sets all alocated bytes to 0

  // int players = 10;

  // int *scores = calloc(players, sizeof(int));

  // if (*scores == NULL) {
  //   printf("memory allocation failed");
  //   return 1;
  // }

  // free(scores);
  // scores = NULL;

  // realloc() --> reallocation resize previously allocated memory

  // DIGITAL CLOCK

  time_t rawtime = 0; // Jan 1, 1970 (Epoch)
  struct tm *pTime = NULL;

  printf("\nDIGITAL CLOCK\n");

  bool isRunning = true;
  while (isRunning) {
    time(&rawtime);
    pTime = localtime(&rawtime);

    printf("\r%02d:%02d:%02d", pTime->tm_hour, pTime->tm_min, pTime->tm_sec);

    fflush(stdout);

    sleep(1);
  }

  printf("\n");
  return 0;
}
