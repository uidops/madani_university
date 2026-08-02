use rand::prelude::*;
use rand::rngs::StdRng;

use plotters::prelude::*;

fn f(x: f64) -> f64 {
    x * x - 3.0 * x + 11.0
}

// I = delta * (f(a)/2 + f(x1) + f(x2) + ... + f(xn-1) + f(b)/2)
fn trapezoidal_rule(f: fn(f64) -> f64, a: f64, b: f64, n: usize) -> f64 {
    let delta = (b - a) / n as f64;
    let mut sum = 0.0;

    for i in 0..=n {
        let x = a + i as f64 * delta;
        let y = f(x);

        if i == 0 || i == n {
            sum += y / 2.0;
        } else {
            sum += y;
        }
    }

    sum * delta
}

fn monte_carlo(
    f: fn(f64) -> f64,
    a: f64,
    b: f64,
    n: usize,
    seed: u64,
) -> (f64, Vec<f64>, Vec<f64>, Vec<bool>, f64) {
    let mut rng = StdRng::seed_from_u64(seed);

    // maximum value of f(x) in [a, b]
    let grid_n = 2000;
    let mut y_max = f64::MIN;
    for i in 0..grid_n {
        let x = a + (b - a) * i as f64 / grid_n as f64;
        y_max = y_max.max(f(x));
    }
    y_max *= 1.02;

    let mut xs = Vec::with_capacity(n);
    let mut ys = Vec::with_capacity(n);
    let mut hits = Vec::with_capacity(n);

    let mut hit_count = 0usize;

    for _ in 0..n {
        let x = rng.random_range(a..b);
        let y = rng.random_range(0.0..y_max);

        let hit = y <= f(x);
        if hit {
            hit_count += 1;
        }

        xs.push(x);
        ys.push(y);
        hits.push(hit);
    }

    // area/area_box = hit_count/n    =>    area = area_box * hit_count / n

    let area_box = (b - a) * y_max;
    let area = area_box * hit_count as f64 / n as f64;

    (area, xs, ys, hits, y_max)
}

fn monte_carlo_mean_value(f: fn(f64) -> f64, a: f64, b: f64, n: usize, seed: u64) -> f64 {
    let mut rng = StdRng::seed_from_u64(seed);
    let mut sum = 0.0;

    for _ in 0..n {
        let x = rng.random_range(a..b);
        sum += f(x);
    }

    (b - a) * sum / n as f64
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let a = -4.0;
    let b = 5.0;

    // Trapezoidal rule
    let trap_small = trapezoidal_rule(f, a, b, 9);
    let trap_large = trapezoidal_rule(f, a, b, 10_000);

    // Monte Carlo
    let n = 500_000;
    let seed = rand::random();
    let (mc_area, xs, ys, hits, y_max) = monte_carlo(f, a, b, n, seed);
    let mc_mean = monte_carlo_mean_value(f, a, b, n, seed);

    println!("========== RESULTS ==========");
    println!("Exact:                   148.500000");
    println!("Trapezoidal (n=9):       {:.6}", trap_small);
    println!("Trapezoidal (n=10000):   {:.6}", trap_large);
    println!("MC:                      {:.6}", mc_area);
    println!("MC Mean Value:           {:.6}", mc_mean);

    // plot
    let root = BitMapBackend::new("image.png", (1200, 500)).into_drawing_area();
    root.fill(&WHITE)?;

    // let (left, right) = root.split_horizontally(600);

    // let mut chart1 = ChartBuilder::on(&left)
    //     .caption("Function Area", ("sans-serif", 20))
    //     .margin(10)
    //     .build_cartesian_2d(a..b, 0.0..60.0)?;

    // chart1.configure_mesh().draw()?;
    // chart1.draw_series(LineSeries::new(
    //     (0..400).map(|i| {
    //         let x = a + (b - a) * i as f64 / 400.0;
    //         (x, f(x))
    //     }),
    //     &BLUE,
    // ))?;

    let sample_n = 4000.min(n);
    // let sample_n = n;
    let mut hits_points = Vec::new();
    let mut miss_points = Vec::new();

    for i in 0..sample_n {
        if hits[i] {
            hits_points.push((xs[i], ys[i]));
        } else {
            miss_points.push((xs[i], ys[i]));
        }
    }

    let mut chart2 = ChartBuilder::on(&root)
        .caption("Monte Carlo", ("sans-serif", 20))
        .margin(10)
        .build_cartesian_2d(a..b, 0.0..y_max)?;

    chart2.configure_mesh().draw()?;
    chart2.draw_series(
        hits_points
            .iter()
            .map(|p| Circle::new(*p, 2, GREEN.filled())),
    )?;

    chart2.draw_series(
        miss_points
            .iter()
            .map(|p| Circle::new(*p, 2, RED.mix(0.4).filled())),
    )?;

    root.present()?;
    Ok(())
}
