#include <err.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

struct color {
	char *color_name;
	unsigned R, G, B;
};

struct answer {
	char *color_name;
	double deviation;
};

const struct color colors[] = {
	{"lightsalmon", 255, 160, 122},
	{"salmon", 250, 128, 114},
	{"darksalmon", 233, 150, 122},
	{"lightcoral", 240, 128, 128},
	{"indianred", 205, 92, 92},
	{"red", 255, 0, 0},
};


char		*detect_color(const struct color);


int
main(void)
{
	struct color input = {NULL, 0xCC, 0xCC, 0xCC};
	fputs("R G B: ", stdout);
	fflush(stdout);

	if (scanf("%u %u %u", &input.R, &input.G, &input.B) != 3)
		errx(EXIT_FAILURE, "An error occurred!");

	printf("%s\n", detect_color(input));
	return EXIT_SUCCESS;
}

char *
detect_color(const struct color input)
{
	struct answer answer = {NULL, 442.0};

	for (size_t i=0; i < sizeof(colors)/sizeof(struct color); i++) {
		double x = sqrt((input.R - colors[i].R) * (input.R - colors[i].R)
				+ (input.G - colors[i].G) * (input.G - colors[i].G) 
				+ (input.B - colors[i].B) * (input.B - colors[i].B));

		if (x == answer.deviation) {
			answer.color_name = NULL;
			break;
		}

		if (x < answer.deviation) {
			answer.color_name = colors[i].color_name;
			answer.deviation = x;
		}

	}

	return answer.color_name;
}
