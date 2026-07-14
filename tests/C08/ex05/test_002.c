typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;
void ft_show_tab(struct s_stock_str *par);
static int slen(char *s){int i=0;while(s[i])i++;return i;}
int main(void){t_stock_str t[2];
t[0].str = "single"; t[0].copy = "single"; t[0].size = slen("single");
 t[1].str = 0;ft_show_tab(t);return 0;}
