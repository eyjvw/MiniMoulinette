typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;
void ft_show_tab(struct s_stock_str *par);
static int slen(char *s){int i=0;while(s[i])i++;return i;}
int main(void){t_stock_str t[4];
t[0].str = "one"; t[0].copy = "one"; t[0].size = slen("one");
t[1].str = "two"; t[1].copy = "two"; t[1].size = slen("two");
t[2].str = "three"; t[2].copy = "three"; t[2].size = slen("three");
 t[3].str = 0;ft_show_tab(t);return 0;}
