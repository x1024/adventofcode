use advent_of_code_2019::intcode::run_intcode;
use std::fs;
use std::{thread, time};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

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

struct P17 {
    code: Vec<i64>,
    map: HashMap<Point, TileType>,
}

impl P17 {
    fn new() -> P17 {
        P17 {
            code: Vec::new(),
            map: HashMap::new(),
        }
    }

    fn output(&mut self, value: i64) {
        self.code.push(value)
    }

    fn read_map(&mut self, code: &Vec<i64>) {
        let mutex = Arc::new(Mutex::new(self));
        run_intcode(&code, ||0, |val| { mutex.lock().unwrap().output(val); });
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
        
    fn check_map(&mut self) -> i64 {
        let offsets: Vec<Point> = vec!(
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        );

        let min_pos = self.map.iter().fold((0, 0), |total, (key, _)| (total.0.min(key.0), total.1.min(key.1)));
        let max_pos = self.map.iter().fold((0, 0), |total, (key, _)| (total.0.max(key.0), total.1.max(key.1)));
        let rows = max_pos.0 - min_pos.0;
        let cols = max_pos.1 - min_pos.1;
        // println!("{} {}", rows, cols);
        
        let mut result = 0;
        for row in 1..rows-1 {
            for col in 1..cols-1 {
                let num_scaffolds = offsets.iter().map(|offset| {
                    let tile = self.map.get(&(row + offset.0, col + offset.1))
                        .unwrap_or(&TileType::Empty);
                    if *tile == TileType::Scaffold { 1 } else { 0 }
                }).sum::<i64>();
                if num_scaffolds == 4 {
                    result += row * col;
                    // println!("{} {} {}", row, col, num_scaffolds);
                }
            }
        }

        // println!("{} {}", rows, cols);
        result
    }

    fn run_bot(&mut self, code: &Vec<i64>, input: &String) -> i64 {
        let mut code = code.clone();
        self.map.clear();
        self.code.clear();

        let print_output = input.find("y").unwrap_or(input.len() * 2) < input.len();

        let mutex = Arc::new(Mutex::new(self));
        let mut index = 0;
        let input = input.chars().collect::<Vec<_>>();

        code[0] = 2;

        run_intcode(&code, || {
            let value = input[index] as i64;
            // println!("INPUT {} {} {}", index, input[index], value);
            index += 1;
            value
        }
        , |val| {
            let mut app = mutex.lock().unwrap();
            let code = &app.code;

            // On two consequitive newlines, print out the current output buffer
            if print_output && code.len() >= 2 && code[code.len() - 1] == val && val == '\n' as i64 {
                app.render_map();
                let map = app.code.iter()
                    .map(|c| (*c as u8) as char)
                    .collect::<String>();

                // clear screen
                print!("{esc}[2J{esc}[1;1H", esc = 27 as char);
                println!("{}", map);
                app.map.clear();
                app.code.clear();
                thread::sleep(time::Duration::from_millis(50));
            }
            app.output(val);
        });

        let app = mutex.lock().unwrap();
        app.code[app.code.len() - 1]
    }
}

fn easy(code: &Vec<i64>) -> i64 {
    let mut app = P17::new();
    app.read_map(code);
    app.render_map();
    app.check_map()
}

fn hard(code: &Vec<i64>) -> i64 {
    // Basically, just look at the map from the easy problem and manually figure out what the program is
    // Every "sub-program" moves on an integer amount of full lines. it never stops halfway through a line.

    /*
    The map looks like this (starting from the ^ sign near the center):

    ......................#######......................
    ......................#.....#......................
    ..................#######...#......................
    ..................#...#.#...#......................
    #########.........#...#.#...#......................
    #.......#.........#...#.#...#......................
    #.......#.#############.#...#......................
    #.......#.#.......#.....#...#......................
    #.......#.#.......#...#######......................
    #.......#.#.......#.....#..........................
    #######.#########.#########........................
    ......#...#.....#.......#.#........................
    ......#...#.....#.......#.#........................
    ......#...#.....#.......#.#........................
    ......#...#.#############.#.........#######........
    ......#...#.#...#.........#.........#.....#........
    ......#...#.#...#.........#########.#.....#........
    ......#...#.#...#.................#.#.....#........
    ......#...#######.................#.#.....#........
    ......#.....#.....................#.#.....#........
    ......#.....#.....................#.#.....#........
    ......#.....#.....................#.#.....#........
    ......#######...........^############.#########....
    ..................................#...#...#...#....
    ..................................#...#...#...#....
    ..................................#...#...#...#....
    ..................................#...#...#########
    ..................................#...#.......#...#
    ..................................#############...#
    ......................................#...........#
    ................................#######...........#
    ................................#.................#
    ................................#.....#############
    ................................#.....#............
    ................................#.....#............
    ................................#.....#............
    ................................#.....#............
    ................................#.....#............
    ................................#######............
    */

    let main_program = "A,A,C,B,A,B,A,C,B,C";
    let program_a = "R,12,L,8,R,6";
    let program_b = "L,8,R,8,R,6,R,12";
    let program_c = "R,12,L,6,R,6,R,8,R,6";
    // let show_video = "y\n";
    let show_video = "n\n";

    let mut app = P17::new();
    let input = vec!(main_program, program_a, program_b, program_c, show_video).join("\n");
    app.run_bot(code, &input)
}

fn main() {
    let code = fs::read_to_string("input/17.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
