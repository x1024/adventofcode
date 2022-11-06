use std::collections::HashMap;
use std::{fs, io};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        let code = "set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2";
        let input = parse_input(code);
        assert_eq!(easy(&input), 4);
    }
}

/*
snd X plays a sound with a frequency equal to the value of X.
set X Y sets register X to the value of Y.
add X Y increases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
*/
#[derive(Debug)]
pub enum Opcode {
    Snd(Value),
    Set(Value, Value),
    Add(Value, Value),
    Sub(Value, Value),
    Mul(Value, Value),
    Mod(Value, Value),
    NOP(),
    RCV(Value),
    JGZ(Value, Value),
    JNZ(Value, Value),
}

#[derive(Debug)]
pub enum Value {
    Literal(i64),
    Register(String),
}

fn parse_value(value: &str) -> Value {
    match value.parse::<i64>() {
        Ok(n) => Value::Literal(n),
        Err(_) => Value::Register(value.to_string())
    }
}

fn parse_row(data: &Vec<&str>) -> Opcode {
    // println!("{:?}", data);
    match data[0] {
        "snd" => Opcode::Snd(parse_value(data[1])),
        "set" => Opcode::Set(parse_value(data[1]), parse_value(data[2])),
        "add" => Opcode::Add(parse_value(data[1]), parse_value(data[2])),
        "sub" => Opcode::Sub(parse_value(data[1]), parse_value(data[2])),
        "mul" => Opcode::Mul(parse_value(data[1]), parse_value(data[2])),
        "mod" => Opcode::Mod(parse_value(data[1]), parse_value(data[2])),
        "nop" => Opcode::NOP(),
        "rcv" => Opcode::RCV(parse_value(data[1])),
        "jgz" => Opcode::JGZ(parse_value(data[1]),  parse_value(data[2])),
        "jnz" => Opcode::JNZ(parse_value(data[1]),  parse_value(data[2])),
        _ => panic!("Invalid opcode")
    }
}

fn parse_input(data: &str) -> Vec<Opcode> {
    data.split("\n").map(|row|
        parse_row(&row.split(" ").collect::<Vec<_>>())
    ).collect::<Vec<_>>()
}

pub fn easy(data: &Vec<Opcode>) -> i64 {
    let mut index: i64 = 0;
    let mut last_sound = 0;
    let mut registers: HashMap<String, i64>= HashMap::new();

    let get_value = |v: &Value, registers: &HashMap<String, i64>|
        match v {
            Value::Literal(n) => *n,
            Value::Register(n) => *registers.get(n).unwrap_or(&0),
        };
    
    let get_string = |v: &Value| -> String {
        match v {
            Value::Literal(n) => panic!("Invalid register: {}", n),
            Value::Register(n) => n.to_string(),
        }
    };

    let mut mul_count = 0;

    loop {
        if index < 0 || index >= data.len() as i64 {
            return mul_count
        }
        let opcode = &data[index as usize];
        // println!("{} {:?}", index, registers);
        match opcode {
            Opcode::Mul(_a, _b) => {
                mul_count += 1;
            },
            _ => {}
        }
        match opcode {
            Opcode::Snd(x) => { last_sound = get_value(x, &registers); }
            Opcode::Set(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers)); },
            Opcode::Add(x, y) => { registers.insert(get_string(&x), get_value(&x, &registers) + get_value(&y, &registers)); },
            Opcode::Sub(x, y) => { registers.insert(get_string(&x), get_value(&x, &registers) - get_value(&y, &registers)); },
            Opcode::Mul(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers) * get_value(&x, &registers)); },
            Opcode::NOP() => {},
            Opcode::Mod(x, y) => { registers.insert(get_string(&x), get_value(&x, &registers) % get_value(&y, &registers)); },
            Opcode::RCV(x) => {
                if get_value(&x, &registers) != 0 {
                    println!("Sound: {}", last_sound);
                    return last_sound
                }
            }
            Opcode::JGZ(x, y) => {
                if get_value(&x, &registers) > 0 {
                    index += get_value(&y, &registers) - 1;
                }
            },
            Opcode::JNZ(x, y) => {
                if get_value(&x, &registers) != 0 {
                    index += get_value(&y, &registers) - 1;
                }
            },
        };

        index += 1;
    }
}

pub fn hard(data: &Vec<Opcode>) -> i64 {
    let mut index: i64 = 0;
    let mut last_sound = 0;
    let mut registers: HashMap<String, i64>= HashMap::new();
    registers.insert("a".to_string(), 1);

    let get_value = |v: &Value, registers: &HashMap<String, i64>|
        match v {
            Value::Literal(n) => *n,
            Value::Register(n) => *registers.get(n).unwrap_or(&0),
        };
    
    let get_string = |v: &Value| -> String {
        match v {
            Value::Literal(n) => panic!("Invalid register: {}", n),
            Value::Register(n) => n.to_string(),
        }
    };

    loop {
        if index < 0 || index >= data.len() as i64 {
            println!("{} {:?}", index, registers);
            return get_value(&Value::Register("h".to_string()), &registers)
        }

        let opcode = &data[index as usize];

        match opcode {
            Opcode::JNZ(_a, _b) => {
                println!("{} {:?}", index + 1, registers);
                let mut search_keyword = String::new();
                io::stdin().read_line(&mut search_keyword).unwrap();
            },
            _ => {
            }
        }

        match opcode {
            Opcode::Snd(x) => { last_sound = get_value(x, &registers); }
            Opcode::Set(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers)); },
            Opcode::Add(x, y) => { registers.insert(get_string(&x), get_value(&x, &registers) + get_value(&y, &registers)); },
            Opcode::Sub(x, y) => { registers.insert(get_string(&x), get_value(&x, &registers) - get_value(&y, &registers)); },
            Opcode::Mul(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers) * get_value(&x, &registers)); },
            Opcode::Mod(x, y) => { registers.insert(get_string(&x), get_value(&x, &registers) % get_value(&y, &registers)); },
            Opcode::NOP() => {},
            Opcode::RCV(x) => {
                if get_value(&x, &registers) != 0 {
                    println!("Sound: {}", last_sound);
                    return last_sound
                }
            }
            Opcode::JGZ(x, y) => {
                if get_value(&x, &registers) > 0 {
                    index += get_value(&y, &registers) - 1;
                }
            },
            Opcode::JNZ(x, y) => {
                if get_value(&x, &registers) != 0 {
                    index += get_value(&y, &registers) - 1;
                }
            },
        };

        index += 1;
    }
}

pub fn main() {
    let input = fs::read_to_string("input/23.txt").unwrap();
    let input = parse_input(&input);
    println!("{:?}", easy(&input));

    // We are actually looking for the number of prime numbers
    // in the range [b:c:17], inclusive on both ends.
    // (Figure out B and C by reading the input)
    let mut b = 100000 + 93 * 100;
    let c = b + 17000;
    let mut h = 0;
    while b <= c {
        if !is_prime(b) {
            h += 1;
        }
        b += 17;
    }
    println!("{}", h);
}

fn is_prime(n: u32) -> bool {
    if n <= 1 {
        return false;
    }
    for a in 2..n {
        if n % a == 0 {
            return false; // if it is not the last statement you need to use `return`
        }
    }
    true // last value to return
}
