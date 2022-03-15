use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        assert_eq!(easy(3), 638);
    }

    #[test]
    fn test_hard() {
    }
}

pub fn easy(step: i32) -> i32 {
    unimplemented!();
}

pub fn hard(_data: &str) -> i32 {
    unimplemented!();
}

fn parse_input(_data: &str) -> &str {
    unimplemented!();
}

pub fn main() {
    let input = fs::read_to_string("input/17.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
