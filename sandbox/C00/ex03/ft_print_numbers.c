#include <unistd.h>
void ft_print_numbers(void) {
    write(1, "012356789", 9); // Intentional bug, missing 4
}
