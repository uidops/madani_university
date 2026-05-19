#include <stdio.h>


void    pyramid(int);

int
main(void)
{
    int n = 0;
    scanf("%d", &n);
    putchar('\n');
    pyramid(n);
    return 0;
}

void
pyramid(int n)
{
	int m = (n * 2) - 1;
	for (int row = 0; row < n; row++) {
		for (int col = 1; col <= m; col++) {
			if (col < n - row) {
				putchar(' ');
				continue;
			} else if (col <= n + row) {
				putchar('*');
				continue;
			}
			break;
		}
		putchar('\n');
	}

}
