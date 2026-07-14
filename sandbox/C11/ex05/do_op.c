#include <unistd.h>

static void	ft_putstr(char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	write(1, s, i);
}

static void	ft_putnbr(int n)
{
	char	c;

	if (n == -2147483648)
	{
		ft_putstr("-2147483648");
		return ;
	}
	if (n < 0)
	{
		write(1, "-", 1);
		n = -n;
	}
	if (n >= 10)
		ft_putnbr(n / 10);
	c = '0' + n % 10;
	write(1, &c, 1);
}

static int	ft_atoi(char *s)
{
	int	sign;
	int	n;

	sign = 1;
	n = 0;
	while (*s == ' ' || (*s >= 9 && *s <= 13))
		s++;
	while (*s == '+' || *s == '-')
	{
		if (*s == '-')
			sign = -sign;
		s++;
	}
	while (*s >= '0' && *s <= '9')
	{
		n = n * 10 + (*s - '0');
		s++;
	}
	return (n * sign);
}

static int	op_add(int a, int b)
{
	return (a + b);
}

static int	op_sub(int a, int b)
{
	return (a - b);
}

static int	op_mul(int a, int b)
{
	return (a * b);
}

static int	op_div(int a, int b)
{
	return (a / b);
}

static int	op_mod(int a, int b)
{
	return (a % b);
}

int	main(int argc, char **argv)
{
	char	ops[6];
	int		(*f[5])(int, int);
	int		i;

	ops[0] = '+';
	ops[1] = '-';
	ops[2] = '*';
	ops[3] = '/';
	ops[4] = '%';
	ops[5] = '\0';
	f[0] = op_add;
	f[1] = op_sub;
	f[2] = op_mul;
	f[3] = op_div;
	f[4] = op_mod;
	if (argc != 4)
		return (0);
	i = 0;
	while (ops[i] && !(argv[2][0] == ops[i] && argv[2][1] == '\0'))
		i++;
	if (!ops[i])
	{
		ft_putstr("0\n");
		return (0);
	}
	if (i == 3 && ft_atoi(argv[3]) == 0)
	{
		ft_putstr("Stop : division by zero\n");
		return (0);
	}
	if (i == 4 && ft_atoi(argv[3]) == 0)
	{
		ft_putstr("Stop : modulo by zero\n");
		return (0);
	}
	ft_putnbr(f[i](ft_atoi(argv[1]), ft_atoi(argv[3])));
	ft_putstr("\n");
	return (0);
}
