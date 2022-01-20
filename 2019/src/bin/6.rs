use std::fs;
use std::collections::HashMap;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

use advent_of_code_2019::intcode::run_intcode;

struct Tree<'a> {
    parent: &'a Tree<'a>,
    num_children: usize
}

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy() {
      let input = String::from("COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L");
      let input = parse_input(input).unwrap();
      assert_eq!(easy(&input), 42);
    }

    #[test]
    pub fn test_hard() {
        let input = String::from("COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        K)YOU
        I)SAN");
        let input = parse_input(input).unwrap();
        assert_eq!(hard(&input), 4);
    }
}

fn parse_input(input: String) -> Result<HashMap<String, String>> {
    let res = input
        .split("\n")
        .map(|line| {
            let parts = line.trim().split(")").collect::<Vec<_>>();
            (
                String::from(parts[1]),
                String::from(parts[0])
            )
        })
        .collect::<HashMap<_, _>>();
    Ok(res)
}

fn path(current: &String, data: &HashMap<String, String>) -> Vec<String> {
    let mut path = Vec::<String>::new();
    let mut current = current;
    // println!("{:?}", current);
    loop {
        match data.get(current) {
            Some(value) => {
                path.push(current.clone());
                current = value;
            },
            None => break
        }
    }

    path
}

fn easy(data: &HashMap<String, String>) -> usize {
    data.iter().map(|(node, _)| path(node, data).len()).sum::<usize>()
}

fn hard(data: &HashMap<String, String>) -> usize {
    let you = data.get("YOU").expect("'YOU' not found in data");
    let santa = data.get("SAN").expect("'SAN' not found in data");
    let path_you = path(you, data);
    let path_santa = path(santa, data);

    let mut i = 0;
    loop {
        if path_you[path_you.len() - 1 - i] != path_santa[path_santa.len() - 1 - i] {
            break;
        }
        i += 1;
    };

    let common = path_you.len() + path_santa.len() - i - i;
    common
}

fn main() {
    let code = fs::read_to_string("input/6.txt").unwrap();
    let code = parse_input(code).unwrap();
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
