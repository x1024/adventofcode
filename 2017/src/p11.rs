use counter::Counter;
use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        assert_eq!(easy("ne,ne,ne"), 3);
        assert_eq!(easy("ne,ne,sw,sw"), 0);
        assert_eq!(easy("ne,ne,s,s"), 2);
        assert_eq!(easy("se,sw,se,sw,sw"), 3);
    }

    #[test]
    fn test_hard() {
    }
}

pub fn step_offset(step: &str) -> (i32, i32) {
    match step {
        "n" => (-1, -1),
        "ne" => (0, -1),
        "nw" => (-1, 0),
        "s" => (1, 1),
        "se" => (1, 0),
        "sw" => (0, 1),
        _ => panic!("Invalid movement")
    }
}

pub fn solve(data: &Counter<&str, i32>) -> i32 {
    let result = data.iter()
        .map(|(step, count)| (step_offset(step), count))
        .map(|(offset, count)| (offset.0 * count, offset.1 * count))
        .fold((0, 0), |acc, step| (acc.0 + step.0, acc.1 + step.1));

    if result.0 * result.1 > 0 {
        result.0.abs().max(result.1.abs())
    } else {
        result.0.abs() + result.1.abs()
    }
}

pub fn easy(data: &str) -> i32 {
    solve(&parse_input(data))
}

pub fn hard(data: &str) -> i32 {
    let mut c = Counter::<&str, i32>::new();
    let mut result = 0;
    for step in data.split(",") {
        c[&step] += 1;
        result = result.max(solve(&c));
    }
    result
}

fn parse_input(data: &str) -> counter::Counter<&str, i32> {
    data.split(",").collect::<Counter<_, i32>>()
}

pub fn main() {
    let input = fs::read_to_string("input/11.txt").unwrap();
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
