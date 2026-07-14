#include <stdio.h>
char **ft_split(char *str, char *charset);
int main(void){char s[] = "mix\tof\ndifferent seps"; char **r = ft_split(s, " \t\n");if (!r){printf("NULL");return 0;}for (int i = 0; r[i]; i++) printf("[%s]", r[i]);return 0;}
