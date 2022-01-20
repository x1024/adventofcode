use std::fs;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy() {
        assert_eq!(check(111111), true);
        assert_eq!(check(223450), false);
        assert_eq!(check(123789), false);
    }

    #[test]
    pub fn test_hard() {
        assert_eq!(check_hard(112233), true);
        assert_eq!(check_hard(123444), false);
        assert_eq!(check_hard(111122), true);
    }
}

fn parse_input(input: &String) -> (i32, i32) {
    let values = input.split("-")
        .map(|num| num.parse::<i32>().expect("Value is not a number"))
        .collect::<Vec<_>>();

    (values[0], values[1])
}

fn check(value: i32) -> bool {
    let chars = value.to_string();
    let chars = chars.chars().map(|d| d.to_digit(10)).collect::<Vec<_>>();

    let mut has_double = false;
    for i in 0..chars.len()-1 {
        if chars[i] > chars[i + 1] { return false }
        if chars[i] == chars[i + 1] { has_double = true }
    }

    return has_double
}

fn check_hard(value: i32) -> bool {
    let chars = value.to_string();
    let chars = chars.chars().map(|d| d.to_digit(10)).collect::<Vec<_>>();

    let mut has_double = false;
    let mut i = 0;
    while i < chars.len() - 1 {
        let mut length = 1;
        while i < chars.len() - 1 && chars[i] == chars[i + 1] {
            i += 1;
            length += 1;
        }

        if length == 2 { has_double = true; }
        i += 1;
    }

    for i in 0..chars.len() - 1 {
        if chars[i] > chars[i + 1] { return false }
    }

    return has_double
}

fn easy(start: i32, end: i32) -> i32 {
    (start..end + 1)
        .map(|i| check(i) as i32)
        .sum::<_>()
}

fn hard(start: i32, end: i32) -> i32 {
    (start..end + 1)
        .map(|i| check_hard(i) as i32)
        .sum::<_>()
}

fn main() {
    let res = fs::read_to_string("input/4.txt").expect("Input file not found");
    let (start, end) = parse_input(&res);
    println!("{}", easy(start, end));
    println!("{}", hard(start, end));
    ()
}
