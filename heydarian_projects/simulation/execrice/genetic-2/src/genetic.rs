use rand::RngExt;
use rand_distr::{Distribution, Normal};

const POPULATION_SIZE: usize = 20;
const MAX_GENERATIONS: usize = 1_000;
const GENE_INTERVAL: (i32, i32) = (-50, 50);
const MUTATION_RATE: f64 = 0.15;
const CHROMOSOME_LENGTH: usize = 3;
const TARGET_TOLERANCE: f64 = 0.25;

#[derive(Clone, Debug)]
pub struct Chromosome {
    pub genes: [i32; CHROMOSOME_LENGTH], // [x, y, z]
}

pub struct RunResult {
    pub reached_target: bool,
    pub generation: usize,
    pub best: Chromosome,
}

impl Chromosome {
    fn random() -> Self {
        let mut rng = rand::rng();
        let gene_min = GENE_INTERVAL.0;
        let gene_max = GENE_INTERVAL.1;

        Self {
            genes: [
                rng.random_range(gene_min..=gene_max),
                rng.random_range(gene_min..=gene_max),
                rng.random_range(gene_min..=gene_max),
            ],
        }
    }

    pub fn fit_value(&self) -> i32 {
        let x = self.genes[0];
        let y = self.genes[1];
        let z = self.genes[2];

        2 * x + 12 * y - 6 * z - 20
    }

    fn fitness_score(&self) -> u32 {
        self.fit_value().unsigned_abs()
    }

    fn reached_target(&self) -> bool {
        (self.fit_value() as f64).abs() <= TARGET_TOLERANCE
    }
}

fn normal_index(mean: f64, std_dev: f64, min: usize, max: usize) -> usize {
    let mut rng = rand::rng();
    let normal = Normal::new(mean, std_dev).expect("standard deviation must be positive");
    let sampled_index = normal.sample(&mut rng).round() as isize;

    // Keep normally sampled positions inside the valid chromosome index range.
    sampled_index.clamp(min as isize, max as isize) as usize
}

fn crossover(parent1: &Chromosome, parent2: &Chromosome) -> Chromosome {
    let mut child = parent1.clone();

    // Part B: choose the crossover point using a normal random distribution.
    let crossover_mean = CHROMOSOME_LENGTH as f64 / 2.0;
    let crossover_std_dev = CHROMOSOME_LENGTH as f64 / 6.0;
    let crossover_point = normal_index(crossover_mean, crossover_std_dev, 1, CHROMOSOME_LENGTH - 1);

    for i in crossover_point..CHROMOSOME_LENGTH {
        child.genes[i] = parent2.genes[i];
    }

    child
}

fn mutate(chromosome: &mut Chromosome) {
    let mut rng = rand::rng();

    if rng.random_bool(MUTATION_RATE) {
        // Part B: choose the mutation location using a normal random distribution.
        let mutation_mean = (CHROMOSOME_LENGTH as f64 - 1.0) / 2.0;
        let mutation_std_dev = CHROMOSOME_LENGTH as f64 / 6.0;
        let mutation_position =
            normal_index(mutation_mean, mutation_std_dev, 0, CHROMOSOME_LENGTH - 1);
        chromosome.genes[mutation_position] = rng.random_range(GENE_INTERVAL.0..=GENE_INTERVAL.1);
    }
}

fn select_parent(population: &[Chromosome]) -> Chromosome {
    let mut rng = rand::rng();

    // Tournament selection
    let a = &population[rng.random_range(0..population.len())];
    let b = &population[rng.random_range(0..population.len())];

    if a.fitness_score() <= b.fitness_score() {
        a.clone()
    } else {
        b.clone()
    }
}

fn best_chromosome(population: &[Chromosome]) -> Chromosome {
    population
        .iter()
        .min_by_key(|chromosome| chromosome.fitness_score())
        .expect("population should not be empty")
        .clone()
}

pub fn run_genetic_algorithm() -> RunResult {
    let mut population: Vec<Chromosome> =
        (0..POPULATION_SIZE).map(|_| Chromosome::random()).collect();

    let initial_best = best_chromosome(&population);
    if initial_best.reached_target() {
        return RunResult {
            reached_target: true,
            generation: 0,
            best: initial_best,
        };
    }

    for generation in 1..=MAX_GENERATIONS {
        population.sort_by_key(|c| c.fitness_score());

        let mut new_population = Vec::new();

        // Elitism: keep the best chromosomes
        new_population.push(population[0].clone());
        new_population.push(population[1].clone());

        while new_population.len() < POPULATION_SIZE {
            let parent1 = select_parent(&population);
            let parent2 = select_parent(&population);

            let mut child = crossover(&parent1, &parent2);
            mutate(&mut child);

            new_population.push(child);
        }

        population = new_population;

        let best = best_chromosome(&population);
        if best.reached_target() {
            return RunResult {
                reached_target: true,
                generation,
                best,
            };
        }
    }

    RunResult {
        reached_target: false,
        generation: MAX_GENERATIONS,
        best: best_chromosome(&population),
    }
}
