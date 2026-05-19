use std::time::{SystemTime, UNIX_EPOCH};

mod rng;
use rng::Rng;

type Point = (usize, usize);

const ROWS: usize = 10;
const COLS: usize = 10;

// 0 = white (allowed), 1 = black (blocked)
const BOARD: [[u8; COLS]; ROWS] = [
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
];

const START: Point = (9, 2);
const DEST: Point = (0, 8);

// Directions: 0=Up, 1=Down, 2=Right, 3=Left
const DR: [i32; 4] = [-1, 1, 0, 0];
const DC: [i32; 4] = [0, 0, 1, -1];

// Dice-based direction:
//   Roll 1, 2, 3 -> Up    (prob = 3/6 = 0.5)
//   Roll 4       -> Down  (prob = 1/6)
//   Roll 5       -> Right (prob = 1/6)
//   Roll 6       -> Left  (prob = 1/6)
fn pick_dice(rng: &mut Rng) -> usize {
    let roll = rng.next_range(6) + 1;
    match roll {
        1 | 2 | 3 => 0, // Up
        4 => 1,         // Down
        5 => 2,         // Right
        _ => 3,         // Left  (roll == 6)
    }
}

struct RunResult {
    moves: u64,
    failures: u64,
}

fn simulate(rng: &mut Rng, max_moves: u64) -> Option<RunResult> {
    let (mut r, mut c) = START;
    let mut moves: u64 = 0;
    let mut failures: u64 = 0;

    while (r, c) != DEST {
        if moves >= max_moves {
            return None;
        }

        let d = pick_dice(rng);

        let nr = r as i32 + DR[d];
        let nc = c as i32 + DC[d];

        // Out of bounds OR landed on a black square -> FAILURE.
        // Per problem statement: stay on the previous white square (the bead "returns").
        if nr < 0
            || nr >= ROWS as i32
            || nc < 0
            || nc >= COLS as i32
            || BOARD[nr as usize][nc as usize] == 1
        {
            failures += 1;
            moves += 1; // the attempted move still counts as a move
            continue; // position unchanged
        }

        // Successful move
        r = nr as usize;
        c = nc as usize;
        moves += 1;
    }
    Some(RunResult { moves, failures })
}

fn run_experiment(trials: u64, seed: u64) {
    let mut rng = Rng::new(seed);
    let mut sum_a: u128 = 0;
    let mut sum_b: u128 = 0;
    let mut min_a: u64 = u64::MAX;
    let mut max_a: u64 = 0;
    let mut completed: u64 = 0;
    let max_moves: u64 = 10_000_000;

    for _ in 0..trials {
        if let Some(res) = simulate(&mut rng, max_moves) {
            sum_a += res.moves as u128;
            sum_b += res.failures as u128;
            if res.moves < min_a {
                min_a = res.moves;
            }
            if res.moves > max_a {
                max_a = res.moves;
            }
            completed += 1;
        }
    }

    let mean_a = sum_a as f64 / completed as f64;
    let mean_b = sum_b as f64 / completed as f64;
    let ratio = mean_a / (mean_a + mean_b);

    println!("=== Dice-based random walk ({} trials) ===", trials);
    println!("  Completed runs : {}", completed);
    println!("  E[A] (moves)   : {:.2}", mean_a);
    println!("  E[B] (failures): {:.2}", mean_b);
    println!("  min A / max A  : {} / {}", min_a, max_a);
    println!("  A / (A+B)      : {:.4}", ratio);
    println!();
}

fn print_board() {
    println!("Board (■=black, .=white, S=start, D=destination):");
    for r in 0..ROWS {
        print!("  ");
        for c in 0..COLS {
            let ch = if (r, c) == START {
                'S'
            } else if (r, c) == DEST {
                'D'
            } else if BOARD[r][c] == 1 {
                '#'
            } else {
                '.'
            };
            print!("{} ", ch);
        }
        println!();
    }
    println!();
}

fn main() {
    print_board();

    let seed = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards")
        .as_nanos() as u64;

    run_experiment(10_000, seed);
}
