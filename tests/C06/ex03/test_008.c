#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "./a.out";
	char a1[] = "Zebra";
	char a2[] = "apple";
	char a3[] = "Apple";
	char a4[] = "zebra";
	char *av[] = {a0, a1, a2, a3, a4, 0};

	return ft_student_main(5, av);
}
