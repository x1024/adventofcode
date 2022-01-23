use std::fs;
use std::f64::consts::PI;
use std::collections::HashSet;
use std::collections::HashMap;

type Point = (i32, i32);

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy_1() {
        let data = ".#..#
         .....
         #####
         ....#
         ...##".to_string();
        assert_eq!(easy(data), 8);
    }

    #[test]
    pub fn test_easy_2() {
        let data = ".#..#..###
                    ####.###.#
                    ....###.#.
                    ..###.##.#
                    ##.##.#.#.
                    ....###..#
                    ..#.#..#.#
                    #..#.#.###
                    .##...##.#
                    .....#.#..".to_string();
        assert_eq!(easy(data), 41);
    }

    #[test]
    pub fn test_easy_3() {
        let data = ".#..##.###...#######
                    ##.############..##.
                    .#.######.########.#
                    .###.#######.####.#.
                    #####.##.#.##.###.##
                    ..#####..#.#########
                    ####################
                    #.####....###.#.#.##
                    ##.#################
                    #####.##.###..####..
                    ..######..##.#######
                    ####.##.####...##..#
                    .#####..#.######.###
                    ##...#.##########...
                    #.##########.#######
                    .####.#.###.###.#.##
                    ....##.##.###..#####
                    .#.#.###########.###
                    #.#.#.#####.####.###
                    ###.##.####.##.#..##".to_string();
        assert_eq!(easy(data), 210);
    }

    #[test]
    pub fn test_hard_1() {
        let data = ".#..##.###...#######
                    ##.############..##.
                    .#.######.########.#
                    .###.#######.####.#.
                    #####.##.#.##.###.##
                    ..#####..#.#########
                    ####################
                    #.####....###.#.#.##
                    ##.#################
                    #####.##.###..####..
                    ..######..##.#######
                    ####.##.####...##..#
                    .#####..#.######.###
                    ##...#.##########...
                    #.##########.#######
                    .####.#.###.###.#.##
                    ....##.##.###..#####
                    .#.#.###########.###
                    #.#.#.#####.####.###
                    ###.##.####.##.#..##".to_string();
        assert_eq!(hard(data), 802);
    }
}

fn parse_input(data: String) -> Vec<Point> {
    data
        .split("\n")
        .map(|line| line.trim())
        .enumerate()
        .map(|(y, line)|
            line.chars().enumerate().map(move |(x, c)| (x, y, c)))
        .flatten()
        .filter(|(_, _, c)| *c == '#')
        .map(|(x, y, _)| (x as i32, y as i32))
        .collect::<Vec<_>>()
}

fn angle(dx: i32, dy: i32) -> f64 {
    -(dx as f64).atan2(dy as f64)
}

fn distance(dx: i32, dy: i32) -> i64 {
    (dx * dx + dy * dy) as i64
}

fn find_best_station(code: String) -> (Point, usize) {
    let mut result = 0;
    let points = parse_input(code);
    let mut station: Point = points[0];

    for p1 in &points {
        let mut angles = HashSet::<i64>::new();
        for p2 in &points {
            if p1 == p2 { continue }
            let dx = p1.0 - p2.0;
            let dy = p1.1 - p2.1;
            let angle = (angle(dx, dy) * 10000.0) as i64;
            angles.insert(angle);
        }

        if angles.len() > result {
            result = angles.len();
            station = *p1;
        }
    }

    (station, result)
}

fn easy(code: String) -> usize {
    find_best_station(code).1
}

fn hard(code: String) -> usize {
    let station = find_best_station(code.clone()).0;
    let points = parse_input(code);

    let mut used = HashSet::<Point>::new();
    used.insert(station);
    let angle_multiplier = 100000.0;
    let two_pi = 2.0 * PI;
    let mut min_angle = angle(0, -10) - 0.0001;
    let mut min_point = points[0];
    for i in 0..200 {
        let mut min_result = (two_pi - 0.0001, 9999999999);

        for p in &points {
            if used.contains(p) { continue }
            let dx = p.0 - station.0;
            let dy = p.1 - station.1;
            let angle = angle(dx, dy);
            let distance = distance(dx, dy);
            
            let angle_diff = (angle - min_angle + two_pi) % two_pi;
            let result = (angle_diff, distance);
            if angle_diff < 0.0 { continue; }
            if result < min_result {
                // println!("{:?} {:?}", result, *p);
                min_result = result;
                min_point = *p;
          }
        }

        used.insert(min_point);
        // println!("{} {:?} {:?}", i + 1, min_point, min_result);
        // println!("{:?}", min_angle);
        // println!("{:?}", min_result.0);
        min_angle += min_result.0 + 0.000001;
        // println!("{:?}", min_angle);
    }

    (min_point.0 * 100 + min_point.1) as usize
}

fn main() {
    let code = fs::read_to_string("input/10.txt").expect("Unable to read input file");
    println!("{}", easy(code.clone()));
    println!("{}", hard(code.clone()));
    ()
}
