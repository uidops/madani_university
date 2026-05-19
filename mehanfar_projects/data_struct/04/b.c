#include <stdio.h>
#include <stdlib.h>


struct node {
	int data;
	struct node *next;
};



void
append(struct node **list, int data)
{
	struct node *tmp = *list, *tail = NULL;
	struct node *new = calloc(sizeof(struct node), 1);
	new->data =data;
	if (*list == NULL) {
		new->next = new;
		*list = new;
		return;
	}

	while (tmp->next != *list) tmp = tmp->next;
	new->next = *list;
	tmp->next = new;
	*list = new;
}

void
print(struct node *list)
{
	struct node *start = list;
	if (list != NULL) {
		do {
			printf("%d ", list->data);
			list = list->next;
		} while (list != start);
	}
	putchar('\n');
}


void
f(struct node *start)
{
	struct node *p = start;
	while (p->next != p) {
		print(p);
		p->next = p->next->next;
		p = p->next;
	}

	//printf("%d ", p->data);
}

int
main(void)
{
	struct node *start;
	append(&start, 7);
	append(&start, 6);
	append(&start, 5);
	append(&start, 4);
	append(&start, 3);
	append(&start, 2);
	append(&start, 1);
	//print(start);
	f(start);
 	putchar('\n');
	return 0;
}

