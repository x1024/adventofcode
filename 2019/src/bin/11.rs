use std::fs;
use std::collections::HashMap;
use pipe_channel::channel;

use advent_of_code_2019::intcode::run_intcode;

type Point = (i32, i32);
enum Direction {
    R,
    L,
    U,
    D,
}


#[cfg(test)]
pub mod tests {
    use super::*;
}

fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

struct P11 {
    data: HashMap::<Point, bool>,
    position: Point,
    direction: Direction,
    num_inputs: usize,
}

impl P11 {
    fn make() -> P11 {
        P11 {
            data: HashMap::new(),
            position: (0, 0),
            direction: Direction::U,
            num_inputs: 0,
        }
    }

    fn move_forward(&mut self) {
        // move forward
        let offset = match self.direction {
            Direction::U => (0, -1),
            Direction::D => (0, 1),
            Direction::L => (-1, 0),
            Direction::R => (1, 0),
        };
        self.position = (self.position.0 + offset.0, self.position.1 + offset.1)
    }

    fn turn(&mut self, direction: Direction) {
        match direction {
            Direction::L => {
                self.direction = match self.direction {
                    Direction::U => Direction::L,
                    Direction::L => Direction::D,
                    Direction::D => Direction::R,
                    Direction::R => Direction::U,
                };
            }
            Direction::R => {
                self.direction = match self.direction {
                    Direction::U => Direction::R,
                    Direction::R => Direction::D,
                    Direction::D => Direction::L,
                    Direction::L => Direction::U,
                };
            }
            _ => panic!("Invalid direction"),
        };
    }

    fn paint(&mut self, color: i64) {
        let value = if color > 0 { true } else { false };
        self.data.insert(self.position, value);
    }

    fn input(&self) -> i64 {
        match self.data.get(&self.position) {
            Some(value) => if *value { 1 } else { 0 },
            None => 0,
        }
    }

    fn output(&mut self, value: i64) {
        self.move_forward();
        if self.num_inputs % 2 == 0 {
            self.paint(value);
        } else {
            // Turn
            let direction = if value == 0 { Direction::L } else { Direction::R };
            self.turn(direction);
            self.move_forward();
        }
        self.num_inputs += 1;
    }
}

fn easy(code: &Vec<i64>) -> i64 {
    let mut app = P11::make();
    run_intcode(code.clone(), || app.input(), |val| app.output(val));

    app.data.iter().fold(0, |total, (_, value)| total + if *value { 1 } else { 0 })
}

fn hard(code: &Vec<i64>) -> i64 {
    let mut res: i64 = 0;
    // run_intcode(code.clone(), || 2, |val| res = val);
    res
}

fn main() {
    let code = fs::read_to_string("input/9.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
