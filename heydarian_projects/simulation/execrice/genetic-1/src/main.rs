mod genetic;

use genetic::run_genetic_algorithm;

fn main() {
    println!("Part A: Genetic algorithm with fixed crossover and mutation positions");

    let mut successful_iterations = Vec::new();

    for run in 1..=10 {
        let result = run_genetic_algorithm();
        let x = result.best.genes[0];
        let y = result.best.genes[1];
        let z = result.best.genes[2];
        let best_value = result.best.fit_value();

        if result.reached_target {
            successful_iterations.push(result.generation);
            println!(
                "Run {}: reached target after {} iterations",
                run, result.generation
            );
        } else {
            println!("Run {}: failed after {} iterations", run, result.generation);
        }

        println!("  x = {}, y = {}, z = {}", x, y, z);
        println!("  Final best value = {}", best_value);
        println!();
    }

    if successful_iterations.is_empty() {
        println!("Average successful iterations: no successful runs");
    } else {
        let total: usize = successful_iterations.iter().sum();
        let average = total as f64 / successful_iterations.len() as f64;
        println!("Successful run iterations: {:?}", successful_iterations);
        println!("Average successful iterations: {:.2}", average);
    }
}
