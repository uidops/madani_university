#include <stdio.h>
#include <stdlib.h>
#include <err.h>
#include <errno.h>


struct node {
	int data;
	struct node *next;
};


void
push(struct node **list, int data)
{
	struct node *a = calloc(sizeof(struct node), 1);
	a->data = data;
	
	printf("list = %p\n", *list);
	a->next = *list;
	*list = a;
}


int
pop(struct node **list)
{
	struct node *a = NULL;
	int data = 0;
 	if (list == NULL || *list == NULL) {
		errno = EFAULT;
		warn("list is null");
		return -1;
	}

	a = *list;
	data = (*list)->data;
	*list = (*list)->next;
	free(a);

	return data;
}


int
main(void)
{
	struct node *a = NULL;
	push(&a, 1);
	push(&a, 2);
	push(&a, 3);
	printf("%d\n", pop(&a));
	printf("%d\n", pop(&a));
	printf("%d\n", pop(&a));

	return EXIT_SUCCESS;
}
