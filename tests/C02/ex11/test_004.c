void ft_putstr_non_printable(char *str);
int main(void){char s[] = "mix\x7f" "ed"; ft_putstr_non_printable(s);return 0;}
