use std::collections::HashMap;
use std::collections::HashSet;
use num::abs;
use queues::*;
use std::fs;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn test_easy_1() {
        let data = "#########
                    #b.A.@.a#
                    #########";
        let data = parse_input(data);
        assert_eq!(easy(&data), 8);
    }

    #[test]
    fn test_easy_2() {
        let data = "########################
                    #f.D.E.e.C.b.A.@.a.B.c.#
                    ######################.#
                    #d.....................#
                    ########################";
        let data = parse_input(data);
        assert_eq!(easy(&data), 86);
    }

    #[test]
    fn test_easy_3() {
        let data = "########################
                    #...............b.C.D.f#
                    #.######################
                    #.....@.a.B.c.d.A.e.F.g#
                    ########################";
        let data = parse_input(data);
        assert_eq!(easy(&data), 132);
    }


    #[test]
    fn test_easy_4() {
        let data = "#################
                    #i.G..c...e..H.p#
                    ########.########
                    #j.A..b...f..D.o#
                    ########@########
                    #k.E..a...g..B.n#
                    ########.########
                    #l.F..d...h..C.m#
                    #################";
        let data = parse_input(data);
        assert_eq!(easy(&data), 136);
    }


    #[test]
    fn test_easy_5() {
        let data = "########################
                    #@..............ac.GI.b#
                    ###d#e#f################
                    ###A#B#C################
                    ###g#h#i################
                    ########################";
        let data = parse_input(data);
        assert_eq!(easy(&data), 81);
    }

    fn test_hard_1() {
        let data = "#######
                    #a.#Cd#
                    ##...##
                    ##.@.##
                    ##...##
                    #cB#Ab#
                    #######";
        let data = parse_input(data);
        assert_eq!(hard(&data), 8);
    }

}

#[derive(Debug, Copy, Clone)]
enum Tile {
    Wall,
    Empty,
    Player,
    Key(i64),
    Door(i64),
}

type Point = (i64, i64);
type Pos = (Point, Point, Point, Point);
type Map = Vec<Vec<Tile>>;

struct P18Easy {
    map: Map,
    cache: HashMap<(Point, i64), Vec::<(i64, i64, Point)>>
}

impl P18Easy {
    fn new(map: &Map) -> P18Easy {
        P18Easy { map: map.clone(), cache: HashMap::new() }
    }

    fn solve_easy(&mut self, start: Point, unlocked: i64) -> i64 {
        let to_check = self.dfs(start, unlocked);

        let result = to_check.iter()
            .map(|(steps, key, pos)| steps + self.solve_easy(*pos, unlocked | 1<<*key))
            .min()
            .unwrap_or(0);

        result
    }

    fn dfs(&mut self, start: Point, unlocked: i64) -> &Vec::<(i64, i64, Point)> {
        if let Some(result) = self.cache.get(&(start, unlocked)) {
            return result;
        }

        // println!("DFS: {:?} {}", start, unlocked);
        let mut q = Queue::<(i64, Point)>::new();
        let map = &self.map;
        q.add((0, start)).unwrap();
        let offsets = vec!(
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        );

        let mut to_check = Vec::<(i64, i64, Point)>::new();
        let mut used = HashSet::<Point>::new();

        while q.size() > 0 {
            let (steps, pos) = q.remove().unwrap();
            if used.contains(&pos) { continue; }
            used.insert(pos);
            // println!("{} {:?}", steps, pos);
            for offset in &offsets {
                let new_pos = (pos.0 + offset.0, pos.1 + offset.1);
                let new_steps = steps + 1;
                if new_pos.0 < 0 || new_pos.1 < 0 { continue }
                if new_pos.0 >= map.len() as i64 || new_pos.1 >= map[0].len() as i64 { continue }
                let tile = &map[new_pos.0 as usize][new_pos.1 as usize];

                let new_state = (new_steps, new_pos);
                match tile {
                    Tile::Wall => (),
                    Tile::Player => { q.add(new_state).unwrap(); },
                    Tile::Empty => { q.add(new_state).unwrap(); },
                    Tile::Key(i) => {
                        if unlocked & (1 << i) == 0 {
                            to_check.push((new_steps, *i, new_pos));
                        }
                        q.add(new_state).unwrap();
                    },
                    Tile::Door(i) => {
                        if unlocked & (1 << i) != 0 {
                            q.add(new_state).unwrap();
                        }
                    }
                };
            }
        }

        if unlocked.count_ones() < 4{
            println!("{:?} {} {:?}", start, unlocked, to_check.len());
        }

        self.cache.insert((start, unlocked), to_check.clone());
        return self.cache.get(&(start, unlocked));
    }

    fn dfs_multi(&mut self, start: Pos, unlocked: i64) -> i64 {
        /*
        to_check_a
        to_check_b
        to_check_c
        to_check_d
        */

        0
    }
}

fn parse_tile(c: char) -> Tile {
    match c {
        '#' => Tile::Wall,
        '.' => Tile::Empty,
        '@' => Tile::Player,
        c => {
            if c.is_lowercase() {
                Tile::Key((c as i64) - ('a' as i64))
            } else {
                Tile::Door((c as i64) - ('A' as i64))
            }
        }
    }
}

fn parse_input(data: &str) -> Map {
    data.split("\n")
        .map(|line| line.trim().chars().map(|c| parse_tile(c)).collect::<Vec<_>>())
        .collect::<Vec<_>>()
}

fn easy(map: &Map) -> i64 {
    let mut player_pos = (0, 0);
    for row in 0..map.len() {
        for col in 0..map[0].len() {
            if let Tile::Player = map[row][col] {
                player_pos = (row as i64, col as i64);
            }
        }
    }

    let mut p18 = P18Easy::new(map);
    p18.solve_easy(player_pos, 0)
}

fn hard(map: &Map) -> i64 {
0
}

fn main() {
    let input = fs::read_to_string("input/18.txt").expect("Unable to read input file");
    let input = parse_input(&input);
    println!("{}", easy(&input));
    // println!("{}", hard(&input));
    ()
}