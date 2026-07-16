int    ft_atoi(char *str)
{
    int result;
    int sign;

    result = 0;
    sign = 1;
    while (*str == ' ' || (*str >= 9 && *str <= 13))
        str++;
    while (*str == '-' || *str == '+')
    {
        if (*str == '-')
            sign = -sign;
        str++;
    }
    while (*str >= '0' && *str <= '9')
    {
        result = (result * 10) + (*str - '0');
        str++;
    }
    return (sign * result);
}
