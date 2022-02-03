use std::collections::HashSet;
use std::collections::HashMap;
use std::fs;
use pathfinding::prelude::bfs;

type Graph = HashMap<i32, Vec<i32>>;

#[cfg(test)]
mod tests {
    use super::*;
    

    #[test]
    fn test_easy() {
        let data = "0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5";
        let data = parse_input(data);
        assert_eq!(easy(&data), 6);
    }

    #[test]
    fn test_hard() {
        let data = "0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5";
        let data = parse_input(data);
        assert_eq!(hard(&data), 2);
    }
}

pub fn easy(data: &Graph) -> i32 {
    let mut seen = 0;
    bfs(&0, |p| {
        seen += 1;
        data[p].clone()
    },
    |p| *p == -1);
    seen
}

pub fn hard(data: &Graph) -> i32 {
    let mut groups = 0;
    let mut seen = HashSet::new();
    for (from, _) in data {
        if seen.contains(from) { continue; }
        groups += 1;
        bfs(from, |p| {
            seen.insert(p.clone());
            data[p].clone()
        },
        |p| *p == -1);
    }

    groups
}

fn parse_input(data: &str) -> Graph {
    let mut res = HashMap::new();
    for row in data.split("\n") {
        let p = row.split(" <-> ").collect::<Vec<_>>();
        let from = p[0].parse::<i32>().unwrap();
        let to = p[1]
            .split(", ")
            .map(|c| c.parse::<i32>().unwrap())
            .collect::<Vec<_>>();
        res.insert(from, to);
    }

    res
}

pub fn main() {
    let input = fs::read_to_string("input/12.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
