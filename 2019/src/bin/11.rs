use std::fs;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use advent_of_code_2019::intcode::run_intcode;

type Point = (i32, i32);

#[derive(Debug)]
enum Direction {
    R,
    L,
    U,
    D,
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

    fn count_tiles(&self) -> usize {
        self.data.iter().fold(0, |total, (_, _)| total + 1)
    }

    fn as_string(&self) -> String {
        let min_pos = self.data.iter().fold((0, 0), |total, (key, _)|
            (total.0.min(key.0), total.1.min(key.1)));
        let max_pos = self.data.iter().fold((0, 0), |total, (key, _)|
            (total.0.max(key.0), total.1.max(key.1)));
        // println!("{:?} {:?}", min_pos, max_pos);

        let data = &self.data;
        let mut result = Vec::<String>::new();

        for col in min_pos.1..max_pos.1+1 {
            let mut row_vec = Vec::<char>::new();
            for row in min_pos.0..max_pos.0+1 {
                let val = data.get(&(row, col)).unwrap_or(&false);
                row_vec.push(if *val { '█' } else { ' ' });
            }

            result.push(row_vec.iter().collect::<String>());
        }

        result.join("\n")
    }
}

fn easy(code: &Vec<i64>) -> usize {
    let app = P11::make();
    let mutex = Arc::new(Mutex::new(app));
    run_intcode(code,
        || mutex.lock().unwrap().input(),
        |val| mutex.lock().unwrap().output(val)
    );

    let app = mutex.lock().unwrap();
    app.count_tiles()
}

fn hard(code: &Vec<i64>) -> String {
    let mut app = P11::make();
    app.data.insert((0, 0), true);
    let mutex = Arc::new(Mutex::new(app));

    run_intcode(code,
        || mutex.lock().unwrap().input(),
        |val| mutex.lock().unwrap().output(val)
    );

    let app = mutex.lock().unwrap();
    app.as_string()
}

fn main() {
    let code = fs::read_to_string("input/11.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
