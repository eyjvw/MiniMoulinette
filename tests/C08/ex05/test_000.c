typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;
void ft_show_tab(struct s_stock_str *par);
static int slen(char *s){int i=0;while(s[i])i++;return i;}
int main(void){t_stock_str t[3];
t[0].str = "Rick"; t[0].copy = "Rick"; t[0].size = slen("Rick");
t[1].str = "Morty"; t[1].copy = "Morty"; t[1].size = slen("Morty");
 t[2].str = 0;ft_show_tab(t);return 0;}
