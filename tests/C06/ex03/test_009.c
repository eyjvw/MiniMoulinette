#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "~";
	char a2[] = "!";
	char a3[] = "0";
	char a4[] = "Z";
	char a5[] = "_";
	char a6[] = "a";
	char *av[] = {a0, a1, a2, a3, a4, a5, a6, 0};

	return ft_student_main(7, av);
}
