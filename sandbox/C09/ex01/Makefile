NAME		= libft.a

SRCS_DIR	= srcs
INC_DIR		= includes

SRCS		= $(SRCS_DIR)/ft_putchar.c \
			  $(SRCS_DIR)/ft_swap.c \
			  $(SRCS_DIR)/ft_putstr.c \
			  $(SRCS_DIR)/ft_strlen.c \
			  $(SRCS_DIR)/ft_strcmp.c

OBJS		= $(SRCS:.c=.o)

CC			= cc
CFLAGS		= -Wall -Wextra -Werror
AR			= ar -rc

all: $(NAME)

$(NAME): $(OBJS)
	$(AR) $(NAME) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -I$(INC_DIR) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
