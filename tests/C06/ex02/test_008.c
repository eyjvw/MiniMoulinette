#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "1";
	char a2[] = "2";
	char a3[] = "3";
	char a4[] = "4";
	char a5[] = "5";
	char a6[] = "6";
	char a7[] = "7";
	char a8[] = "8";
	char a9[] = "9";
	char a10[] = "10";
	char *av[] = {a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, 0};

	return ft_student_main(11, av);
}
