#undef main
int ft_student_main(int argc, char **argv);

int main(void)
{
	char a0[] = "ft_print_program_name";
	char *av[] = {a0, 0};

	return ft_student_main(1, av);
}
