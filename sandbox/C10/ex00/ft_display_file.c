#include <unistd.h>
#include <fcntl.h>

#define BUF_SIZE 4096

static void	putstr_err(char *s)
{
	int	i;

	i = 0;
	while (s[i])
		i++;
	write(2, s, i);
}

static int	display(char *path)
{
	char	buf[BUF_SIZE];
	int		fd;
	int		r;

	fd = open(path, O_RDONLY);
	if (fd < 0)
		return (-1);
	r = read(fd, buf, BUF_SIZE);
	while (r > 0)
	{
		write(1, buf, r);
		r = read(fd, buf, BUF_SIZE);
	}
	close(fd);
	if (r < 0)
		return (-1);
	return (0);
}

int	main(int argc, char **argv)
{
	if (argc == 1)
	{
		putstr_err("File name missing.\n");
		return (1);
	}
	if (argc > 2)
	{
		putstr_err("Too many arguments.\n");
		return (1);
	}
	if (display(argv[1]) < 0)
	{
		putstr_err("Cannot read file.\n");
		return (1);
	}
	return (0);
}
