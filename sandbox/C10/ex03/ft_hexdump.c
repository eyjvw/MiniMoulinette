#include <unistd.h>
#include <fcntl.h>
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
	putstr_fd(2, ": ");
	putstr_fd(2, file);
	putstr_fd(2, ": ");
	putstr_fd(2, strerror(errno));
	putstr_fd(2, "\n");
}

static void	put_hex(char *dst, unsigned long v, int width)
{
	int	i;

	i = width - 1;
	while (i >= 0)
	{
		dst[i] = "0123456789abcdef"[v % 16];
		v /= 16;
		i--;
	}
}

/* One canonical line: offset, 16 hex bytes in two groups, |ascii|. */
static void	print_line(unsigned long off, unsigned char *b, int n)
{
	char	line[80];
	int		i;
	int		len;

	memset(line, ' ', sizeof(line));
	put_hex(line, off, 8);
	if (n == 0)
	{
		line[8] = '\n';
		write(1, line, 9);
		return ;
	}
	i = 0;
	while (i < n)
	{
		put_hex(line + 10 + i * 3 + (i >= 8), b[i], 2);
		i++;
	}
	line[60] = '|';
	i = 0;
	while (i < n)
	{
		if (b[i] >= 32 && b[i] <= 126)
			line[61 + i] = b[i];
		else
			line[61 + i] = '.';
		i++;
	}
	line[61 + n] = '|';
	line[62 + n] = '\n';
	len = 63 + n;
	write(1, line, len);
}

typedef struct s_dump
{
	unsigned char	cur[16];
	unsigned char	prev[16];
	int				fill;
	int				has_prev;
	int				squeezing;
	unsigned long	off;
}	t_dump;

static void	flush_line(t_dump *d)
{
	if (d->fill == 16 && d->has_prev
		&& memcmp(d->cur, d->prev, 16) == 0)
	{
		if (!d->squeezing)
			write(1, "*\n", 2);
		d->squeezing = 1;
	}
	else
	{
		print_line(d->off, d->cur, d->fill);
		d->squeezing = 0;
	}
	memcpy(d->prev, d->cur, 16);
	d->has_prev = 1;
	d->off += d->fill;
	d->fill = 0;
}

static int	dump_fd(int fd, t_dump *d)
{
	unsigned char	buf[BUF_SIZE];
	int				r;
	int				i;

	r = read(fd, buf, BUF_SIZE);
	while (r > 0)
	{
		i = 0;
		while (i < r)
		{
			d->cur[d->fill++] = buf[i++];
			if (d->fill == 16)
				flush_line(d);
		}
		r = read(fd, buf, BUF_SIZE);
	}
	return (r);
}

int	main(int argc, char **argv)
{
	static t_dump	d;
	int				i;
	int				fd;
	int				ret;

	i = 1;
	if (i < argc && strcmp(argv[i], "-C") == 0)
		i++;
	ret = 0;
	if (i == argc)
		dump_fd(0, &d);
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
			dump_fd(fd, &d);
			close(fd);
		}
		i++;
	}
	if (d.fill > 0)
		flush_line(&d);
	if (d.off > 0)
		print_line(d.off, (unsigned char *)"", 0);
	return (ret);
}
