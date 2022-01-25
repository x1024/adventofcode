use std::fmt::Display;
use num::One;
use std::ops::Add;
use std::ops::Mul;
use std::ops::Rem;
use std::collections::HashMap;
use modinverse::modinverse;
// use mod_exp::mod_exp;
use num_bigint::*;
use std::fs;
use ring_algorithm::chinese_remainder_theorem;

#[cfg(test)]
pub mod tests {
    use super::*;

    fn run_test(shuffles: &Vec<Shuffle>, results: &Vec<i64>) {
        run_test_easy(shuffles, &results.clone());
        // run_test_hard(shuffles, &results.clone());
        run_test_hard_reverse(shuffles, &results.clone());
    }

    fn run_test_easy(shuffles: &Vec<Shuffle>, expected: &Vec<i64>) {
        let l = expected.len() as i64;
        let result = shuffle_cards(shuffles, l);
        assert_eq!(result, *expected);
    }

    /*
    fn run_test_hard(shuffles: &Vec<Shuffle>, expected: &Vec<i64>) {
        let expected = expected
            .iter().enumerate().collect::<Vec<_>>();
        let l = expected.len() as i64;
        for (start, &end) in &expected {
            let result = shuffle_card(shuffles, l, *start as i64);
            println!("{} {} {}", start, end, result);
            // assert_eq!(result, end);
        }
        assert_eq!(1, 0);
    }
    */

    fn run_test_hard_reverse(shuffles: &Vec<Shuffle>, expected: &Vec<i64>) {
        let expected = expected
            .iter().enumerate().collect::<Vec<_>>();
        let l = expected.len() as i64;
        for (start, &end) in &expected {
            let result = unshuffle_card(shuffles, l, *start as i64);
            // println!("{} {} {}", start, end, result);
            assert_eq!(result, end);
        }
    }

    #[test]
    fn test_reverse() {
        let data = "deal into new stack";
        let data = parse_input(data);
        run_test(&data, &vec!(9, 8, 7, 6, 5, 4, 3, 2, 1, 0));
    }

    #[test]
    fn test_cut() {
        let data = "cut 3";
        let data = parse_input(data);
        run_test(&data, &vec!(3, 4, 5, 6, 7, 8, 9, 0, 1, 2));
    }

    #[test]
    fn test_cut_negative() {
        let data = "cut -4";
        let data = parse_input(data);
        run_test(&data, &vec!(6, 7, 8, 9, 0, 1, 2, 3, 4, 5));
    }

    #[test]
    fn test_increment() {
        let data = "deal with increment 3";
        let data = parse_input(data);
        run_test(&data, &vec!(0, 7, 4, 1, 8, 5, 2, 9, 6, 3));
    }

    #[test]
    fn test_easy_1() {
        let data = "deal with increment 7
deal into new stack
deal into new stack";
        let data = parse_input(data);
        run_test(&data, &vec!(0, 3, 6, 9, 2, 5, 8, 1, 4, 7));
    }

    #[test]
    fn test_easy_2() {
        let data = "deal with increment 7
deal with increment 9
cut -2";
        let data = parse_input(data);
        run_test(&data, &vec!(6, 3, 0, 7, 4, 1, 8, 5, 2, 9));
    }

    #[test]
    fn test_easy_3() {
        let data = "deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1";
        let data = parse_input(data);
        run_test(&data, &vec!(9, 2, 5, 8, 1, 4, 7, 0, 3, 6));
    }

    #[test]
    fn test_easy_4() {
        let data = "cut 3
deal into new stack";
        let data = parse_input(data);
        run_test(&data, &vec!(2, 1, 0, 9, 8, 7, 6, 5, 4, 3));
    }

    #[test]
   fn test_easy_5() {
        let data = "deal with increment 7";
        let data = parse_input(data);
        run_test(&data, &vec!(0, 3, 6, 9, 2, 5, 8, 1, 4, 7));
    }
        
    #[test]
   fn test_easy_6() {
        let data = vec!(
            Shuffle::Increment(2),
            Shuffle::Increment(2),
            Shuffle::Increment(2),
            Shuffle::Increment(2),
        );
        /*
        increment 2, multiple times:
        0 1 2 3 4
        0 3 1 4 2    
        0 4 3 2 1
        0 2 4 1 3
        0 1 2 3 4
        */
        run_test(&data, &vec!(0, 1, 2, 3, 4));
    }

}

#[derive(Debug)]
enum Shuffle {
    Reverse,
    Cut(i64),
    Increment(i64)
}

type Deck = Vec<i64>;

fn parse_input(input: &str) -> Vec<Shuffle> {
    input.split("\n").map(|line| {
        let words = line.split(" ").collect::<Vec<_>>();
        // println!("{:?}", words);
        if words.len() == 2 {
            Shuffle::Cut(words[1].parse::<i64>().unwrap())
        } else if words[2] == "increment" {
            Shuffle::Increment(words[3].parse::<i64>().unwrap())
        } else {
            Shuffle::Reverse
        }
    })
    .collect::<Vec<_>>()
}

fn do_shuffle(mut deck: Deck, shuffle: &Shuffle) -> Deck {
    let l = deck.len() as i64;

    match shuffle {
        Shuffle::Increment(count) => {
            let mut new_deck = deck.clone();
            for i in 0..l {
                new_deck[((i * count) % l) as usize] = deck[i as usize];
            }
            deck = new_deck;
        },
        Shuffle::Cut(count) => deck.rotate_left(((l + count) % l) as usize),
        Shuffle::Reverse => deck.reverse(),
    };

    deck
}

fn shuffle_cards(shuffles: &Vec<Shuffle>, deck_size: i64) -> Deck {
    shuffles.iter().fold((0..deck_size).collect::<Vec<_>>(),
        |deck, shuffle| do_shuffle(deck, shuffle))
}

fn easy(shuffles: &Vec<Shuffle>, deck_size: i64, card_to_pick: i64) -> i64 {
    let cards = shuffle_cards(shuffles, deck_size);
    for i in 0..cards.len() {
        if cards[i] == card_to_pick {
            return i as i64;
        }
    }

    return - 1
}

fn reverse_shuffle_single(card: i64, deck_size: i64, shuffle: &Shuffle) -> i64 {
    match shuffle {
        Shuffle::Increment(count) => {
            let modulo = deck_size * (*count);
            let result = chinese_remainder_theorem::<i64>(
                &vec!(card, 0),
                &vec!(deck_size, *count)
            ).unwrap();

            ((result + modulo) % modulo) / count
        },
        Shuffle::Cut(count) => (card + count + deck_size) % deck_size,
        Shuffle::Reverse => deck_size - 1 - card,
    }
}

fn shuffle_card(shuffles: &Vec<Shuffle>, card: BigInt) -> BigInt {
    shuffles.iter().fold(card,
        |card, shuffle| match shuffle {
            Shuffle::Increment(count) => card * ToBigInt::to_bigint(count).unwrap(),
            Shuffle::Cut(count) => card - count,
            Shuffle::Reverse => - 1 - card,
        })
}

fn transform_card(shuffles: &Vec<Shuffle>, card: BigInt) -> (BigInt, BigInt) {
    let transformation = (1, 0);
    // Every transformation is actually linear
    // (at the end, the whole thing needs to be taken with a modulo, but that's it)
    // And also, every transformation results in an expression like (a*x + b)
    // If we just keep "a" and "b", we can simplify the calculations a lot

    let t = (ToBigInt::to_bigint(&1).unwrap(), ToBigInt::to_bigint(&0).unwrap());

    let transformation = shuffles.iter().fold(t,
        |card, shuffle| match shuffle {
            Shuffle::Increment(count) => (card.0 * count, card.1 * count),
            Shuffle::Cut(count) => (card.0, card.1 - count),
            Shuffle::Reverse => (-card.0, -1 - card.1),
        });

    transformation
}

fn unshuffle_card(shuffles: &Vec<Shuffle>, deck_size: i64, card: i64) -> i64 {
    shuffles.iter().rev().fold(card,
        |card, shuffle| { reverse_shuffle_single(card, deck_size, shuffle) })
}

fn mod_exp(a: i128, mut pow: i128, modulo: i128) -> i128 {
    let mut tmp: i128 = a;

    let mut result: i128 = One::one();
    while pow > 0 {
        if pow % 2 == 1 {
            result = (result * tmp) % modulo;
        }
        // println!("\t{} {} {} {}", pow, pow % 2, tmp, result);
        tmp = (tmp * tmp) % modulo;
        pow >>= 1;
    }

    result
}

fn hard(shuffles: &Vec<Shuffle>, deck_size: i128, card: i128, rounds: i128) -> i128 {
    let card2 = ToBigInt::to_bigint(&card).unwrap();
    let tmp = transform_card(shuffles, card2);

    // let result = (a * card + b) % deck_size;
    let a = ((tmp.0 % deck_size) + deck_size) % deck_size;
    let b = ((tmp.1 % deck_size) + deck_size) % deck_size;
    let a = a.to_u64_digits().1[0] as i128;
    let b = b.to_u64_digits().1[0] as i128;
    // println!("{} {} {} {}", a, b, card, deck_size);

    /*
    The transformation is:

    round 1
    x * a + b

    round 2
    (x * a + b) * a + b
    (x * a*a) + a*b + b

    round 3
    ((x * a*a) + a*b + b) * a + b
    x * a^3 + b*(a^2 + a + 1)

    round N:
    x * a^n + b*(a^n - 1)/(a-1)

    final answer is:
    x * a^n + b*(a^n - 1)/(a-1)
    where N is the number of rounds

    forward transform is: 
    x * a + b = y
    backward transform is:
    (y - b) / a = x

    Round 1:
    (y - b) * ia
    y*ia - b*ia

    Round 2:
    ((y - b) * ia - b) * ia
    y * ia^2 - b * (ia + ia^2)

    Round 3:
    (((y - b) * ia - b) * ia - b) * ia
    y * ia^3 - b * (ia + ia^2 + ia^3)

    Round N:
    y * ia^N - b * (ia + ia^2 ... + ia^N)
    y * ia^N - b * ia * (1 + ia^1 ... + ia^N-1)
    y * ia^N - b * ia * (ia^N - 1) / (ia - 1)

    print a_n

    */

    let ia = modinverse(a, deck_size).unwrap();
    let ia_n = mod_exp(ia, rounds, deck_size);
    let iia = modinverse(ia - 1, deck_size).unwrap();

    /*
    // This is the answer. Now... to avoid overflows:
    let mut result = (card * ia_n - b * ia * (ia_n - 1) * iia) % deck_size;
    result = (result + deck_size) % deck_size;
    */

    let part_a = (card * ia_n) % deck_size;
    let part_b = (b * ia) % deck_size;
    let part_c = ((ia_n - 1) * iia) % deck_size;
    let part_d = (part_b * part_c) % deck_size;
    let result = ((part_a - part_d) % deck_size + deck_size) % deck_size;
    return result;




    /*

    let num = mod_exp(a, rounds, deck_size);
    let denum = modinverse(a - 1, deck_size).unwrap();
    let part_a = (card * num) % deck_size;
    let part_b = (b * (num - 1)) % deck_size;
    let part_c = (part_b * denum) % deck_size;
    let part_d = (part_a + part_c) % deck_size;
    // println!("{} {} {} {}", part_a, part_b, part_c, part_d);
    return part_d;

    */



    /*
    // (2014*2019 + 662) % 10007
    for _round in 1..rounds+1 {
        card = (a * card + b) % deck_size;
        println!("{:?} {:?} {:?}", a, b, card);
    }

    card
    */

    /*
    let mut poly = poly![b, a];
    let card_big = ToBigInt::to_bigint(&card);
    let result = poly.eval(card_big);
    println!("{:?}", poly, result);
    */

    // result = a*x + b

    // now
    // let c = (&a * card + &b) % deck_size;

    /*
    let mut seen = HashMap::<u32, i64>::new();
    seen.insert(card, 0);
    for round in 1..rounds+1 {
        if round % 1000000 == 0 {
            println!("{} {} {}", round, seen.len(), card);
        }

        if let Some(previous) = seen.insert(card, round) {
            println!("Cycle found! {} {} ", previous, round);
            break;
        }
    }
    */

    //card
}

fn main() {
    let input = fs::read_to_string("input/22.txt").expect("Unable to read input file");
    let input = parse_input(&input);

    let deck_size = 10007;
    let card_to_pick = 2019;

    let answer_easy = easy(&input, deck_size, card_to_pick);
    println!("{:?}", answer_easy);
    // assert_eq!(card_to_pick as i128, hard(&input, deck_size as i128, answer_easy as i128, 1));

    let deck_size_large = 119315717514047i128;
    let shuffles_large =  101741582076661i128;
    let card_to_pick = 2020i128;
    println!("{:?}", hard(&input, deck_size_large, card_to_pick, shuffles_large));
    ()
}