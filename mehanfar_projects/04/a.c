#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


struct node {
	int data;
	struct node *next;
};


void
append(struct node **list, int data)
{
	struct node *tmp = NULL, *start = *list;
	struct node *new = calloc(sizeof(struct node), 1);
	new->data = data;
	while (start != NULL && start->data < data) {
		tmp = start;
		start = start->next;
	}

	new->next = start;
	if (tmp != NULL)
		tmp->next = new;
	else
		*list = new;
}


void
print(struct node *list)
{
	if (list == NULL) return;

	print(list->next);
	printf("%d ", list->data);
}


void
rprint(struct node *list)
{
	struct node *start = list;
	uint64_t size;
	for (size = 0; start != NULL; start = start->next) size++;
	for (int i = size - 1; i >= 0; i--) {
		start = list;
		for (int j = 0; j <= i; j++) {
			if (i == j)
				printf("%d ", start->data);

			start = start->next;
		}
	}
	putchar('\n');
}


int
main(void)
{
	struct node *start = calloc(sizeof(struct node), 1);
	struct node *start1 = calloc(sizeof(struct node), 1);
	struct node *start2 = calloc(sizeof(struct node), 1);

	start->data = 1; start->next = start1;
	start1->data = 2; start1->next = start2;
	start2->data = 4; start2->next = NULL;

	print(start);
	append(&start, 100);
	append(&start, 3);
	putchar('\n');
	rprint(start);

	return 0;
}
