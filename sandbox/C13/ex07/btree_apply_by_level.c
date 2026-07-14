#include "ft_btree.h"

static int	level_count(t_btree *root)
{
	int	left;
	int	right;

	if (!root)
		return (0);
	left = level_count(root->left);
	right = level_count(root->right);
	if (left > right)
		return (left + 1);
	return (right + 1);
}

static void	apply_level(t_btree *root, int level, int target,
		void (*applyf)(void *, int, int))
{
	static int	is_first;

	if (level == 0)
		is_first = 1;
	if (!root)
		return ;
	if (level == target)
	{
		applyf(root->item, level, is_first);
		is_first = 0;
		return ;
	}
	apply_level(root->left, level + 1, target, applyf);
	apply_level(root->right, level + 1, target, applyf);
}

void	btree_apply_by_level(t_btree *root,
		void (*applyf)(void *item, int current_level, int is_first_elem))
{
	int	depth;
	int	i;

	depth = level_count(root);
	i = 0;
	while (i < depth)
	{
		apply_level(root, 0, i, applyf);
		i++;
	}
}
