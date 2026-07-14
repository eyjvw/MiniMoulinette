#include <stdlib.h>

int		ft_is_valid_base(char *base);
long	ft_atoi_base(char *nbr, char *base, int base_len);

static int	count_len(long val, int base_len, int *neg)
{
	int		len;
	long	tmp;

	len = 0;
	*neg = 0;
	if (val < 0)
		*neg = 1;
	if (val == 0)
		return (1);
	tmp = val;
	while (tmp != 0)
	{
		tmp /= base_len;
		len++;
	}
	return (len);
}

char	*ft_convert_base(char *nbr, char *base_from, char *base_to)
{
	int		from_len;
	int		to_len;
	long	val;
	char	*res;
	int		len;
	int		neg;
	long	v;
	int		i;
	int		d;

	from_len = ft_is_valid_base(base_from);
	to_len = ft_is_valid_base(base_to);
	if (!from_len || !to_len)
		return (0);
	val = ft_atoi_base(nbr, base_from, from_len);
	len = count_len(val, to_len, &neg);
	res = (char *)malloc(sizeof(char) * (len + neg + 1));
	if (!res)
		return (0);
	res[len + neg] = '\0';
	i = len + neg - 1;
	if (val == 0)
		res[i--] = base_to[0];
	v = val;
	while (v != 0)
	{
		d = (int)(v % to_len);
		if (d < 0)
			d = -d;
		res[i--] = base_to[d];
		v /= to_len;
	}
	if (neg)
		res[0] = '-';
	return (res);
}
