use itertools::Itertools;
use num::abs;
use std::collections::HashSet;
use std::collections::HashMap;
use std::fs;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn test_score() {
        let input = ".....
                     .....
                     .....
                     #....
                     .#...";
        let game = GOL::new(&input, false);
        assert_eq!(game.score(), 2129920);
    }

    #[test]
    fn test_easy() {
        let input = "....#
                     #..#.
                     #..##
                     ..#..
                     #....";
        assert_eq!(easy(input), 2129920);
    }

    #[test]
    fn test_hard() {
        let input = "....#
                     #..#.
                     #..##
                     ..#..
                     #....";
        assert_eq!(hard(input, 10), 99);
    }
}

type GOLBoard = Vec<Vec<bool>>;

#[derive(Debug, Clone)]
struct GOL {
    data: HashMap<i64, GOLBoard>,
    round: i64,
    max_level: i64,
    neighbors: Vec<Vec<(i64, i64, i64)>>,
    recursive: bool
}

impl GOL {
    fn new(input: &str, recursive: bool) -> GOL {
        let input = input.split("\n")
            .map(|row| row.trim().chars().collect::<Vec<_>>())
            .collect::<Vec<_>>();
        let w = input.len();
        let h = input[0].len();

        let mut data = HashMap::new();
        let mut board = Self::make_board();

        for row in 0..h {
            for col in 0..w {
                if input[row][col] == '#' {
                    board[row][col] = true;
                }
            }
        }

        data.insert(0, board);

        let neighbors = if recursive {
            Self::initialize_neighbors_recursive()
        } else {
            Self::initialize_neighbors()
        };

        let gol = GOL { data, round: 0, max_level: 0, neighbors, recursive };
        gol
    }

    fn initialize_neighbors() -> Vec<Vec<(i64, i64, i64)>> {
        let mut neighbors: Vec<Vec<(i64, i64, i64)>> = Vec::new();
        for _ in 0..5*5 { neighbors.push(Vec::new()); }
        for i in 0..5*5 {
            let (row, col) = (i/5, i % 5);
            let n = &mut neighbors[i as usize];
            n.push((0, row - 1, col));
            n.push((0, row + 1, col));
            n.push((0, row, col - 1));
            n.push((0, row, col + 1));
        }

        neighbors
    }

    fn initialize_neighbors_recursive() -> Vec<Vec<(i64, i64, i64)>> {
        /*
        0  1  2  3  4
        5  6  7  8  9
        10 11 12 13 14
        15 16 17 18 19
        20 21 22 23 24
        */
        let tile = |i: &i64| -> (i64, i64) { (i/5, i % 5) };

        let top_edge     = [0, 1, 2, 3, 4].iter().map(tile).collect::<Vec<_>>();
        let left_edge    = [0, 5, 10, 15, 20].iter().map(tile).collect::<Vec<_>>();
        let bottom_edge  = [20, 21, 22, 23, 24].iter().map(tile).collect::<Vec<_>>();
        let right_edge   = [4, 9, 14, 19, 24].iter().map(tile).collect::<Vec<_>>();
        let left_inner_tile   = (2, 1);
        let right_inner_tile  = (2, 3);
        let top_inner_tile    = (1, 2);
        let bottom_inner_tile = (3, 2);

        let mut neighbors: Vec<Vec<(i64, i64, i64)>> = Vec::new();
        for _ in 0..5*5 { neighbors.push(Vec::new()); }
        for i in 0..5*5 {
            let tile = tile(&i);
            let (row, col) = tile;
            let n = &mut neighbors[i as usize];

            // top neighbours
            if top_edge.contains(&tile) { n.push((-1, top_inner_tile.0, top_inner_tile.1)) }
            else if bottom_inner_tile == tile { n.extend(bottom_edge.iter().map(|(row, col)| (1, *row, *col))); }
            else { n.push((0, row - 1, col)); }

            // bottom neighbours
            if bottom_edge.contains(&tile) { n.push((-1, bottom_inner_tile.0, bottom_inner_tile.1)) }
            else if top_inner_tile == tile { n.extend(top_edge.iter().map(|(row, col)| (1, *row, *col))); }
            else { n.push((0, row + 1, col)); }

            // left neighbours
            if left_edge.contains(&tile) { n.push((-1, left_inner_tile.0, left_inner_tile.1)) }
            else if right_inner_tile == tile { n.extend(right_edge.iter().map(|(row, col)| (1, *row, *col))); }
            else { n.push((0, row, col - 1)); }

            // right neighbours
            if right_edge.contains(&tile) { n.push((-1, right_inner_tile.0, right_inner_tile.1)) }
            else if left_inner_tile == tile { n.extend(left_edge.iter().map(|(row, col)| (1, *row, *col))); }
            else { n.push((0, row, col + 1)); }

            // println!("{} {} {:?} {:?}", row, col, tile, n);
        }

        neighbors
    }


    fn make_board() -> GOLBoard {
        let mut board = Vec::<Vec::<bool>>::new();
        for _ in 0..5 {
            let mut row = Vec::new();
            row.resize(5, false);
            board.push(row);
        }

        board
    }

    fn score(&self) -> usize {
        let data = &self.data;

        let board = data.get(&0).unwrap();

        let mut counter = 1;
        let mut total = 0;
        for row in 0..5 {
            for col in 0..5 {
                if board[row][col] {
                    total += counter;
                }
                counter <<= 1;
            }
        }

        total
    }

    fn board_cells(&self, board: &Vec<Vec<bool>>) -> usize {
        let mut sum = board.iter().map(|row|
            row.iter().map(|cell| if *cell { 1 } else { 0 })
        )
        .flatten()
        .sum();

        if self.recursive {
            // we don't count the middle cell in recursive boards
            let middle_cell = if board[2][2] { 1 } else { 0 };
            sum -= middle_cell;
        }

        sum
    }

    fn cell_count(&self) -> usize {
        self.data.iter().map(|(_, board)| self.board_cells(board)).sum()
    }

    fn get(&self, level: i64, row: i64, col: i64) -> i64 {
        if row < 0 || row >= 5 || col < 0 || col >= 5 { return 0}
        if let Some(board) = self.data.get(&level) {
            board[row as usize][col as usize] as i64
        } else {
            0
        }
    }

    fn neighbors(&self, level: i64, row: usize, col: usize) -> i64 {
        if abs(level) > self.max_level { return 0 }
        let index = row * 5 + col as usize;
        self.neighbors[index].iter().map(
            |(offset, r, c)| self.get(level + offset, *r, *c)
        ).sum()
    }

    fn update(&mut self) {
        if self.recursive && self.round % 2 == 0 {
            let data = &mut self.data;
            // On every two turns, the recursive board can go one level deeper
            self.max_level += 1;
            data.insert(-self.max_level, Self::make_board());
            data.insert(self.max_level, Self::make_board());
        }

        self.round += 1;
        let data = &self.data;
        let mut new_data = HashMap::new();

        for level in -self.max_level..self.max_level + 1 {
            let board = data.get(&level).unwrap();
            let mut new_board = board.clone();
            // println!("{} {}", self.round, level);
            for row in 0..5 {
                for col in 0..5 {
                    let neighbors = self.neighbors(level, row, col);
                    let new_val = if board[row as usize][col as usize] {
                        neighbors == 1
                    } else {
                        neighbors >= 1 && neighbors <= 2
                    };
                    new_board[row as usize][col as usize] = new_val;
                }
            }
            new_data.insert(level, new_board);
        }

        self.data = new_data;
    }
}

impl std::fmt::Display for GOL {
    // This trait requires `fmt` with this exact signature.
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        // Write strictly the first element into the supplied output
        // stream: `f`. Returns `fmt::Result` which indicates whether the
        // operation succeeded or failed. Note that `write!` uses syntax which
        // is very similar to `println!`.
        let mut boards = Vec::new();

        for level in -self.max_level..self.max_level + 1 {
            let board = self.data.get(&level).unwrap();
            let mut board_string = board.iter()
                .map(|row| row.iter()
                    .map(|&c| if c { '#' } else { '.' })
                    .collect::<Vec<_>>()
                )
                .collect::<Vec<_>>();
            if self.recursive {
                board_string[2][2] = '?';
            }
            boards.push(board_string);
        }

        let board_string = (0..5)
            .map(|i| boards.iter()
                .map(|board| board[i].iter().collect::<String>()).join("\t"))
                .join("\n");

        write!(f, "Round: {}\nCount: {}\nScore: {}\n{}\n",
            self.round,
            self.cell_count(),
            self.score(),
            board_string)
    }
}

fn easy(input: &str) -> usize {
    let mut game = GOL::new(&input, false);
    let mut scores = HashSet::new();
    loop {
        // println!("{}", game);
        if !scores.insert(game.score()) { break}
        game.update();
    }
    game.score()
}

fn hard(input: &str, rounds: usize) -> usize {
    let mut game = GOL::new(&input, true);
    // println!("{}", game);
    for _ in 0..rounds {
        game.update();
        // println!("{}", game);
    }

    game.cell_count()
}

fn main() {
    let input = fs::read_to_string("input/24.txt").expect("Unable to read input file");
    println!("{}", easy(&input));
    println!("{}", hard(&input, 200));
    ()
}