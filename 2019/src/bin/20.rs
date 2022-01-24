use std::collections::HashMap;
use pathfinding::directed::dijkstra::dijkstra;
use std::fs;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn test_easy_1() {
        let data = 
"         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       ";
        let data = P20Map::from_map(&data);
        assert_eq!(easy(&data), 23);
    }

    #[test]
    fn test_easy_2() {
        let data = 
"                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               ";
        let data = P20Map::from_map(&data);
        assert_eq!(easy(&data), 58);
    }

    #[test]
    fn test_hard_1() {
        let data = 
"         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       ";
        let data = P20Map::from_map(&data);
        assert_eq!(hard(&data), 26);
    }

    #[test]
    fn test_hard_2() {
        let data = 
"             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     ";
        let data = P20Map::from_map(&data);
        assert_eq!(hard(&data), 396);
    }

}

#[derive(Debug)]
#[derive(std::clone::Clone)]
enum Tile {
    Wall,
    Empty,
    PortalOuter(String),
    PortalInner(String),
}

type Point = (i64, i64);
type Point3 = (i64, i64, i64);
type Map = HashMap<Point, Tile>;

#[derive(Debug)]
struct P20Map {
    start: Point,
    finish: Point,
    // maps input portal to output portal AND potential level change
    portals: HashMap<Point, Point>,
    map: Map,
}

impl P20Map {
    fn from_map(data: &str) -> P20Map {
        let data = data.split("\n")
            .map(|row| row.chars().collect::<Vec<_>>())
            .collect::<Vec<_>>();

        let rows = data.len();
        let cols = data[0].len();

        let mut map = Map::new();

        let mut aa = (0, 0);
        let mut zz = (0, 0);

        for row in 0..rows {
            for col in 0..cols {
                let cell = data[row][col];
                let pos = (row as i64, col as i64);
                let tile = if cell == '.' {
                    Tile::Empty
                } else if cell >= 'A' && cell <= 'Z' {
                    if let Some(name) = P20Map::get_portal(&data, row as i64, col as i64) {
                        if name == "AA" { aa = pos; }
                        if name == "ZZ" { zz = pos; }
                        let is_outer = row == 1 || row == rows - 2 || col == 1 || col == cols - 2;
                        if is_outer {
                            Tile::PortalOuter(name)
                        } else {
                            Tile::PortalInner(name)
                        }
                    } else {
                        Tile::Wall
                    }
                } else {
                    Tile::Wall
                };

                map.insert(pos, tile);
            }
        }

        let outer_portals = map.iter().filter(|(_, val)| {
            if let Tile::PortalOuter(_) = val { true } else { false }
        }).collect::<Vec<_>>();

        let inner_portals = map.iter().filter(|(_, val)| {
            if let Tile::PortalInner(_) = val { true } else { false }
        }).collect::<Vec<_>>();

        let mut portals: HashMap<Point, Point> = HashMap::new();
        for (&pos_outer, tile1) in &outer_portals {
            if let Tile::PortalOuter(name1) = tile1 {
                for (&pos_inner, tile2) in &inner_portals {
                    if let Tile::PortalInner(name2) = tile2 {
                        if name1 != name2 { continue }
                        // println!("{:?} {:?} {}", pos_outer, pos_inner, name2);
                        portals.insert(pos_outer, pos_inner);
                        portals.insert(pos_inner, pos_outer);
                    }
                }
            }
        }

        P20Map {
            map,
            start: aa,
            finish: zz,
            portals,
        }
    }

    fn get_portal(data: &Vec<Vec<char>>, row: i64, col: i64) -> std::option::Option<String> {
        let offsets: Vec::<Point> = vec!(
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        );

        let mut has_empty_tile = false;
        let mut letters = vec!(data[row as usize][col as usize]);
        for offset in &offsets {
            let pr = row + offset.0;
            let pc = col + offset.1;
            if pr < 0 || pc < 0 { return None; }
            if pr as usize >= data.len() || pc as usize >= data[0].len() { return None; }

            let cell = data[pr as usize][pc as usize];
            if cell == '.' {
                has_empty_tile = true;
            } else if cell >= 'A' && cell <= 'Z' {
                letters.push(cell);
            }
        }

        if !has_empty_tile {
            return None;
        }

        letters.sort();
        Some(letters.iter().collect::<String>())
    }

    fn neighbors(&self, pos: Point3, use_levels: bool) -> Vec<(Point3, i64)> {
        // println!("{:?}", pos);

        let offsets: Vec::<Point> = vec!(
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        );
        let mut v = Vec::<(Point3, i64)>::new();
        let level = pos.2;

        for offset in offsets {
            let p = ((pos.0 + offset.0), (pos.1 + offset.1));
            let tile = self.map.get(&p).unwrap_or(&Tile::Wall);

            match tile {
                Tile::Empty => { v.push(((p.0, p.1, level), 1)); },
                Tile::Wall => (),
                Tile::PortalInner(_) => {
                    let new_pos = if let Some(pos) = self.portals.get(&p) {
                        let max_level = 99999;
                        if level < max_level || !use_levels {
                            let new_level = if use_levels { level + 1 } else { level };
                            ((pos.0, pos.1, new_level), 0)
                        } else {
                            // At level 0 this isn't a portal.
                            ((p.0, p.1, level), 1)
                        }
                    } else {
                        ((p.0, p.1, level), 1)
                    };
                    v.push(new_pos);
                }
                Tile::PortalOuter(_) => {
                    let new_pos = if let Some(pos) = self.portals.get(&p) {
                        if level > 0 || !use_levels {
                            let new_level = if use_levels { level - 1 } else { level };
                            ((pos.0, pos.1, new_level), 0)
                        } else {
                            // At level 0 this isn't a portal.
                            ((p.0, p.1, level), 1)
                        }
                    } else {
                        ((p.0, p.1, level), 1)
                    };
                    v.push(new_pos);
                }
            }
        }

        v
    }

    fn solve(&self, use_levels: bool) -> i64 {
        let start = (self.start.0, self.start.1, 0);
        let finish = (self.finish.0, self.finish.1, 0);
        let result = dijkstra(&start,
                    |pos| self.neighbors(*pos, use_levels),
                    |pos| *pos == finish)
            .unwrap();

        result.1 - 2
    }
}


fn easy(map: &P20Map) -> i64 {
    map.solve(false)
}

fn hard(map: &P20Map) -> i64 {
    map.solve(true)
}

fn main() {
    let input = fs::read_to_string("input/20.txt").expect("Unable to read input file");
    let input = P20Map::from_map(&input);

    println!("{}", easy(&input));
    println!("{}", hard(&input));
    ()
}