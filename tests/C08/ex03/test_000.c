#include <stdio.h>
#include "ft_point.h"
void set_point(t_point *p){p->x = 42; p->y = 21;}
int main(void){t_point p; set_point(&p);printf("%d %d", p.x, p.y);return 0;}
