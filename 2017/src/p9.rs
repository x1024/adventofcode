use regex::Captures;
use std::fs;
use regex::Regex;


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        assert_eq!(easy("{}"), 1);
        assert_eq!(easy("{{{}}}"), 6);
        assert_eq!(easy("{{},{}}"), 5);
        assert_eq!(easy("{{{},{},{{}}}}"), 16);
        assert_eq!(easy("{<a>,<a>,<a>,<a>}"), 1);
        assert_eq!(easy("{{<ab>},{<ab>},{<ab>},{<ab>}}"), 9);
        assert_eq!(easy("{{<!!>},{<!!>},{<!!>},{<!!>}}"), 9);
        assert_eq!(easy("{{<a!>},{<a!>},{<a!>},{<ab>}}"), 3);
    }

    #[test]
    fn test_hard() {
        assert_eq!(hard("<>"), 0);
        assert_eq!(hard("<random characters>"), 17);
        assert_eq!(hard("<<<<>"), 3);
        assert_eq!(hard("<{!>}>"), 2);
        assert_eq!(hard("<!!>"), 0);
        assert_eq!(hard("<!!!>>"), 0);
        assert_eq!(hard("<{o\"i!a,<{i<a>"), 10);
    }
}

pub fn cleanup(data: &str) -> (String, usize) {
    let mut data: String = data.to_string();
    let re = Regex::new(r"!.").unwrap();
    loop {
        let mut replaced = false;
        let tmp = re.replace(&data, |_: &Captures| {
            replaced = true;
            ""
        });
        data = tmp.into_owned();
        if !replaced { break; }
    }

    let mut garbage_cleaned = 0;
    let re = Regex::new(r"<.*?>").unwrap();
    loop {
        let mut replaced = false;
        let tmp = re.replace(&data, |caps: &Captures| {
            garbage_cleaned += caps[0].len() - 2;
            replaced = true;
            ""
        });
        data = tmp.into_owned();
        if !replaced { break; }
    }
    data = data.replace(",", "");

    (data, garbage_cleaned)
}

pub fn score(data: &str) -> i32 {
    let mut total = 0;
    let mut level = 0;
    for c in data.chars() {
        if c == '{' {
            level += 1;
        }
        if c == '}' {
            total += level;
            level -= 1;
        }
    }

    total
}

pub fn easy(data: &str) -> i32 {
    let data = cleanup(data).0;
    score(&data)
}

pub fn hard(data: &str) -> usize {
    cleanup(data).1
}

pub fn main() {
    let input = fs::read_to_string("input/9.txt").unwrap();
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
