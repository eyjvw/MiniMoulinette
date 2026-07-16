#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "same";
	char a2[] = "same";
	char a3[] = "same";
	char *av[] = {a0, a1, a2, a3, 0};

	return ft_student_main(4, av);
}
