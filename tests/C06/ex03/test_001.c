#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "z";
	char *av[] = {a0, a1, 0};

	return ft_student_main(2, av);
}
