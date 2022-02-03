use std::collections::HashSet;
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

pub fn easy_line(data: &Vec<&str>) -> bool {
    let h: HashSet<&str> = HashSet::from_iter(data.iter().cloned());
    h.len() == data.len()
}

pub fn hard_line(data: &Vec<&str>) -> bool {
    let w = data.iter().map(|word| {
        let mut word = word.chars()
            .collect::<Vec<char>>();
        word.sort();
        word.iter().collect::<String>()
    })
    .collect::<Vec<String>>();
    let h: HashSet<String> = HashSet::from_iter(w.iter().cloned());
    h.len() == data.len()
}


pub fn easy(data: &Vec<Vec<&str>>) -> i32 {
    data.iter().map(|row| easy_line(row) as i32).sum()
}

pub fn hard(data: &Vec<Vec<&str>>) -> i32 {
    data.iter().map(|row| hard_line(row) as i32).sum()
}

fn parse_input(data: &str) -> Vec<Vec<&str>> {
    data.split("\n")
        .map(|row| row.trim().split(" ").collect::<Vec<_>>())
        .collect::<Vec<_>>()
}

pub fn main() {
    let input = fs::read_to_string("input/4.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}