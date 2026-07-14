#include <stdio.h>
char **ft_split(char *str, char *charset);
int main(void){char s[] = "hello world foo"; char **r = ft_split(s, " ");if (!r){printf("NULL");return 0;}for (int i = 0; r[i]; i++) printf("[%s]", r[i]);return 0;}
