use std::collections::HashSet;
use queues::IsQueue;
use queues::Queue;
use advent_of_code_2019::intcode::IntCode;
use advent_of_code_2019::intcode::Opcode;
use std::fs;
// use std::{thread, time};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

#[derive(Debug, Copy, Clone, PartialEq)]
enum Direction {
    Up = 1,
    Down = 2,
    Left = 3,
    Right = 4,
}

impl Direction {
    fn reverse(&self) -> Direction {
        match *self {
            Direction::Up => Direction::Down,
            Direction::Down => Direction::Up,
            Direction::Left => Direction::Right,
            Direction::Right => Direction::Left,
        }
    }

    fn all() -> Vec<Direction> {
        vec!(
            Direction::Up,
            Direction::Down,
            Direction::Left,
            Direction::Right,
        )
    }

    fn offset(&self) -> Point {
        match *self {
            Direction::Up => (0, -1),
            Direction::Down => (0, 1),
            Direction::Left => (-1, 0),
            Direction::Right => (1, 0),
        }
    }
}

#[derive(Debug, Copy, Clone, PartialEq)]
enum TileType {
    Wall = 0,
    Empty = 1,
    Goal = 2,
}

fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

type Point = (i64, i64);

struct P15 {
    tiles: HashMap<Point, TileType>,
    stack: Vec<Direction>,
    is_done: bool
}

impl P15 {
    fn new() -> P15 {
        P15 {
            tiles: HashMap::new(),
            stack: vec!(),
            is_done: false,
        }
    }

    fn position(&self) -> Point {
        let mut pos = (0, 0);
        for direction in &self.stack {
            let offset = direction.offset();
            pos = (pos.0 + offset.0, pos.1 + offset.1);
        }
        pos
    }

    fn dfs(&self, start: Point, stop_at_goal: bool) -> i64 {
        let mut q = Queue::<(i64, Point)>::new();
        let mut seen = HashSet::<Point>::new();
        let mut max_steps = 0;
        let directions = Direction::all();
        q.add((0, start)).unwrap();

        while q.size() > 0 {
            let (steps, pos) = q.remove().unwrap();
            max_steps = max_steps.max(steps);
            // println!("{} {} {:?}", q.size(), steps, pos);
            let tile = self.tiles.get(&pos).unwrap();
            if stop_at_goal && tile == &TileType::Goal { return steps; }
            if tile == &TileType::Wall { continue; }

            for direction in &directions {
                let offset = direction.offset();
                let new_pos = (pos.0 + offset.0, pos.1 + offset.1);
                if seen.contains(&new_pos) { continue }

                seen.insert(new_pos);
                q.add((steps + 1, new_pos)).unwrap();
            }
        }

        max_steps
    }

    fn make_move(&mut self) -> Direction {
        let pos = self.position();
        let directions = Direction::all();

        for direction in directions {
            let offset = direction.offset();
            let new_pos = (pos.0 + offset.0, pos.1 + offset.1);
            if !self.tiles.contains_key(&new_pos) {
                self.stack.push(direction);
                return direction;
            }
        }

        if self.stack.is_empty() {
            self.is_done = true;
            return Direction::Up;
        }

        self.stack.pop().unwrap().reverse()
    }

    fn input(&mut self) -> i64 {
        self.make_move() as i64
    }

    fn output(&mut self, value: i64) -> TileType {
        let result = match value {
            1 => TileType::Empty,
            2 => TileType::Goal,
            _ => TileType::Wall,
        };

        let pos = self.position();
        self.tiles.insert(pos, result.clone());

        if result == TileType::Wall {
            self.stack.pop();
        }

        // print!("{esc}[2J{esc}[1;1H", esc = 27 as char);
        // println!("result, {:?} {:?}", pos, result);
        // println!("{}", self.as_string());
        // thread::sleep(time::Duration::from_millis(10));
        result
    }

    #[allow(dead_code)]
    fn as_string(&self) -> String {
        let tiles = &self.tiles;
        let min_pos = tiles.iter().fold((0, 0), |total, (key, _)|
            (total.0.min(key.0), total.1.min(key.1)));
        let max_pos = tiles.iter().fold((0, 0), |total, (key, _)|
            (total.0.max(key.0), total.1.max(key.1)));

        let mut result = Vec::<String>::new();
        let pos = self.position();

        for col in min_pos.1..max_pos.1+1 {
            let mut row_vec = Vec::<char>::new();
            for row in min_pos.0..max_pos.0+1 {
                let tile = tiles.get(&(row, col)).unwrap_or(&TileType::Empty);
                let mut c = match tile {
                    TileType::Empty => ' ',
                    TileType::Wall => '█',
                    TileType::Goal => '●',
                };
                if row == pos.0 && col == pos.1 {
                    c = '@'
                }
                row_vec.push(c);
            }

            result.push(row_vec.iter().collect::<String>());
        }

        result.join("\n")
    }
}

impl P15 {
    fn explore_maze(&mut self, code: &Vec<i64>) {
        let mutex = Arc::new(Mutex::new(self));

        let input = || mutex.lock().unwrap().input();
        let output = |val| { mutex.lock().unwrap().output(val); };


        let mut code = code.clone();
        code.resize(10000, 0);

        let mut c = IntCode::new(code, Box::new(input), Box::new(output));

        loop {
            if let Opcode::Exit = c.run_step() { break }
            if mutex.lock().unwrap().is_done { break }
        }
    }
}


fn easy(code: &Vec<i64>) -> i64 {
    let mut app = P15::new();
    app.explore_maze(code);
    app.dfs((0, 0), true)
}

fn hard(code: &Vec<i64>) -> i64 {
    let mut app = P15::new();
    app.explore_maze(code);
    let goal = app.tiles.iter().filter(|t| *t.1 == TileType::Goal).next().unwrap().0;
    app.dfs(*goal, false) - 1
}

fn main() {
    let code = fs::read_to_string("input/15.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
