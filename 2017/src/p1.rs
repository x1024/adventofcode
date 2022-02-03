use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        assert_eq!(easy("1122"), 3);
        assert_eq!(easy("1111"), 4);
        assert_eq!(easy("1234"), 0);
        assert_eq!(easy("91212129"), 9);
    }

    #[test]
    fn test_hard() {
        assert_eq!(hard("1212"), 6);
        assert_eq!(hard("1221"), 0);
        assert_eq!(hard("123425"), 4);
        assert_eq!(hard("123123"), 12);
        assert_eq!(hard("12131415"), 4);
    }
}

pub fn easy(data: &str) -> i32 {
    let data = data.chars().map(|c| c.to_string().parse::<i32>().unwrap()).collect::<Vec<_>>();
    let mut sum = 0;
    for i in 0..data.len() {
        if data[i] == data[(i + 1) % data.len()] {
            sum += data[i]
        }
    }

    sum
}

pub fn hard(data: &str) -> i32 {
    let data = data.chars().map(|c| c.to_string().parse::<i32>().unwrap()).collect::<Vec<_>>();
    let mut sum = 0;
    for i in 0..data.len() {
        if data[i] == data[(i + data.len() / 2) % data.len()] {
            sum += data[i]
        }
    }

    sum
}


pub fn main() {
    let res = fs::read_to_string("input/1.txt").unwrap();
    println!("{}", easy(&res));
    println!("{}", hard(&res));
}