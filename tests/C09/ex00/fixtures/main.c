#include "ft.h"

int	main(void)
{
	int	a;
	int	b;

	a = 5;
	b = 9;
	ft_putstr("hello");
	ft_putchar('\n');
	ft_swap(&a, &b);
	ft_putchar('0' + a);
	ft_putchar('0' + b);
	ft_putchar('\n');
	ft_putchar('0' + ft_strlen("hello"));
	ft_putchar('\n');
	if (ft_strcmp("abc", "abc") == 0)
		ft_putstr("eq");
	if (ft_strcmp("abc", "abd") < 0)
		ft_putstr("lt");
	ft_putchar('\n');
	return (0);
}
