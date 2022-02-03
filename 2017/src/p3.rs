use std::collections::HashMap;
use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        assert_eq!(easy(1), 0);
        assert_eq!(easy(9), 2);
        assert_eq!(easy(25), 4);
    }

    #[test]
    fn test_easy_2() {
        assert_eq!(easy(12), 3);
        assert_eq!(easy(23), 2);
        assert_eq!(easy(1024), 31);
    }

    #[test]
    fn test_hard() {
    }
}

pub fn coordinates(input: i32) -> (i32, i32) {
    let mut n = 1;

    while (n+2) * (n+2) < input {
        n += 2;
    }

    let mut pos = ((n / 2), n / 2);
    let mut remaining = input - n*n;

    if remaining > 0 {
        pos = (pos.0 + 1, pos.1 + 1);
    }

    let offsets = [
        (0, -1),
        (-1, 0),
        (0, 1),
        (1, 0),
    ];

    for offset in offsets {
        let mut side = n + 1;
        while remaining > 0 && side > 0 {
            pos = (pos.0 + offset.0, pos.1 + offset.1);
            remaining -= 1;
            side -= 1;
        }
    }

    pos
}

pub fn easy(input: i32) -> i32 {
    let pos = coordinates(input);
    pos.0.abs() + pos.1.abs()
}

pub fn hard(input: i32) -> i32 {
    let mut data = HashMap::new();
    data.insert((0, 0), 1);

    let mut i = 1;
    loop {
        let pos = coordinates(i);
        let mut sum = 0;
        for dx in -1..1+1 {
            for dy in -1..1+1 {
                sum += data.get(&(pos.0 + dx, pos.1 + dy)).unwrap_or(&0);
            }
        }
        // println!("{} {:?} {}", i, pos, sum);
        data.insert(pos, sum);
        if sum > input { return sum }
        i += 1
    }
}

pub fn main() {
    let input = fs::read_to_string("input/3.txt").unwrap().parse::<i32>().unwrap();
    println!("{}", easy(input));
    println!("{}", hard(input));
}
