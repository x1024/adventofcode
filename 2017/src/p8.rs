use std::collections::HashMap;
use std::fs;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        let data = "b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10";
        let data = parse_input(data);
        println!("{:?}", data);
        assert_eq!(easy(&data), 1);
    }

    #[test]
    fn test_hard() {
    }
}

#[derive(Debug)]
enum Operation {
    Increase, Decrease
}

#[derive(Debug, Copy, Clone)]
enum Comparison {
    Eq,
    Ne,
    Gt,
    Lt,
    Gte,
    Lte,
}

#[derive(Debug)]
struct Expression(String, Operation, i32, String, Comparison, i32);

fn eval_comparison(a: i32, cmp: Comparison, b: i32) -> bool {
    match cmp {
        Comparison::Eq => a == b,
        Comparison::Ne => a != b,
        Comparison::Gt => a > b,
        Comparison::Lt => a < b,
        Comparison::Gte => a >= b,
        Comparison::Lte => a <= b,
    }
}

fn eval_expression(expression: &Expression, registers: &mut HashMap<String, i32>) {
    let target = *registers.get(&expression.3).unwrap_or(&0);
    if !eval_comparison(target, expression.4, expression.5) { return }

    let register = registers.get(&expression.0).unwrap_or(&0);
    let value = match expression.1 {
        Operation::Increase => register + expression.2,
        Operation::Decrease => register - expression.2,
    };

    registers.insert(expression.0.clone(), value);
}

fn easy(data: &Vec<Expression>) -> i32 {
    let mut registers = HashMap::<String, i32>::new();
    for row in data {
        eval_expression(row, &mut registers);
    }

    *registers.iter().map(|(_, value)| value).max().unwrap_or(&0)
}

fn hard(data: &Vec<Expression>) -> i32 {
    let mut registers = HashMap::<String, i32>::new();
    let mut result = 0;

    for row in data {
        eval_expression(row, &mut registers);
        result = result.max(*registers.iter().map(|(_, value)| value).max().unwrap_or(&0));
    }

    result
}

fn parse_operation(value: &str) -> Operation {
    match value {
        "inc" => Operation::Increase,
        "dec" => Operation::Decrease,
        _ => panic!("Invalid operation")
    }
}

fn parse_comparison(value: &str) -> Comparison {
    match value {
        ">" => Comparison::Gt,
        ">=" => Comparison::Gte,
        "<" => Comparison::Lt,
        "<=" => Comparison::Lte,
        "==" => Comparison::Eq,
        "!=" => Comparison::Ne,
        _ => panic!("Invalid comparison")
    }
}


fn parse_expression(row: &str) -> Expression {
    let words = row.split_whitespace().collect::<Vec<_>>();
    Expression (
        words[0].to_string(), parse_operation(words[1]), words[2].parse::<i32>().unwrap(),
        words[4].to_string(), parse_comparison(words[5]), words[6].parse::<i32>().unwrap()
    )
}

fn parse_input(data: &str) -> Vec<Expression> {
    data.split("\n").map(|row| parse_expression(row)).collect::<Vec<_>>()
}

pub fn main() {
    let input = fs::read_to_string("input/8.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
