use std::fs;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy() {
        assert_eq!(process_easy(&12), 2);
        assert_eq!(process_easy(&14), 2);
        assert_eq!(process_easy(&1969), 654);
        assert_eq!(process_easy(&100756), 33583);
    }

    #[test]
    pub fn test_hard() {
        assert_eq!(process_hard(&12), 2);
    }
}

fn parse_input() -> Result<Vec<i32>> {
    let res = fs::read_to_string("input/1.txt")?
        .lines()
        .map(|line| line.parse::<i32>().unwrap())
        .collect::<Vec<_>>();
    Ok(res)
}

fn process_easy(val: &i32) -> i32 {
    val / 3 - 2
}

fn process_hard(val: &i32) -> i32 {
    let result = process_easy(val);
    if result <= 0 { 0 } else { result + process_hard(&result) }
}

fn easy() -> Result<i32> {
    Ok(parse_input()?.iter().map(process_easy).sum())
}

fn hard() -> Result<i32> {
    Ok(parse_input()?.iter().map(process_hard).sum())
}

fn main() {
    println!("{}", easy().unwrap());
    println!("{}", hard().unwrap());
    ()
}
