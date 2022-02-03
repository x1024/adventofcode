use std::collections::HashSet;
use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        let v = vec!(0, 2, 7, 0);
        assert_eq!(easy(&v), 5);
    }

    #[test]
    fn test_hard() {
        let v = vec!(0, 2, 7, 0);
        assert_eq!(hard(&v), 4);
    }
}

pub fn solve(data: &Vec<i32>, check_loop: bool) -> i32 {
    let mut data = data.clone();
    let mut seen = HashSet::new();
    let mut cycle = 0;
    let mut first_item: String = String::new();
    let mut first_item_time = 0;
    loop {
        let mut max = 0;
        let s = data.iter().map(|c| format!("{}", c)).collect::<String>();
        if !seen.insert(s.clone()) {
            if !check_loop {
                return cycle;
            } else {
                if first_item.len() == 0 { 
                    first_item = s;
                    first_item_time = cycle;
                } else {
                    if s == first_item {
                        return cycle - first_item_time;
                    }
                }

            }
        }

        for i in 1..data.len() {
            // println!("{} {}", i, max);
            if data[i] > data[max] {
                max = i;
            }
        }

        let mut t = data[max];
        data[max] = 0;
        // println!("{} {}", max, t);
        while t > 0 {
            max = (max + 1) % data.len();
            data[max] += 1;
            t -= 1;
        }

        cycle += 1;
    }
}

pub fn easy(data: &Vec<i32>) -> i32 {
    solve(data, false)
}

pub fn hard(data: &Vec<i32>) -> i32 {
    solve(data, true)
}

fn parse_input(data: &str) -> Vec<i32> {
    data.split_whitespace().map(|cell| cell.parse::<i32>().unwrap()).collect::<Vec<_>>()
}

pub fn main() {
    let input = fs::read_to_string("input/6.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
