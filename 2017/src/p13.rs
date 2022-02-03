use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        let data = "0: 3
                    1: 2
                    4: 4
                    6: 4";
        let data = parse_input(data);
        assert_eq!(easy(&data), 24);
    }

    #[test]
    fn test_hard() {
        let data = "0: 3
                    1: 2
                    4: 4
                    6: 4";
        let data = parse_input(data);
        assert_eq!(hard(&data), 10);
    }
}

pub fn severity(data: &Vec<(i32, i32)>, delay: i32) -> (bool, i32) {
    let mut severity = 0;
    let mut caught = false;
    for (layer, size) in data {
        let scanner_pos = (layer + delay) % (2 * size - 2);
        // println!("{} {} {}", delay, layer, scanner_pos);
        if scanner_pos == 0 {
            severity += layer * size;
            caught = true;
        }
    }

    (caught, severity)
}

pub fn easy(data: &Vec<(i32, i32)>) -> i32 {
    severity(data, 0).1
}

pub fn hard(data: &Vec<(i32, i32)>) -> i32 {
    let mut delay = 0;
    loop {
        if !severity(data, delay).0 { return delay; }
        delay += 1;
    }
}

fn parse_input(data: &str) -> Vec<(i32, i32)> {
    data.split('\n')
        .map(|row|
            row.trim()
                .split(": ")
                .map(|c| c.parse::<i32>().unwrap())
                .collect::<Vec<_>>()
            )
        .map(|row| (row[0], row[1]))
        .collect::<Vec<_>>()
}

pub fn main() {
    let input = fs::read_to_string("input/13.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
