#include <stdlib.h>

static int	ft_strlen(char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

static char	*ft_append(char *dst, char *src)
{
	int	i;

	i = 0;
	while (src[i])
	{
		*dst++ = src[i];
		i++;
	}
	return (dst);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	char	*res;
	char	*ptr;
	int		total;
	int		i;

	total = 0;
	i = 0;
	while (i < size)
		total += ft_strlen(strs[i++]);
	if (size > 1)
		total += ft_strlen(sep) * (size - 1);
	res = (char *)malloc(sizeof(char) * (total + 1));
	if (!res)
		return (0);
	ptr = res;
	i = 0;
	while (i < size)
	{
		ptr = ft_append(ptr, strs[i]);
		if (i < size - 1)
			ptr = ft_append(ptr, sep);
		i++;
	}
	*ptr = '\0';
	return (res);
}
