use std::fs;
// use std::{thread, time};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use num::signum;

use advent_of_code_2019::intcode::run_intcode;

#[derive(Debug, PartialEq)]
enum TileType {
    Empty,
    Wall,
    Block,
    Paddle,
    Ball
}

struct Tile {
    x: i64,
    y: i64,
    tile: TileType,
}

impl Tile {
    fn make(x: i64, y: i64, tile: i64) -> Tile {
        let tile = match tile {
            1 => TileType::Wall,
            2 => TileType::Block,
            3 => TileType::Paddle,
            4 => TileType::Ball,
            _ => TileType::Empty,
        };

        Tile { x, y, tile }
    }

}

fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

struct P13 {
    data: Vec<i64>,
    tiles: HashMap<(i64, i64), TileType>,
}

impl P13 {
    fn make() -> P13 {
        P13 {
            data: Vec::new(),
            tiles: HashMap::new(),
        }
    }

    fn input(&mut self) -> i64 {
        self.make_move()
    }

    fn output(&mut self, value: i64) {
        self.data.push(value);
    }

    fn count_blocks(&self) -> usize {
        self.tiles.iter()
            .map(|(_, value)| if *value == TileType::Block { 1 } else { 0 })
            .sum()
    }

    fn make_move(&mut self) -> i64 {
        self.process_tiles();

        let tiles = &self.tiles;
        let ball = tiles.iter().filter(|(_, tile)| **tile == TileType::Ball).collect::<Vec<_>>();
        let ball = ball[0].0;
        let paddle = tiles.iter().filter(|(_, tile)| **tile == TileType::Paddle).collect::<Vec<_>>();
        let paddle = paddle[0].0;
        // println!("{:?} {:?}", ball, paddle);
        signum(ball.0 - paddle.0)
    }

    fn process_tiles(&mut self) {
        let tiles = self.data.chunks(3)
            .map(|data| Tile::make(data[0], data[1], data[2]))
            .collect::<Vec<_>>();

        let mut map = HashMap::<(i64, i64), TileType>::new();
        for tile in tiles {
            map.insert((tile.x, tile.y), tile.tile);
        }
        self.tiles = map;
    }

    fn score(&self) -> i64 {
        let score = self.data.chunks(3)
            .filter(|data| data[0] == -1 && data[1] == 0)
            .map(|data| data[2])
            .collect::<Vec<_>>();
        if score.len() == 0 {
            0
        } else {
            score[score.len() - 1]
        }
    }

    #[allow(dead_code)]
    fn as_string(&self) -> String {
        let tiles = &self.tiles;
        let min_pos = (0, 0);
        let max_pos = tiles.iter().fold((0, 0), |total, (key, _)|
            (total.0.max(key.0), total.1.max(key.1)));

        let mut result = Vec::<String>::new();
        result.push(format!("Score: {}, Blocks: {}", self.score(), self.count_blocks()));

        for col in min_pos.1..max_pos.1+1 {
            let mut row_vec = Vec::<char>::new();
            for row in min_pos.0..max_pos.0+1 {
                let tile = tiles.get(&(row, col)).unwrap_or(&TileType::Empty);
                let c = match tile {
                    TileType::Empty => ' ',
                    TileType::Wall => '█',
                    TileType::Block => '░',
                    TileType::Paddle => '━',
                    TileType::Ball => '●',
                };
                row_vec.push(c);
            }

            result.push(row_vec.iter().collect::<String>());
        }

        result.join("\n")
    }
}

fn easy(code: &Vec<i64>) -> usize {
    let app = P13::make();
    let mutex = Arc::new(Mutex::new(app));
    run_intcode(code,
        || mutex.lock().unwrap().input(),
        |val| mutex.lock().unwrap().output(val)
    );

    let mut app = mutex.lock().unwrap();
    app.process_tiles();
    app.count_blocks()
}

fn hard(code: &Vec<i64>) -> i64 {
    let mut code = code.clone();
    code[0] = 2;

    let app = P13::make();
    let mutex = Arc::new(Mutex::new(app));
    run_intcode(&code,
        || {
            let mut app = mutex.lock().unwrap();
            // clear screen
            // print!("{esc}[2J{esc}[1;1H", esc = 27 as char);
            // println!("{}", app.as_string());
            // thread::sleep(time::Duration::from_millis(5));
            app.input()
        },
        |val| mutex.lock().unwrap().output(val)
    );

    let mut app = mutex.lock().unwrap();
    app.process_tiles();
    app.score()
}

fn main() {
    let code = fs::read_to_string("input/13.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
