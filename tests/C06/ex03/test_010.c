#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "abc";
	char a2[] = "abd";
	char a3[] = "abb";
	char *av[] = {a0, a1, a2, a3, 0};

	return ft_student_main(4, av);
}
