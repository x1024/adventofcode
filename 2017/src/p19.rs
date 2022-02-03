use std::fs;

#[cfg(test)]
mod tests {
    

    #[test]
    fn test_easy() {
    }

    #[test]
    fn test_hard() {
    }
}

pub fn easy(_data: &str) -> i32 {
    unimplemented!();
}

pub fn hard(_data: &str) -> i32 {
    unimplemented!();
}

fn parse_input(_data: &str) -> &str {
    unimplemented!();
}

pub fn main() {
    let input = fs::read_to_string("input/19.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
