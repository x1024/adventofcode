use num_integer::Integer;
use std::fs;
use std::collections::HashMap;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    fn test_easy_1() {
        let data = "10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL";
        assert_eq!(easy(data), 31);
    }

    #[test]
    fn test_easy_2() {
        let data = "9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL";
        assert_eq!(easy(data), 165);
    }

    #[test]
    fn test_easy_3() {
        let data = "157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT";
        assert_eq!(easy(data), 13312);
    }

    #[test]
    fn test_easy_4() {
        let data = "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF";
        assert_eq!(easy(data), 180697);
    }

    #[test]
    fn test_easy_5() {
        let data = "171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX";
        assert_eq!(easy(data), 2210736);
    }

    #[test]
    fn test_hard_3() {
        let data = "157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT";
        assert_eq!(hard(data), 82892753);
    }

    #[test]
    fn test_hard_4() {
        let data = "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF";
        assert_eq!(hard(data), 5586022);
    }
    #[test]
    fn test_hard_5() {
        let data = "171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX";
        assert_eq!(hard(data), 460664);
    }
}

#[derive(Debug)]
struct Ingredient(i64, String);

impl Clone for Ingredient {
    fn clone(&self) -> Self {
        Ingredient ( self.0, self.1.clone())
    }
}

type RecipeBook = HashMap::<String, (i64, Vec<Ingredient>)>;

fn parse_segment(segment: &str) -> Ingredient {
    let segment = segment.trim().split(" ").collect::<Vec<_>>();
    let count = segment[0].parse::<i64>().unwrap();
    Ingredient (count, segment[1].to_string())
}

fn parse_line(line: &str) -> Vec<Vec<Ingredient>> {
    line.split("=>")
        .map(|segment| segment.split(", ")
                              .map(|s| parse_segment(s))
                              .collect::<Vec<_>>())
        .collect::<Vec<_>>()
}

fn parse_input(data: &str) -> RecipeBook {
    let mut recipes = RecipeBook::new();
    for recipe in data.split("\n").map(parse_line) {
        let ingredients = &recipe[0];
        let result = &recipe[1][0];
        let name = &result.1;
        let quantity = result.0;
        recipes.insert(name.to_string(), (quantity, ingredients.clone()));
    }
    recipes
}

fn process(recipes: &RecipeBook, quantity: i64, start: &String, end: &String) -> i64 {
    let mut contents = HashMap::<String, i64>::new();
    contents.insert(start.to_string(), quantity);

    loop {
        let mut to_add = Vec::<(String, i64)>::new();
        let mut to_remove: String = "".to_string();
        let mut to_make: i64 = 0;
        let mut found_recipe = false;

        for (name, &quantity) in &contents {
            if name.eq(end) { continue }
            if quantity < 0 { continue }

            let (result_quantity, ingredients) = &recipes[name];
            to_make = quantity.div_ceil(&result_quantity);
            found_recipe = true;
            for ingredient in ingredients {
                let new_name = ingredient.1.clone();
                let new_qty = contents.get(&new_name).unwrap_or(&0) + to_make * ingredient.0;
                to_add.push((new_name, new_qty));
            }

            to_remove = name.clone();
            break
        }

        if !found_recipe { break }

        let items_made = recipes[&to_remove].0 * to_make;
        let items_needed = contents.get(&to_remove).unwrap_or(&0);
        // println!("{} {} {} | {} {}", to_remove, items_needed, items_made, to_make, recipes[&to_remove].0);
        let new_items = items_needed - items_made;
        if new_items == 0 {
            contents.remove(&to_remove);
        } else {
            contents.insert(to_remove, new_items);
        }
        
        for (name, quantity) in &to_add {
            contents.insert(name.clone(), *quantity);
        }

        // println!("{:?}", contents);

        if contents.len() == 1 && contents.contains_key(end) { break }
    }

    contents[end]
}

fn easy(code: &str) -> i64 {
    let recipe_book = parse_input(code);
    process(&recipe_book, 1, &"FUEL".to_string(), &"ORE".to_string())
}

fn hard(code: &str) -> i64 {
    let recipe_book = parse_input(code);
    let start = "FUEL".to_string();
    let end = "ORE".to_string();
    let max_used = 1000000000000 as i64;

    let mut limit = 1;
    let mut step = (2 as i64).pow(31);

    while step > 0 {
        step /= 2;

        if process(&recipe_book, limit + step, &start, &end) <= max_used {
            limit += step;
        }
    }

    limit
}

fn main() {
    let input = fs::read_to_string("input/14.txt").expect("Unable to read input file");
    println!("{}", easy(&input));
    println!("{}", hard(&input));
    ()
}
