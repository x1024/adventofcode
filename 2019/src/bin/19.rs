use itertools::Itertools;
use advent_of_code_2019::intcode::run_intcode;
use std::fs;
use std::collections::HashMap;

#[derive(Debug, PartialEq, Eq)]
enum TileType {
    Empty,
    TractorBeam,
}


fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

type Point = (i64, i64);

struct P19 {
    code: Vec<i64>,
    ranges: Vec<Point>,
}

impl P19 {
    fn new(code: &Vec<i64>) -> P19 {
        let mut ranges: Vec<Point> = Vec::new();
        ranges.push((0, 1));
        ranges.push((0, 0));
        ranges.push((5, 6));
        ranges.push((7, 9));

        P19 {
            code: code.clone(),
            ranges,
        }
    }

    fn count_tiles(&self, size: Point) -> usize {
        (0..size.0).map(|row|
            (0..size.1).map(|col| self.check_point((row, col)))
                .collect::<Vec<_>>()
        ).flatten()
        .sum::<i64>() as usize
    }

    fn check_point(&self, pos: Point) -> i64 {
        let mut result = 0;
        let mut num_outputs = 0;

        let input = || {
            num_outputs += 1;
            if num_outputs == 1 { pos.0 } else { pos.1 }
        };
        let output = |val| { result = val; };
        run_intcode(&self.code, input, output);

        result
    }

    fn generate_map(&mut self, size: Point) -> Vec<Vec<char>> {
        let mut map: HashMap<Point, i64> = HashMap::new();
        self.generate_ranges(size.0 as usize);

        for row in 0..(size.0 as usize) {
            let result = self.ranges[row];
            for col in 0..result.0 {
                let pos = (row as i64, col);
                map.insert(pos, 0);
            }
            for col in result.0..result.1 {
                let pos = (row as i64, col);
                map.insert(pos, 1);
            }
            for col in result.1..size.1 {
                let pos = (row as i64, col);
                map.insert(pos, 0);
            }
        }

        let map = (0..size.0).map(|row|
            (0..size.1).map(|col| match map.get(&(row, col)).unwrap() {
                0 => '.',
                _ => '█',
            }).collect::<Vec<_>>()
        ).collect::<Vec<_>>();

        map
    }

    fn generate_ranges(&mut self, limit: usize) -> usize {
        let mut row = 0;
        loop {
            if self.ranges.len() <= row {
                let mut start = self.ranges[row - 1].0;
                while self.check_point((row as i64, start)) == 0 { start += 1; }
                let mut end = self.ranges[row-1].1;
                while self.check_point((row as i64, end)) == 1 { end += 1; }
                self.ranges.push((start, end));
            }

            if row >= limit {
                let start = self.ranges[row].0;
                let previous_end = self.ranges[row - limit + 1].1;
                // println!("{} {} {}", row, start, previous_end);
                if (start + (limit - 1) as i64) < previous_end {
                    let x = start as usize;
                    let y = row - limit + 1;
                    return x * 10000 + y;
                }
            }

            row = row + 1;
        }
    }

}

fn easy(code: &Vec<i64>) -> usize {
    let app = P19::new(code);
    // println!("{:#?}", app.generate_map((50, 50)));
    app.count_tiles((50, 50))
}

fn hard(code: &Vec<i64>) -> i64 {
    let app = P19::new(code);
    let limit = 100;

    let mut col = 0;
    let mut row = limit;
    loop {
        while app.check_point((row, col)) == 0 { col += 1; }
        if app.check_point((row - limit + 1, col + limit - 1)) == 1 { break }
        row += 1;
    }

    // println!("{} {}", row - limit + 1, col);
    (row - limit + 1) * 10000 + col
}

fn main() {
    let code = fs::read_to_string("input/19.txt").expect("Unable to read input file");
    let code = parse_input(code);
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
