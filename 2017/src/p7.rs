use std::collections::HashSet;
use std::collections::HashMap;
use std::fs;
use trees::{Tree,Node};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_easy() {
        let input = "pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)";
        let input = parse_input(input);
        assert_eq!(easy(&input), "tknk");
    }

    #[test]
    fn test_hard() {
        let input = "pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)";
        let input = parse_input(input);
        assert_eq!(hard(&input), 60);
    }
}

type TreeDef = (String, i32, Vec<String>);
type T = (String, i32);

fn parse_row(row: &str) -> TreeDef {
    let parts = row.split(" -> ").collect::<Vec<_>>();
    let name_weight = parts[0].split(" ").collect::<Vec<_>>();
    let name = String::from(name_weight[0]);
    let weight = name_weight[1].replace("(", "").replace(")", "").parse::<i32>().unwrap();
    let mut children :Vec<_> = Vec::new();
    if parts.len() == 2 {
        children = parts[1].split(", ").map(|c| String::from(c)).collect::<Vec<_>>();
    }

    return (name, weight, children)
}

fn parse_input(data: &str) -> Vec<TreeDef> {
    data.split("\n").map(|row| parse_row(row)).collect::<Vec<_>>()
}

pub fn easy(data: &Vec<TreeDef>) -> String {
    let mut names = HashSet::<&String>::new();
    for node in data { names.insert(&node.0); }
    for (_, _, children) in data {
        for child in children { names.remove(child); }
    }

    names.iter().collect::<Vec<_>>()[0].to_string()
}

pub fn build_tree(node: &TreeDef, map: &HashMap<&String, &TreeDef>) -> Tree<(String, i32)> {
    let mut t = Tree::new((node.0.clone(), node.1));
    for c in &node.2 {
        let child = map.get(&c).unwrap();
        t.push_back(build_tree(child, map));
    }

    t
}

pub fn weight(node: &Node<T>) -> i32 {
    node.data().1 + node.iter().map(|n| weight(n)).sum::<i32>()
}

pub fn find_unbalanced(node: &Node<T>) -> Option<i32> {
    let weights = node.iter().map(|n| weight(n)).collect::<Vec<_>>();
    let mut values = Vec::new();
    for weight in weights {
        if values.len() == 0 {
            values.push(weight);
        } else if values[values.len() - 1] != weight {
            values.pop();
        } else {
            values.push(weight);
        }
    }
    let expected = values[0];

    for child in node.iter() {
        let weight = weight(child);
        if weight != expected {
            let result = if let Some(val) = find_unbalanced(child) {
                val
            } else {
                let difference = weight - expected;
                // println!("{} {} {}", weight, expected, difference);
                child.data().1 - difference
            };
            return Some(result)
        }
    }
    
    None
}

pub fn hard(data: &Vec<TreeDef>) -> i32 {
    let mut map = HashMap::<&String, &TreeDef>::new();
    for node in data { map.insert(&node.0, node); }
    let root = easy(data);
    let root = map.get(&root).unwrap();
    let tree = build_tree(root, &map);
    find_unbalanced(&tree).unwrap()
}

pub fn main() {
    let input = fs::read_to_string("input/7.txt").unwrap();
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
}
