typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;
void ft_show_tab(struct s_stock_str *par);
static int slen(char *s){int i=0;while(s[i])i++;return i;}
int main(void){t_stock_str t[3];
t[0].str = ""; t[0].copy = ""; t[0].size = slen("");
t[1].str = "x"; t[1].copy = "x"; t[1].size = slen("x");
 t[2].str = 0;ft_show_tab(t);return 0;}
