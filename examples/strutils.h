#ifndef STRUTILS_H
#define STRUTILS_H

#include <ctype.h>
#include <stddef.h>

char *strlwr(char *str)
{
    for (char *p = str; *p; p++)
        *p = tolower((unsigned char)*p);

    return str;
}

char *strupr(char *str)
{
    for (char *p = str; *p; p++)
        *p = toupper((unsigned char)*p);

    return str;
}

char *strset(char *str, int c)
{
    for (char *p = str; *p; p++)
        *p = c;

    return str;
}

char *strnset(char *str, int c, size_t n)
{
    for (char *p = str; *p && n > 0; p++, n--)
        *p = c;

    return str;
}

char *strrev(char *str)
{
    char *start = str;
    char *end = str;

    while (*end)
        end++;

    if (end != str)
        end--;

    while (start < end)
    {
        char temp = *start;
        *start = *end;
        *end = temp;

        start++;
        end--;
    }

    return str;
}

#endif
