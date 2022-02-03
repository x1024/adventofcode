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

pub fn easy(input: &Vec<i32>) -> i32 {
    let mut input = input.clone();
    let mut i: i32 = 0;
    let mut steps = 0;
    loop {
        // println!("{} {} {}", i, input.len(), steps);
        if i < 0 || i >= input.len() as i32 {
            return steps
        }
        let tmp = input[i as usize];
        input[i as usize] += 1;
        i += tmp;
        steps += 1;
    }
}

pub fn hard(input: &Vec<i32>) -> i32 {
    let mut input = input.clone();
    let mut i: i32 = 0;
    let mut steps = 0;
    loop {
        // println!("{} {} {}", i, input.len(), steps);
        if i < 0 || i >= input.len() as i32 {
            return steps
        }
        let tmp = input[i as usize];
        if tmp >= 3 {
            input[i as usize] -= 1;
        } else {
            input[i as usize] += 1;
        }
        i += tmp;
        steps += 1;
    }
}


fn parse_input(input: &str) -> Vec<i32> {
    input.split("\n").map(|row| row.trim().parse::<i32>().unwrap()).collect::<Vec<_>>()
}

pub fn main() {
    let input = fs::read_to_string("input/5.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}