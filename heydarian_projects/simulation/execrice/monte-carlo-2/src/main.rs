use plotters::element::Circle;
use plotters::prelude::*;
use plotters::style::Color;
use plotters::style::full_palette::GREY;
use rand::prelude::*;
use rand::rngs::StdRng;

#[derive(Clone, Copy)]
struct Disc {
    c: (f64, f64),
    r: f64,
}

fn monte_carlo(c1: Disc, c2: Disc, n: usize, seed: u64) -> (f64, Vec<(f64, f64, bool)>, f64) {
    let mut rng = StdRng::seed_from_u64(seed);

    // bounding box
    let x_min = (c1.c.0 - c1.r).min(c2.c.0 - c2.r);
    let x_max = (c1.c.0 + c1.r).max(c2.c.0 + c2.r);
    let y_min = (c1.c.1 - c1.r).min(c2.c.1 - c2.r);
    let y_max = (c1.c.1 + c1.r).max(c2.c.1 + c2.r);

    // convert to square bounding box
    let side = (x_max - x_min).max(y_max - y_min);

    // center of the bounding box
    let cx = (x_min + x_max) / 2.0;
    let cy = (y_min + y_max) / 2.0;

    // square bounding box coordinates
    let sxmin = cx - side / 2.0;
    let sxmax = cx + side / 2.0;
    let symin = cy - side / 2.0;
    let symax = cy + side / 2.0;

    let mut hits = 0usize;
    let mut samples = Vec::with_capacity(8000);

    for i in 0..n {
        // random point in the square bounding box
        let x = rng.random_range(sxmin..sxmax);
        let y = rng.random_range(symin..symax);

        // check if the point is inside both circles
        let in_c1 = (x - c1.c.0).powi(2) + (y - c1.c.1).powi(2) <= c1.r * c1.r;
        let in_c2 = (x - c2.c.0).powi(2) + (y - c2.c.1).powi(2) <= c2.r * c2.r;

        let both = in_c1 && in_c2;
        if both {
            hits += 1;
        }

        if i < 200_000 {
            samples.push((x, y, both));
        }
    }

    // area / area_box = hits / n    =>    area = area_box * hits / n
    let area_box = side * side;
    let area = area_box * hits as f64 / n as f64;

    (area, samples, side)
}

fn plot(
    c1: Disc,
    c2: Disc,
    samples: &[(f64, f64, bool)],
    side: f64,
) -> Result<(), Box<dyn std::error::Error>> {
    let root = BitMapBackend::new("image.png", (700, 700)).into_drawing_area();

    root.fill(&WHITE)?;

    let cx = (c1.c.0 + c2.c.0) / 2.0;
    let cy = (c1.c.1 + c2.c.1) / 2.0;

    let xmin = cx - side / 2.0;
    let xmax = cx + side / 2.0;
    let ymin = cy - side / 2.0;
    let ymax = cy + side / 2.0;

    let mut chart = ChartBuilder::on(&root)
        .caption("Monte Carlo Circle Intersection", ("sans-serif", 20))
        .margin(10)
        .build_cartesian_2d(xmin..xmax, ymin..ymax)?;

    chart.configure_mesh().draw()?;

    // circles
    let steps = 300;
    let theta = (0..steps).map(|i| i as f64 * 2.0 * std::f64::consts::PI / steps as f64);

    chart.draw_series(LineSeries::new(
        theta
            .clone()
            .map(|t| (c1.c.0 + c1.r * t.cos(), c1.c.1 + c1.r * t.sin())),
        &BLACK,
    ))?;

    chart.draw_series(LineSeries::new(
        theta.map(|t| (c2.c.0 + c2.r * t.cos(), c2.c.1 + c2.r * t.sin())),
        &RED,
    ))?;

    // scatter points
    chart.draw_series(samples.iter().map(|(x, y, inside)| {
        if *inside {
            Circle::new((*x, *y), 2, GREEN.filled())
        } else {
            Circle::new((*x, *y), 1, GREY.mix(0.3).filled())
        }
    }))?;

    root.present()?;
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let c1 = Disc {
        c: (0.0, 0.0),
        r: 4.0,
    };

    let c2 = Disc {
        c: (4.3, 0.0),
        r: 1.7,
    };

    let n = 300_000;

    let (area, samples, side) = monte_carlo(c1, c2, n, 7);

    println!("Area = {:.6}", area);
    plot(c1, c2, &samples, side)?;

    Ok(())
}
