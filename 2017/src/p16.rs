use std::collections::HashMap;
use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        let data = "s1,x3/4,pe/b";
        assert_eq!(easy(5, data), "baedc");
    }

    #[test]
    fn test_hard() {
    }
}

enum Move {
    Spin(usize),
    Exchange(usize, usize),
    Partner(String, String),
}

fn easy(num_dancers: usize, dance: &str) -> String {
    let dance = parse_input(dance);
    let mut dancers = (0..num_dancers)
        .map(|i| (i as u8 + 'a' as u8) as char)
        .collect::<Vec<_>>();

    solve(&mut dancers, &dance);
    dancers.iter().collect::<String>()
}

fn solve(dancers: &mut Vec<char>, dance: &Vec<Move>) {
    for m in dance {
        match m {
            Move::Spin (x) => { dancers.rotate_right(*x); },
            Move::Exchange (a, b) => {
                let tmp = dancers[*a];
                dancers[*a] = dancers[*b];
                dancers[*b] = tmp;
            },
            Move::Partner (a, b) => {
                let mut ia = 0;
                let mut ib = 0;
                let a = a.chars().next().unwrap();
                let b = b.chars().next().unwrap();;
                for (i, d) in dancers.iter().enumerate() {
                    if *d == a { ia = i; }
                    if *d == b { ib = i; }
                }
                let tmp = dancers[ia];
                dancers[ia] = dancers[ib];
                dancers[ib] = tmp;
            }
        }
    }
}

fn hard(mut num_steps: i64, num_dancers: usize, dance: &str) -> String {
    let dance = parse_input(dance);
    let mut dancers = (0..num_dancers)
        .map(|i| (i as u8 + 'a' as u8) as char)
        .collect::<Vec<_>>();

    let mut seen = HashMap::new();

    let mut step = -1_i64;
    while num_steps > 0 {
        solve(&mut dancers, &dance);
        step += 1;
        let state = dancers.iter().collect::<String>();
        if let Some(loop_start) = seen.insert(state, step) {
            if loop_start == 0 {
                num_steps %= step - loop_start;
            }
        }

        num_steps -= 1;
    }

    dancers.iter().collect::<String>()
}

fn parse_input(data: &str) -> Vec<Move> {
    data.split(',').map(|m| {
        let chars = m.chars().collect::<Vec<_>>();
        let move_type = chars[0];
        let move_def = &m[1..];
        
        match move_type {
            's' => Move::Spin(move_def.parse::<usize>().unwrap()),
            'x' => {
                let items = move_def.split("/")
                    .map(|i| i.parse::<usize>().unwrap())
                    .collect::<Vec<_>>();
                Move::Exchange(items[0], items[1])
            },
            'p' => {
                let items = move_def.split("/")
                    .map(|i| i.to_string())
                    .collect::<Vec<_>>();
                Move::Partner(items[0].to_string(), items[1].to_string())
            },
            _ => panic!("Invalid Dance Move"),
        }
    })
    .collect()
}

pub fn main() {
    let input = fs::read_to_string("input/16.txt").unwrap();
    println!("{}", easy(16, &input));
    println!("{}", hard(1 * 1000 * 1000 * 1000, 16, &input));
}
