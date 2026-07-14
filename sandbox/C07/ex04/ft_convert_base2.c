int	ft_is_valid_base(char *base)
{
	int		len;
	int		j;
	char	c;

	len = 0;
	while (base[len])
	{
		c = base[len];
		if (c == '+' || c == '-' || c == ' ' || (c >= 9 && c <= 13))
			return (0);
		j = 0;
		while (j < len)
		{
			if (base[j] == c)
				return (0);
			j++;
		}
		len++;
	}
	if (len < 2)
		return (0);
	return (len);
}

int	ft_char_index(char *base, char c)
{
	int	i;

	i = 0;
	while (base[i])
	{
		if (base[i] == c)
			return (i);
		i++;
	}
	return (-1);
}

long	ft_atoi_base(char *nbr, char *base, int base_len)
{
	long	res;
	int		sign;
	int		i;
	int		digit;

	res = 0;
	sign = 1;
	i = 0;
	while (nbr[i] == ' ' || (nbr[i] >= 9 && nbr[i] <= 13))
		i++;
	while (nbr[i] == '+' || nbr[i] == '-')
	{
		if (nbr[i] == '-')
			sign = -sign;
		i++;
	}
	digit = ft_char_index(base, nbr[i]);
	while (nbr[i] && digit >= 0)
	{
		res = res * base_len + digit;
		i++;
		digit = ft_char_index(base, nbr[i]);
	}
	return (res * sign);
}
