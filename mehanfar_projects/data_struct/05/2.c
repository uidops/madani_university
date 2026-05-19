#include <stdio.h>
#include <stdlib.h>
#include <err.h>
#include <errno.h>

#define STACK_MAX 10

struct dual_stack {
 	int top_s1, top_s2;
	int stack[STACK_MAX];
};


void
push_s1(struct dual_stack *stack, int data)
{
	if (stack->top_s1+1 == stack->top_s2) {
		errno = EFAULT;
		warn("overflow");
		return;
	}

	stack->top_s1++;
	stack->stack[stack->top_s1] = data;
}

void
push_s2(struct dual_stack *stack, int data)
{
	if (stack->top_s2-1 == stack->top_s1) {
		errno = EFAULT;
		warn("overflow");
		return;
	}

	stack->top_s2--;
	stack->stack[stack->top_s2] = data;
}

int
pop_s1(struct dual_stack *stack)
{
	if (stack->top_s1 == -1) {
		errno = EFAULT;
		warn("underflow");
		return -1;
	}

	int data = stack->stack[stack->top_s1];
	stack->top_s1--;
	return data;
}

int
pop_s2(struct dual_stack *stack)
{
	if (stack->top_s2 == STACK_MAX) {
		errno = EFAULT;
		warn("underflow");
		return -1;
	}

	int data = stack->stack[stack->top_s2];
	stack->top_s2++;
	return data;
}

int
main(void)
{
	struct dual_stack stack = {0};
	stack.top_s1 = -1; stack.top_s2 = STACK_MAX;

	push_s1(&stack, 1);
	push_s1(&stack, 2);
	push_s1(&stack, 3);
	push_s1(&stack, 4);
	push_s1(&stack, 5);
	push_s2(&stack, 6);
	push_s2(&stack, 7);
	push_s2(&stack, 8);
	push_s2(&stack, 9);
	push_s2(&stack, 10);
	printf("%d\n", pop_s1(&stack));
	return EXIT_SUCCESS;
}
