use advent_of_code_2019::intcode::run_intcode_ascii;
use std::fs;
use std::{thread, time};
use std::collections::HashMap;
// use std::sync::{Arc, Mutex};

#[derive(Debug, PartialEq, Eq)]
enum TileType {
    Empty,
    Scaffold,
}

fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

type Point = (i64, i64);

struct P21 {
    code: Vec<i64>,
    map: HashMap<Point, TileType>,
}

impl P21 {
    fn new() -> P21 {
        P21 {
            code: Vec::new(),
            map: HashMap::new(),
        }
    }

    fn output(&mut self, value: i64) {
        self.code.push(value)
    }

    fn render_map(&mut self) {
        let map = self.code.iter()
            .map(|c| (*c as u8) as char)
            .collect::<String>();
        // println!("{}", map);
        let map = map.split("\n").collect::<Vec<_>>();
        self.map = map
            .iter()
            .enumerate()
            .map(|(row, line)|
                line.chars()
                    .enumerate()
                    .map(move |(col, c)| {
                        let tile = match c {
                            '.' => TileType::Empty,
                            _ => TileType::Scaffold,
                        };
                        ((row as i64, col as i64), tile)
                    }
            ))
            .flatten()
            .collect::<HashMap<_, _>>();
    }

    fn print_map(&mut self) {
        let map = self.code.iter()
            .map(|c| (*c as u8) as char)
            .collect::<String>();

        // clear screen
        // print!("{esc}[2J{esc}[1;1H", esc = 27 as char);
        println!("{}", map);
        thread::sleep(time::Duration::from_millis(100));
    }

    fn print_output(&mut self) {
        // On two consequitive newlines, print out the current output buffer
        let code = &self.code;
        let l = code.len();
        let newline = '\n' as i64;
        if code.len() >= 2 && code[l - 1] == newline && code[l - 2] == newline {
            self.render_map();
            self.print_map();
            self.map.clear();
            self.code.clear();
        }
    }
        
    fn run_bot(&mut self, code: &Vec<i64>, input: &str, print_output: bool) -> i64 {
        run_intcode_ascii(&code, input, |val| {
            self.output(val);
            if print_output { self.print_output(); }
        });

        self.code[self.code.len() - 1]
    }
}

fn easy(code: &Vec<i64>) -> i64 {
    let mut app = P21::new();
    let show_video = false;
    // Jump if there's any hole in tiles 1-3, but NO hole in tile 4
    let input = "NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
";
    app.run_bot(code, input, show_video)
}

fn hard(code: &Vec<i64>) -> i64 {
    let mut app = P21::new();
    let show_video = false;
    // Jump if there's any hole in tiles 1 and 3, but NO hole in tile 4
    // and jumping to tile 4 doesn't immediately lead to game over
    // (this can happen if there's both a hole in tile 5 and a hole in tile 8,
    // meaning that we need to immediately jump from 4, but there's nowhere to jump to)
    let input = "NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT H T
NOT T T
OR E T
AND T J
RUN
";
    app.run_bot(code, input, show_video)
}


fn main() {
    let code = fs::read_to_string("input/21.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}