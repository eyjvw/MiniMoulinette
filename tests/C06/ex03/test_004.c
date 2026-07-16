#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "ab";
	char a2[] = "a";
	char *av[] = {a0, a1, a2, 0};

	return ft_student_main(3, av);
}
