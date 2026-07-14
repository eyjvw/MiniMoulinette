void ft_putstr_non_printable(char *str);
int main(void){char s[] = "\x01\x02\x03"; ft_putstr_non_printable(s);return 0;}
