#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <libgen.h>

#define BUF_SIZE 4096

static void	putstr_fd(int fd, char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	write(fd, s, i);
}

static void	print_error(char *prog, char *file)
{
	putstr_fd(2, prog);
	putstr_fd(2, ": cannot open '");
	putstr_fd(2, file);
	putstr_fd(2, "' for reading: ");
	putstr_fd(2, strerror(errno));
	putstr_fd(2, "\n");
}

static int	ft_streq(char *a, char *b)
{
	int	i;

	i = 0;
	while (a[i] && a[i] == b[i])
		i++;
	return (a[i] == b[i]);
}

static long	ft_atol(char *s)
{
	long	n;

	n = 0;
	while (*s >= '0' && *s <= '9')
	{
		n = n * 10 + (*s - '0');
		s++;
	}
	return (n);
}

/* Keep only the last `count` bytes of fd using a ring buffer. */
static int	tail_fd(int fd, long count)
{
	char	buf[BUF_SIZE];
	char	*ring;
	long	total;
	long	pos;
	int		r;

	if (count <= 0)
		return (0);
	ring = malloc(count);
	if (!ring)
		return (-1);
	total = 0;
	pos = 0;
	r = read(fd, buf, BUF_SIZE);
	while (r > 0)
	{
		for (int i = 0; i < r; i++)
		{
			ring[pos] = buf[i];
			pos = (pos + 1) % count;
		}
		total += r;
		r = read(fd, buf, BUF_SIZE);
	}
	if (r < 0)
		return (free(ring), -1);
	if (total <= count)
		write(1, ring, total);
	else
	{
		write(1, ring + pos, count - pos);
		write(1, ring, pos);
	}
	free(ring);
	return (0);
}

static void	print_header(char *name, int first)
{
	if (!first)
		putstr_fd(1, "\n");
	putstr_fd(1, "==> ");
	putstr_fd(1, name);
	putstr_fd(1, " <==\n");
}

int	main(int argc, char **argv)
{
	long	count;
	int		i;
	int		fd;
	int		ret;

	if (argc < 3 || !ft_streq(argv[1], "-c"))
		return (1);
	count = ft_atol(argv[2]);
	if (argc == 3)
		return (tail_fd(0, count) < 0);
	ret = 0;
	i = 3;
	while (i < argc)
	{
		fd = open(argv[i], O_RDONLY);
		if (fd < 0)
		{
			print_error(basename(argv[0]), argv[i]);
			ret = 1;
		}
		else
		{
			if (argc > 4)
				print_header(argv[i], i == 3);
			tail_fd(fd, count);
			close(fd);
		}
		i++;
	}
	return (ret);
}
