use std::collections::HashSet;
use std::fs;
use crate::p10::knot_hash_str;
use pathfinding::prelude::bfs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knot_hash() {
        assert_eq!(parse_knot_hash("a0c2017"), "1010000011000010000000010111");
    }

    #[test]
    fn test_easy() {
        let data = "flqrgnkx";
        let result = get_disk_state(data);
        let result = result[0..8].iter()
            .map(|row| row[0..8].to_string())
            .collect::<Vec<_>>()
            .join("\n");

        let expected = "##.#.#..
                        .#.#.#.#
                        ....#.#.
                        #.#.##.#
                        .##.#...
                        ##..#..#
                        .#...#..
                        ##.#.##.".replace(".", "0")
                                 .replace("#", "1")
                                 .replace(" ", "");
        assert_eq!(result, expected);
    }

    #[test]
    fn test_easy_2() {
        let data = "flqrgnkx";
        assert_eq!(easy(data), 8108);
    }

    #[test]
    fn test_hard() {
        let data = "flqrgnkx";
        assert_eq!(hard(data), 1242);
    }
}

pub fn parse_knot_hash(data: &str) -> String {
    data
        .chars()
        .map(|c| i64::from_str_radix(&format!("{}", c), 16).unwrap())
        .map(|c| format!("{:04b}", c))
        .collect::<Vec<_>>()
        .join("")
}

pub fn get_disk_state(data: &str) -> Vec<String> {
    let rows = 128;
    (0..rows).map(|row: i32| {
        parse_knot_hash(&knot_hash_str(&format!("{}-{}", data, row)))
    }).collect::<Vec<_>>()
}

pub fn easy(data: &str) -> i32 {
    get_disk_state(data).iter().map(|row| 
        row.chars().map(|c| if c == '1' { 1 } else { 0 }).sum::<i32>()
    ).sum::<i32>()
}

pub fn hard(data: &str) -> i32 {
    let state = get_disk_state(data)
        .iter()
        .map(|row| row.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let mut seen = HashSet::<(usize, usize)>::new();
    let mut regions = 0;
    let offsets = vec!(
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    );

    for i in 0..state.len() {
        for j in 0..state[0].len() {
            let p = (i, j);
            if state[i][j] == '1' && !seen.contains(&p) {
                regions += 1;
                bfs(&p, |p| {
                    let mut results = Vec::new();
                    seen.insert(*p);
                    for offset in &offsets {
                        let n0 = p.0 as i32 + offset.0;
                        let n1 = p.1 as i32 + offset.1;
                        if n0 < 0 || n1 < 0 || n0 >= 128 || n1 >= 128 { continue }
                        let n = (n0 as usize, n1 as usize);
                        if state[n0 as usize][n1 as usize] == '1' && !seen.contains(&n) {
                            results.push(n);
                        }
                    }
                    results
                }, |_| false);
            }
        }
    }

    regions
}

pub fn main() {
    let input = fs::read_to_string("input/14.txt").unwrap();
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
