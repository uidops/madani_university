use plotters::element::Circle;
use plotters::prelude::*;
use rand::prelude::*;
use rand::rngs::StdRng;

fn monte_carlo_pi(n: usize, seed: u64) -> (f64, Vec<(f64, f64, bool)>) {
    let mut rng = StdRng::seed_from_u64(seed);
    let mut hits = 0usize;
    let mut samples = Vec::with_capacity(n.min(10_000));

    let r = 1.0;

    for i in 0..n {
        let x = rng.random_range(0.0..r);
        let y = rng.random_range(0.0..r);

        let inside = (x * x + y * y) <= (r * r);
        if inside {
            hits += 1;
        }

        if i < 100_000 {
            samples.push((x, y, inside));
        }
    }

    // pi / 4 = hits / n  =>  pi = 4 * hits / n
    let pi_estimate = 4.0 * hits as f64 / n as f64;

    (pi_estimate, samples)
}

fn monte_carlo_pi_non_uniform(n: usize, seed: u64) -> f64 {
    let mut rng = StdRng::seed_from_u64(seed);
    let mut hits = 0usize;
    let r = 1.0;

    for _ in 0..n {
        // Non-uniform sampling (skewed towards 1.0)
        let u1: f64 = rng.random_range(0.0..1.0);
        let u2: f64 = rng.random_range(0.0..1.0);
        let x = r * u1.sqrt();
        let y = r * u2.sqrt();

        if (x * x + y * y) <= (r * r) {
            hits += 1;
        }
    }

    4.0 * hits as f64 / n as f64
}

fn plot(
    samples: &[(f64, f64, bool)],
    n: usize,
    pi_est: f64,
) -> Result<(), Box<dyn std::error::Error>> {
    let root = BitMapBackend::new("image.png", (800, 800)).into_drawing_area();
    root.fill(&WHITE)?;

    let caption = format!("Monte Carlo Pi Estimation (N = {}, Pi ~ {:.5})", n, pi_est);

    let mut chart = ChartBuilder::on(&root)
        .caption(caption, ("sans-serif", 20))
        .margin(15)
        .build_cartesian_2d(0.0..1.05, 0.0..1.05)?;

    chart.configure_mesh().draw()?;

    // Draw quarter circle arc x^2 + y^2 = 1
    let steps = 300;
    let arc_points = (0..=steps).map(|i| {
        let theta = (i as f64 / steps as f64) * (std::f64::consts::PI / 2.0);
        (theta.cos(), theta.sin())
    });

    chart.draw_series(LineSeries::new(arc_points, BLACK.stroke_width(2)))?;

    // Plot scatter points (Red inside quarter circle, Blue outside, matching reference diagram)
    chart.draw_series(samples.iter().map(|(x, y, inside)| {
        if *inside {
            Circle::new((*x, *y), 2, RED.mix(0.6).filled())
        } else {
            Circle::new((*x, *y), 2, BLUE.mix(0.6).filled())
        }
    }))?;

    root.present()?;
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let r = 1.0;
    let n = 500_000;
    let seed: u64 = rand::random();

    let (pi_est, samples) = monte_carlo_pi(n, seed);
    let pi_non_uniform = monte_carlo_pi_non_uniform(n, seed);
    let actual_pi = std::f64::consts::PI;

    println!("========== MONTE CARLO PI ESTIMATION ==========");
    println!("Radius (r):                    {:.1}", r);
    println!("Total Samples (N):             {}", n);
    println!("Actual Pi (π):                 {:.6}", actual_pi);
    println!("Monte Carlo Estimate (Uniform): {:.6}", pi_est);
    println!(
        "Absolute Error (Uniform):       {:.6}",
        (pi_est - actual_pi).abs()
    );
    println!(
        "Relative Error (Uniform):       {:.4}%",
        ((pi_est - actual_pi).abs() / actual_pi) * 100.0
    );
    println!("------------------------------------------------");
    println!("Monte Carlo Estimate (Non-Uniform): {:.6}", pi_non_uniform);
    println!(
        "Absolute Error (Non-Uniform):   {:.6}",
        (pi_non_uniform - actual_pi).abs()
    );
    println!("================================================");

    plot(&samples, n, pi_est)?;

    println!("\nPlot saved successfully to 'image.png'.");

    Ok(())
}
