#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

void	ft_print_combn(int n)
{
	int	nums[10];
	int	i;

	i = 0;
	while (i < n)
	{
		nums[i] = i;
		i++;
	}
	while (1)
	{
		i = 0;
		while (i < n)
			ft_putchar('0' + nums[i++]);
		if (nums[0] == 10 - n)
			break ;
		ft_putchar(',');
		ft_putchar(' ');
		i = n - 1;
		while (i >= 0 && nums[i] == 9 - (n - 1 - i))
			i--;
		nums[i]++;
		while (++i < n)
			nums[i] = nums[i - 1] + 1;
	}
}
