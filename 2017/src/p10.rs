use std::fs;

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_easy() {
        let data = vec!(3, 4, 1, 5);
        assert_eq!(knot_hash(&data, 5), vec!(3, 4, 2, 1, 0));
    }

    #[test]
    fn test_dense_hash() {
        let data = vec!(65,27,9,1,4,3,40,50,91,7,6,0,2,5,68,22);
        assert_eq!(dense_hash(&data), "40");
    }

    #[test]
    fn test_hard() {
        assert_eq!(knot_hash_str(""), "a2582a3a0e66e6e86e3812dcb672a272");
        assert_eq!(knot_hash_str("AoC 2017"), "33efeb34ea91902bb2f59c9920caa6cd");
        assert_eq!(knot_hash_str("1,2,3"), "3efbe78a8d82f29979031a4aa0b16a9d");
        assert_eq!(knot_hash_str("1,2,4"), "63960835bcdc130f0b66d7ff4f6a5a8e");
    }
}

pub fn dense_hash(data: &Vec<i32>) -> String {
    data.chunks(16)
        .map(|c| c.iter().fold(0, |a, b| a ^ b))
        .map(|c| format!("{:02x}", c))
        .collect::<String>()
}

pub fn knot_hash(data: &Vec<i32>, l: i32) -> Vec<i32> {
    let mut numbers = (0..l).collect::<Vec<i32>>();
    let mut cur = 0;
    let mut skip = 0;
    for i in data {
        // Reverse
        let mut j = 0;
        loop {
            let a = ((cur + j) % l) as usize;
            let b = ((cur + i - 1 - j) % l) as usize;
            if j >= i - 1 - j { break; }
            let tmp = numbers[a];
            numbers[a] = numbers[b];
            numbers[b] = tmp;
            j += 1;
        }

        cur += i + skip;
        skip += 1;
    }

    numbers
}

pub fn knot_hash_str(data: &str) -> String {
    let mut data = data.chars().map(|c| c as i32).collect::<Vec<_>>();
    data.extend([17, 31, 73, 47, 23]);
    // duplicate it 64 times
    for _ in 0..6 { data.extend(data.clone()); }
    dense_hash(&knot_hash(&data, 256))
}

fn parse_input(data: &str) -> Vec<i32> {
    data.split(",").map(|s| s.trim().parse::<i32>().unwrap()).collect::<Vec<_>>()
}

pub fn hard(data: &str) -> String {
    knot_hash_str(data)
}


pub fn easy(data: &Vec<i32>) -> i32 {
    let result = knot_hash(data, 256);
    result[0] * result[1]
}

pub fn main() {
    let input = fs::read_to_string("input/10.txt").unwrap();
    println!("{}", easy(&parse_input(&input)));
    println!("{}", hard(&input));
}
