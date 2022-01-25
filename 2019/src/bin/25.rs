use queues::IsQueue;
use queues::Queue;
use advent_of_code_2019::intcode::run_intcode;
use std::fs;
use std::io::{self, BufRead};


fn parse_input(data: String) -> Vec<i64> {
    data.split(",")
        .map(|line| line.parse::<i64>().unwrap())
        .collect::<Vec<_>>()
}

/*
Movement via north, south, east, or west.
To take an item the droid sees in the environment, use the command take <name of item>. For example, if the droid reports seeing a red ball, you can pick it up with take red ball.
To drop an item the droid is carrying, use the command drop <name of item>. For example, if the droid is carrying a green ball, you can drop it with drop green ball.
To get a list of all of the items the droid is currently carrying, use the command inv (for "inventory").

Coords:  | Room Name            | Dir | Items
----------------------------------------------
( 0,  0) | Hull Breach              | NWE |
( 0, -1) | Corridor                 | NES | infinite loop - joke item, it causes an infinite loop
( 0, -2) | Stables                  | WES | mutex
(-1, -2) | Kitchen                  | E   |
( 1, -2) | Engineering              | W   | antenna
( 1, -1) | Passages                 | NWE | cake
( 1, -2) | Gift Wrapping Center     | S   | 
( 2, -1) | Arcade                   | NW  | escape pod - joke item, you get ejected into space
( 2, -2) | Navigation               | S   | pointer
(-1,  0) | Sick Bay                 | WE  | photons - joke item, without photons it gets dark and you get eaten by a grue
(-2,  0) | Hot Chocolate Fountain   | NWE | 
(-3,  0) | Crew Quarters            | E   | coin
(-2, -1) | Warp Drive Maintenance   | S   | molten lava - joke item, you melt. Obviously
( 1,  0) | Storage                  | WE  | giant electromagnet - joke item, you get stuck on it
( 2,  0) | Observatory              | NWE | tambourine
( 2, -1) | Science Lab              | S   | 
( 3,  0) | Holodeck                 | WE  | fuel cell
( 4,  0) | Hallway                  | NW  | boulder
( 5, -1) | Pressure-Sensitive Floor | ES  | (have to be the right weight)

Full inventory:
- fuel cell
- cake
- pointer
- boulder
- mutex
- antenna
- tambourine
- coin

# Correct inventory to pass:
- coin
- cake
- antenna
- boulder


A loud, robotic voice says "Analysis complete! You may proceed." and you enter the cockpit.
Santa notices your small droid, looks puzzled for a moment, realizes what has happened, and radios your ship directly.
"Oh, hello! You should be able to get in by typing 319815680 on the keypad at the main airlock."
["south", "east", "east", "east", "east", "take tambourine", "inv", "east", "take fuel cell", "east", "take boulder", "inv", "north", "east", "south", "west", "west", "north", "south", "east", "east", "north", "inv", "drop boulder", "east", "take boulder", "east", "drop mutex", "east", "drop antenna", "east", "take mutex", "east", "take antenna", "drop tambourine", "east", "take tambourine", "inv", "drop cake", "east", "take cake", "drop fuel cell", "east", "drop cake", "east", "drop antenna", "east", "drop tambourine", "east", "drop pointer", "east", "drop coin", "east", "drop mutex", "east", "take coin", "east", "drop coin", "take pointer", "east", "take coin", "east", "take cake", "east", "take antenna", "east", "drop pointer", "east"]

*/

fn main() {
    let code = fs::read_to_string("input/25.txt").expect("Unable to read input file");
    let code = parse_input(code);
    
    let mut queue = Queue::new();
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let mut commands = Vec::new();

    // Not an optimal solution. Oh well.
    let prepared_commands = [
        "north", "north", "take mutex", "west", "east", "west", "east", "east", "take antenna",
        "take two", "west", "south", "east", "take cake", "north", "south", "west", "east",
        "east", "north", "take pointer", "south", "west", "west", "south", "west", "west", "west",
        "take coin", "east", "north", "south", "east", "east", "east", "east", "take tambourine",
        "inv", "east", "take fuel cell", "east", "take boulder", "north", "east", "south", "west",
        "west", "north", "south", "east", "east", "north", "inv", "drop boulder", "east", "take boulder",
        "east", "drop mutex", "east", "drop antenna", "east", "take mutex", "east", "take antenna",
        "drop tambourine", "east", "take tambourine", "inv", "drop cake", "east", "take cake",
        "drop fuel cell", "east", "drop cake", "east", "drop antenna", "east", "drop tambourine",
        "east", "drop pointer", "east", "drop coin", "east", "drop mutex", "east", "take coin",
        "east", "drop coin", "take pointer", "east", "take coin", "east", "take cake",
        "east", "take antenna", "east", "drop pointer", "east"
    ];

    for line in prepared_commands {
        for c in line.chars() {
            queue.add(c as i64).unwrap();
        }
        queue.add('\n' as i64).unwrap();
    }

    let input = || {
        while queue.size() == 0 {
            let mut line = lines.next().unwrap().unwrap();
            line = line.to_string();
            commands.push(line.clone());
            for c in line.chars() {
                queue.add(c as i64).unwrap();
            }
            queue.add('\n' as i64).unwrap();
        }

        queue.remove().unwrap()
    };
    let output = |val| print!("{}", (val as u8) as char);
    run_intcode(&code, input, output);

    println!("{:?}", commands);
}