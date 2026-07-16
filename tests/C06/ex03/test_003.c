#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "B";
	char a2[] = "a";
	char a3[] = "A";
	char a4[] = "b";
	char *av[] = {a0, a1, a2, a3, a4, 0};

	return ft_student_main(5, av);
}
