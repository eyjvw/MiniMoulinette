#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <libgen.h>

#define BUF_SIZE 29000

static void	putstr_fd(int fd, char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	write(fd, s, i);
}

static int	cat_fd(int fd)
{
	char	buf[BUF_SIZE];
	int		r;

	r = read(fd, buf, BUF_SIZE);
	while (r > 0)
	{
		write(1, buf, r);
		r = read(fd, buf, BUF_SIZE);
	}
	if (r < 0)
		return (-1);
	return (0);
}

static void	print_error(char *prog, char *file)
{
	putstr_fd(2, prog);
	putstr_fd(2, ": ");
	if (file)
	{
		putstr_fd(2, file);
		putstr_fd(2, ": ");
	}
	putstr_fd(2, strerror(errno));
	putstr_fd(2, "\n");
}

int	main(int argc, char **argv)
{
	int	i;
	int	fd;
	int	ret;

	if (argc == 1)
	{
		if (cat_fd(0) < 0)
			return (print_error(basename(argv[0]), NULL), 1);
		return (0);
	}
	ret = 0;
	i = 1;
	while (i < argc)
	{
		fd = open(argv[i], O_RDONLY);
		if (fd < 0 || cat_fd(fd) < 0)
		{
			print_error(basename(argv[0]), argv[i]);
			ret = 1;
		}
		if (fd >= 0)
			close(fd);
		i++;
	}
	return (ret);
}
