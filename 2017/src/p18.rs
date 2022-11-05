use queues::{Queue, IsQueue};
use core::time::Duration;
use std::collections::HashMap;
use std::thread::JoinHandle;
use std::{thread, fs};
use std::sync::{Arc, Mutex};

const INVALID_VALUE: i64 = -9999999999;

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

    #[test]
    fn test_hard() {
        let code = "snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d";
        assert_eq!(hard(&code), 3);
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
    Mul(Value, Value),
    Mod(Value, Value),
    RCV(Value),
    JGZ(Value, Value),
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
        "mul" => Opcode::Mul(parse_value(data[1]), parse_value(data[2])),
        "mod" => Opcode::Mod(parse_value(data[1]), parse_value(data[2])),
        "rcv" => Opcode::RCV(parse_value(data[1])),
        "jgz" => Opcode::JGZ(parse_value(data[1]),  parse_value(data[2])),
        _ => panic!("Invalid opcode")
    }
}

fn parse_input(data: &str) -> Vec<Opcode> {
    data.split("\n").map(|row|
        parse_row(&row.split(" ").collect::<Vec<_>>())
    ).collect::<Vec<_>>()
}

pub fn eval_easy(data: &Vec<Opcode>) -> i64 {
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

    loop {
        if index < 0 || index >= data.len() as i64 {
            return -1
        }
        let opcode = &data[index as usize];
        println!("{} {:?} {:?}", index, opcode, registers);
        match opcode {
            Opcode::Snd(x) => { last_sound = get_value(x, &registers); }
            Opcode::Set(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers)); },
            Opcode::Add(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers) + get_value(&x, &registers)); },
            Opcode::Mul(x, y) => { registers.insert(get_string(&x), get_value(&y, &registers) * get_value(&x, &registers)); },
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
        };

        index += 1;
    }
}

/*
pub fn run_intcode<'a, I: 'a, O: 'a>(code: &Vec<i64>, input: I, output: O) -> Vec<i64>
    where I: FnMut() -> i64, O: FnMut(i64) {

  let mut code = code.clone();
  code.resize(1000000, 0);

  let mut c = IntCode::new(code.clone(), Box::new(input), Box::new(output));

  loop {
    if let Opcode::Exit = c.run_step() {
      break
    }
  }
}
*/

pub fn eval_hard<'a, I: 'a, O: 'a>(data: &Vec<Opcode>, program_index: usize, input: &mut I, output: &mut O)
    where I: FnMut() -> i64, O: FnMut(i64) {
    let mut index: i64 = 0;
    let mut r: HashMap<String, i64> = HashMap::new(); // "registers"
    r.insert("p".to_string(), program_index as i64);

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
            return
        }
        let opcode = &data[index as usize];
        // println!("{} {:?} {:?}", index, opcode, r);
        match opcode {
            Opcode::Snd(x) => { output(get_value(x, &r)); }
            Opcode::Set(x, y) => { r.insert(get_string(&x), get_value(&y, &r)); },
            Opcode::Add(x, y) => { r.insert(get_string(&x), get_value(&y, &r) + get_value(&x, &r)); },
            Opcode::Mul(x, y) => { r.insert(get_string(&x), get_value(&y, &r) * get_value(&x, &r)); },
            Opcode::Mod(x, y) => { r.insert(get_string(&x), get_value(&x, &r) % get_value(&y, &r)); },
            Opcode::RCV(x) => {
                let value = input();
                if value == INVALID_VALUE {
                    return
                }
                r.insert(get_string(&x), value);
            }
            Opcode::JGZ(x, y) => {
                if get_value(&x, &r) > 0 {
                    index += get_value(&y, &r) - 1;
                }
            },
        };

        index += 1;
    }
}

pub fn easy(data: &Vec<Opcode>) -> i64 {
    eval_easy(data)
}

fn run (input: &str) -> i64 {
    let size = 2;
    let mut all_queues = Vec::new();
    let mut num_values_sent = Vec::new();
    num_values_sent.resize(size, 0);
    for _ in 0..size {
        all_queues.push(Queue::<i64>::new());
    }

    let mutex_queue = Arc::new(Mutex::new(all_queues));
    let mutex_counter = Arc::new(Mutex::new(num_values_sent));

    let mut handles = Vec::<JoinHandle<()>>::new();

    for i in 0..size {
        let m_q = mutex_queue.clone();
        let m_c = mutex_counter.clone();
        let data = parse_input(&input);
        let program_index = if i == 0 { 1 } else { 0 };
        handles.push(thread::spawn(move || {
            eval_hard(&data, program_index, &mut || {
                let mut value = 0;
                let mut found = false;
                // ATTN: This is literally a race condition.
                // A value that's too low will break the program
                // AND it depends on how fast your computer is
                let mut attempts = 10;
                while !found && attempts > 0 {
                    attempts -= 1;
                    {
                        let mut a = m_q.lock().unwrap();
                        let q = &mut a[i];
                        value = match q.remove() {
                            Ok(n) => {
                                found = true;
                                // println!("\tP{} reads {}", i, n); 
                                n
                            }
                            Err(_) => {
                                found = false;
                                INVALID_VALUE
                            }
                        };
                    }

                    // println!("Queue {} empty, sleeping", i);
                    if !found {
                        thread::sleep(Duration::from_millis(1));
                    }
                };
                value
            }, &mut |val| {
                let mut a = m_q.lock().unwrap();
                let other_queue = if i == 0 { 1 } else { 0 };
                let q = &mut a[other_queue];
                q.add(val).unwrap();
                let mut num_values_sent = m_c.lock().unwrap();
                num_values_sent[i] += 1;
                // println!("P{} sends: {}, {}", i, val, &num_values_sent[i]); 
            });
        }));
    }

    for thread in handles {
        thread.join().expect("Unable to join thread");
    }

    let num_values_sent = mutex_counter.lock().unwrap();
    num_values_sent[0]
}

pub fn hard(input: &str) -> i64 {
    run(input)
}

pub fn main() {
    let input = fs::read_to_string("input/18.txt").unwrap();
    if false {
        let input = parse_input(&input);
        println!("{:?}", easy(&input));
    }
    println!("{:?}", hard(&input));
}
