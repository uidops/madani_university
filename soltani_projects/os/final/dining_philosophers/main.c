#include <err.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <ncurses.h>
#include <time.h>
#define __DARWIN_C_LEVEL __DARWIN_C_FULL
#include <math.h>

#define UPDATE_DELAY 500000

#define NUM 5
#define ROUND 5

typedef enum e_state {
	THINKING, // 0
	HUNGRY,   // 1
	EATING    // 2
} state_t;

typedef struct s_philo {
	uint32_t id;        // Philosopher ID
	pthread_t thread;   // Posix thread
	state_t state;      // Current state of the philosopher
	char sem_name[32];  // Name of the mutex for this philosopher
	sem_t *sem;         // Mutex for this philosopher
	uint8_t completed;  // Flag to indicate if the philosopher has completed their rounds
} philo_t;


philo_t *philosophers = NULL;
sem_t *mutex; // semaphore for changing the state of the philosophers
sem_t *display_mutex; // semaphore for displaying the table
char *philosophers_name[] = {"Voltaire", "Plato", "Russell", "Kant", "Descartes"};


// Macros to get the left-hand and right-hand philosophers of a philosopher
#define LEFT(philo) (&philosophers[(philo->id + NUM - 1) % NUM])
#define RIGHT(philo) (&philosophers[(philo->id + 1) % NUM])


static void		 cleanup(philo_t *);
static void		*start(void *);
static void		 think(philo_t *);
static void		 test(philo_t *);
static void		 take_forks(philo_t *);
static void		 put_forks(philo_t *);
static void		 eat(philo_t *);

static void		 init_ncurses(void);
static void		 finish_ncurses(void);
static void		 update_display(void);


int
main(void)
{
	srand((unsigned int)time(NULL)); // Seed the random number generator

	init_ncurses();

	// using named-semaphore to synchronize access to the display with default value 1
	display_mutex = sem_open("/display_mutex", O_CREAT|O_EXCL, S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH, 1);
	if (display_mutex == SEM_FAILED) {
		finish_ncurses();
		err(EXIT_FAILURE, "sem_open(/mutex_sem)");
	}
	sem_unlink("/display_mutex");

	// Allocate memory for philosophers
	philosophers = calloc(NUM, sizeof(philo_t));
	if (!philosophers) {
		finish_ncurses();
		err(EXIT_FAILURE, "calloc(philosophers)");
	}

	// using named-semaphore to synchronize access to the philosophers' states
	mutex = sem_open("/mutex_sem", O_CREAT|O_EXCL, S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH, 1);
	if (mutex == SEM_FAILED) {
		free(philosophers);
		finish_ncurses();
		err(EXIT_FAILURE, "sem_open(/mutex_sem)");
	}
	sem_unlink("/mutex_sem");

	// Initialize philosophers
	for (int i = 0; i < NUM; i++) {
		philosophers[i].id = i;
		philosophers[i].state = THINKING; // Default state is THINKING as dijkstra suggests
		philosophers[i].completed = 0;

		// Create a unique mutex named-semaphore for each philosopher with default value 0
		snprintf(philosophers[i].sem_name, sizeof(philosophers[i].sem_name),
		    "/philo_sem_%d", i);
		philosophers[i].sem = sem_open(philosophers[i].sem_name, O_CREAT|O_EXCL, S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH, 0);
		if (philosophers[i].sem == SEM_FAILED) {
			cleanup(philosophers);
			finish_ncurses();
			err(EXIT_FAILURE, "sem_open(/philo_sem_%d)", i);
		}
		sem_unlink(philosophers[i].sem_name);

		// Create a posix thread for each philosopher
		if (pthread_create(&philosophers[i].thread, NULL, start,
		    &philosophers[i]) != 0) {
			cleanup(philosophers);
			finish_ncurses();
			err(EXIT_FAILURE, "pthread_create(philosopher %d)", i);
		}
	}

	// Main loop to update the display and check for completion
	uint8_t ok = 1;
	while (ok) {
		// Wait for the display mutex to update the display
		sem_wait(display_mutex);
		update_display();
		sem_post(display_mutex);

		usleep(UPDATE_DELAY);

		// Check for user input to quit
		if (getch() == 'q') {
			break;
		}

		// Check if all philosophers have completed their rounds
		ok = 0;
		for (int i = 0; i < NUM; i++) {
			if (!philosophers[i].completed) {
				ok = 1;
				break;
			}
		}

	}


	update_display();
	sleep(4204);

	// Wait for all philosophers to finish their threads
	for (int i = 0; i < NUM; i++) {
		pthread_join(philosophers[i].thread, NULL);
	}

	cleanup(philosophers);
	finish_ncurses();

	return (EXIT_SUCCESS);
}


static void
cleanup(philo_t *philosophers)
{
	// Close all philosopher semaphores
	for (int i = 0; i < NUM; i++) {
		if (philosophers[i].sem && philosophers[i].sem != SEM_FAILED) {
			sem_close(philosophers[i].sem);
			philosophers[i].sem = NULL;
		}
	}

	// Close the mutex and display mutex
	if (mutex && mutex != SEM_FAILED) {
		sem_close(mutex);
		mutex = NULL;
	}

	if (display_mutex && display_mutex != SEM_FAILED) {
		sem_close(display_mutex);
		display_mutex = NULL;
	}

	// Free the philosophers array
	free(philosophers);
	philosophers = NULL;
}


static void *
start(void *args)
{
	philo_t *philosopher = (philo_t *)args;
	for (int i = 0; i < ROUND; i++) {
		think(philosopher);
		take_forks(philosopher);
		eat(philosopher);
		put_forks(philosopher);
	}

	// Mark the philosopher as completed
	sem_wait(display_mutex);
	philosopher->completed = 1;
	sem_post(display_mutex);

	return NULL;
}


static void
think(philo_t *philosopher)
{
	// Simulate thinking by sleeping for a random time
	sem_wait(display_mutex);
	philosopher->state = THINKING;
	sem_post(display_mutex);

	usleep((rand() % 10 + 3) * 100000);
}


static void
test(philo_t *philosopher)
{
	// Check if the philosopher can eat (both neighbors are not eating and the philosopher is hungry)
	if (LEFT(philosopher)->state != EATING && philosopher->state == HUNGRY && RIGHT(philosopher)->state != EATING) {
		philosopher->state = EATING;
		sem_post(philosopher->sem);
	}
}


static void
take_forks(philo_t *philosopher)
{
	// set the philosopher's state to HUNGRY and test if they can eat
	sem_wait(mutex);
	philosopher->state = HUNGRY;
	test(philosopher);
	sem_post(mutex);

	sem_wait(philosopher->sem);
}


static void
put_forks(philo_t *philosopher)
{
	// release the forks and set the philosopher's state to THINKING and test the neighbors
	sem_wait(mutex);
	philosopher->state = THINKING;

	test(LEFT(philosopher));
	test(RIGHT(philosopher));

	sem_post(mutex);
}


static void
eat(philo_t *philosopher)
{
	// simulate eating by sleeping for a random time
	(void) philosopher;
	usleep((rand() % 10 + 3) * 100000);
}


static void
init_ncurses(void)
{
	// initialize ncurses
	initscr();

	// check if terminal supports colors
	if (has_colors()) {
		// enable colors
		start_color();

		// define color pairs for different states
		init_pair(1, COLOR_BLUE,   COLOR_BLACK);
		init_pair(2, COLOR_YELLOW, COLOR_BLACK);
		init_pair(3, COLOR_RED,    COLOR_BLACK);
		init_pair(4, COLOR_CYAN,   COLOR_BLACK);
	}

	// invisible cursor, no echo, and non-blocking input
	curs_set(0);
	noecho();
	nodelay(stdscr, TRUE);
}


static void
finish_ncurses(void)
{
	// restore terminal settings
	endwin();
}


static void
update_display(void)
{
	// clear the screen and print the title
	clear();
	mvprintw(0, 0, "Dining Philosophers (Djikstra approach)");

	// print the colors section and the philosophers' states
	mvprintw(2, 0, "[COLORS]");
	attron(COLOR_PAIR(1));
	mvprintw(3, 2, "THINKING");
	attroff(COLOR_PAIR(1));

	attron(COLOR_PAIR(2));
	mvprintw(4, 2, "HUNGRY");
	attroff(COLOR_PAIR(2));

	attron(COLOR_PAIR(3));
	mvprintw(5, 2, "EATING");
	attroff(COLOR_PAIR(3));

	int center_y = LINES / 2;
	int center_x = COLS / 2;
	int radius = (LINES < COLS ? LINES : COLS) / 4;

	// draw the table in the center of the screen
	attron(COLOR_PAIR(4) | A_BOLD);
	mvprintw(center_y, center_x, "TABLE");
	attroff(COLOR_PAIR(4) | A_BOLD);

	for (int i = 0; i < NUM; i++) {
		// angle for each philosopher in circle
		double angle = 2.0 * M_PI * i / NUM;

		// polar coordinates to cartesian coordinates
		// x = r * cos(teta)
		// y = r * sin(teta)
		int x = center_x + (int)(radius * cos(angle));
		int y = center_y - (int)(radius * sin(angle));

		int color_pair = 0;
		// color of the philosopher based on their state
		switch (philosophers[i].state) {
		case THINKING:
			color_pair = 1;
			break;
		case HUNGRY:
			color_pair = 2;
			break;
		case EATING:
			color_pair = 3;
			break;
		default:
			color_pair = 4;
			break;
		}

		// print name of the philosopher at the calculated position
		attron(COLOR_PAIR(color_pair));
		mvprintw(y, x, "%s", philosophers_name[i]);
		attroff(COLOR_PAIR(color_pair));
	}

	// print the philosophers' states beside the table
	for (int i = 0; i < NUM; i++) {
		mvprintw(NUM + 6 + i, 0, "%s", philosophers_name[i]);
		switch (philosophers[i].state) {
		case THINKING:
			printw(": THINKING");
			break;
		case HUNGRY:
			printw(": HUNGRY");
			break;
		case EATING:
			printw(": EATING");
			break;
		}
		if (philosophers[i].completed) {
			printw(" [DONE]");
		}
	}

	refresh();
}
