use std::collections::HashSet;
use queues::IsQueue;
use std::thread::JoinHandle;
use queues::Queue;
use advent_of_code_2019::intcode::run_intcode;
use advent_of_code_2019::intcode::INPUT_SHORT_CIRCUIT;
use std::fs;
use std::thread;
use std::sync::{Arc, Mutex};

fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

trait P23 {
    fn new(num_workers: usize) -> Self;
    fn read(&mut self, target: usize) -> i64;
    fn write(&mut self, target: usize, data: i64);
    fn result(&self) -> i64;
}

struct P23Easy {
    queues: Vec<Queue::<i64>>,
    buffers: Vec<Vec::<i64>>,
    special: (i64, i64),
    done: bool,
}

impl P23 for P23Easy {
    fn new(num_workers: usize) -> P23Easy {
        let mut queues = Vec::new();
        let mut buffers = Vec::new();
        for i in 0..num_workers {
            let mut q = Queue::new();
            q.add(i as i64).unwrap();
            queues.push(q);
            buffers.push(Vec::new());
        };
        let special = (0, 0);

        P23Easy {
            queues,
            buffers,
            special,
            done: false,
        }
    }

    fn read(&mut self, target: usize) -> i64 {
        if self.done {
            INPUT_SHORT_CIRCUIT
        } else {
            self.queues[target].remove().unwrap_or(-1)
        }
    }

    fn write(&mut self, target: usize, data: i64) {
        // println!("Output {} {}", target, data);
        let buffer = &mut self.buffers[target];
        buffer.push(data);
        if buffer.len() < 3 { return; }
    
        let target = buffer[0];
        let x = buffer[1];
        let y = buffer[2];

        if target == 255 {
            self.special = (x, y);
            self.done = true;
            return
        }

        let q = &mut self.queues[target as usize];
        q.add(x).unwrap();
        q.add(y).unwrap();
        buffer.clear();
    }

    fn result(&self) -> i64 {
        self.special.1
    }
}

struct P23Hard {
    queues: Vec<Queue::<i64>>,
    is_idling: Vec<bool>,
    buffers: Vec<Vec::<i64>>,
    special: (i64, i64),
    nat_history: HashSet::<i64>,
    done: bool,
}

impl P23Hard {
    fn total_queue_size(&self) -> usize {
        self.queues.iter().map(|q| q.size()).sum::<usize>()
    }

    fn total_idle_count(&self) -> usize {
        self.is_idling.iter().map(|val| if *val { 1 } else { 0 } ).sum::<usize>()
    }

    fn is_idle(&self) -> bool {
        self.total_queue_size() == 0 && self.total_idle_count() == self.queues.len()
    }

    fn send_nat_packet(&mut self) {
        let (x, y) = self.special;
        // println!("Sending NAT packet: {} {}", x, y);
        let q = &mut self.queues[0];
        if !self.nat_history.insert(y) {
            self.done = true;
        } else {
            q.add(x).unwrap();
            q.add(y).unwrap();
        }
    }
}


impl P23 for P23Hard {
    fn new(num_workers: usize) -> P23Hard {
        let mut queues = Vec::new();
        let mut buffers = Vec::new();
        let mut is_idling = Vec::new();
        is_idling.resize(num_workers, false);

        for i in 0..num_workers {
            let mut q = Queue::new();
            q.add(i as i64).unwrap();
            queues.push(q);
            buffers.push(Vec::new());
        };

        P23Hard {
            queues,
            buffers,
            is_idling,
            special: (0, 0),
            nat_history: HashSet::new(),
            done: false,
        }
    }

    fn read(&mut self, target: usize) -> i64 {
        if self.done {
            return INPUT_SHORT_CIRCUIT;
        }

        let queue = &mut self.queues[target];
        self.is_idling[target] = queue.size() == 0;
        match queue.remove() {
            Ok(value) => {
                // println!("Value: {} {}", target, value);
                value
            },
            _ => {
                if self.is_idle() {
                    self.send_nat_packet();
                }
                -1
            },
        }
    }

    fn write(&mut self, source: usize, data: i64) {
        // println!("Output {} {}", source, data);
        let buffer = &mut self.buffers[source];
        buffer.push(data);
        if buffer.len() < 3 { return; }

        self.is_idling[source] = false;
        let message_target = buffer[0];
        let x = buffer[1];
        let y = buffer[2];

        if message_target == 255 {
            self.special = (x, y);
            buffer.clear();
            // println!("\t\tWriting special {} {}", x, y);
            return
        }

        // println!("Writing from {} to {} values {} {}", source, message_target, x, y);
        let q = &mut self.queues[message_target as usize];
        q.add(x).unwrap();
        q.add(y).unwrap();
        buffer.clear();
    }

    fn result(&self) -> i64 {
        self.special.1
    }
}


fn run<T: 'static +  P23 + std::marker::Send>(code: &Vec<i64>) -> i64 {
    let size = 50;
    let app = T::new(size);

    let mutex = Arc::new(Mutex::new(app));

    let mut handles = Vec::<JoinHandle<()>>::new();
    for i in 0..size {
        let c = code.clone();
        let m = mutex.clone();
        handles.push(thread::spawn(move || {
            run_intcode(&c, || {
                let mut a = m.lock().unwrap();
                a.read(i)
            }, |val| {
                let mut a = m.lock().unwrap();
                a.write(i, val);
            });
        }));
    }

    for thread in handles {
        thread.join().expect("Unable to join thread");
    }

    let app = mutex.lock().unwrap();
    app.result()
}

fn easy(code: &Vec<i64>) -> i64 {
    run::<P23Easy>(code)
}

fn hard(code: &Vec<i64>) -> i64 {
    run::<P23Hard>(code)
}


fn main() {
    let code = fs::read_to_string("input/23.txt").expect("Unable to read input file");
    let code = parse_input(code);

    println!("{}", easy(&code));
    println!("{}", hard(&code));
    ()
}