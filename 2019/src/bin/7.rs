use std::fs;
use std::thread;
use std::thread::JoinHandle;
use itertools::Itertools;
use pipe_channel::*;



type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

use advent_of_code_2019::intcode::run_intcode;


#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy_1() {
      let input = String::from("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0");
      let input = parse_input(input).unwrap();
      assert_eq!(easy(&input), 43210);
    }

    #[test]
    pub fn test_easy_2() {
      let input = String::from("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0");
      let input = parse_input(input).unwrap();
      assert_eq!(easy(&input), 54321);
    }

    #[test]
    pub fn test_easy_3() {
      let input = String::from("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0");
      let input = parse_input(input).unwrap();
      assert_eq!(easy(&input), 65210);
    }

    #[test]
    pub fn test_hard_1() {
      let input = String::from("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5");
      let input = parse_input(input).unwrap();
      assert_eq!(hard(&input), 139629729);
    }
    
    #[test]
    pub fn test_hard_2() {
      let input = String::from("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10");
      let input = parse_input(input).unwrap();
      assert_eq!(hard(&input), 18216);
    }
}

fn parse_input(data: String) -> Result<Vec<i64>> {
    let res = data
        .split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>();
    Ok(res)
}

fn easy(code: &Vec<i64>) -> i64 {
    fn simulate(permutation: &Vec<i64>, code: &Vec<i64>) -> i64 {
        let mut inputs = Vec::<Box<dyn FnMut() -> i64>>::new();
        let mut outputs = Vec::<Box<dyn FnMut(i64)>>::new();

        for _ in permutation {
            let (mut send, mut receive) = channel::<i64>();
            inputs.push(Box::new(move || {
                receive.recv().expect("Invalid value sent over channel")
            }));
            outputs.push(Box::new(move |val| {
                send.send(val).expect("Unable to send value over channel")
            }));
        }

        for (i, &value) in permutation.iter().enumerate() {
            outputs[i](value);
        }

        outputs[0](0);

        let l = permutation.len();
        for (i, _) in permutation.iter().enumerate() {
            run_intcode(code.clone(), || { inputs[i]() }, |val| outputs[(i+1)%l](val));
        }

        inputs[0]()
    }

    (0..5).permutations(5)
        .map(|perm| simulate(&perm, code))
        .fold(0, |acc,val| acc.max(val))
}

fn hard(code: &Vec<i64>) -> i64 {
    fn simulate_hard(permutation: &Vec<i64>, code: &Vec<i64>) -> i64 {
        let (mut send_result, mut receive_result) = channel::<i64>();
        let (mut send0, mut receive0) = channel::<i64>();
        let mut output0 = move |val| {
            send_result.send(val).unwrap_or_default();
            send0.send(val).unwrap_or_default();
        };
        let input0 = move || { receive0.recv().unwrap_or_default() };

        let (mut send, mut receive) = channel::<i64>();
        let input1 = move || { receive.recv().unwrap() };
        let mut output1 = move |val| { send.send(val).unwrap_or_default(); };

        let (mut send, mut receive) = channel::<i64>();
        let input2 = move || { receive.recv().unwrap() };
        let mut output2 = move |val| { send.send(val).unwrap_or_default(); };

        let (mut send, mut receive) = channel::<i64>();
        let input3 = move || { receive.recv().unwrap() };
        let mut output3 = move |val| { send.send(val).unwrap_or_default(); };

        let (mut send, mut receive) = channel::<i64>();
        let input4 = move || { receive.recv().unwrap() };
        let mut output4 = move |val| { send.send(val).unwrap_or_default(); };

        output0(permutation[0]);
        output1(permutation[1]);
        output2(permutation[2]);
        output3(permutation[3]);
        output4(permutation[4]);

        output0(0);

        let c0 = code.clone();
        let c1 = code.clone();
        let c2 = code.clone();
        let c3 = code.clone();
        let c4 = code.clone();

        let mut handles = Vec::<JoinHandle<()>>::new();
        handles.push(thread::spawn(|| { run_intcode(c0, input0, output1); }));
        handles.push(thread::spawn(|| { run_intcode(c1, input1, output2); }));
        handles.push(thread::spawn(|| { run_intcode(c2, input2, output3); }));
        handles.push(thread::spawn(|| { run_intcode(c3, input3, output4); }));
        handles.push(thread::spawn(|| { run_intcode(c4, input4, output0); }));

        for thread in handles {
            thread.join().expect("Unable to join thread");
        }

        let data = receive_result.iter().collect::<Vec<_>>();
        // println!("{:?}", data);
        data[data.len() - 1]
    }

    (5..10).permutations(5)
        .map(|perm| simulate_hard(&perm, code))
        .fold(0, |acc,val| acc.max(val))
}

fn main() {
    let code = fs::read_to_string("input/7.txt").expect("Unable to read input file");
    let code = parse_input(code).unwrap();
    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}
