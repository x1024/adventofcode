use std::fs;
use counter::Counter;


#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy() {
      let input = String::from("123456789012");
      assert_eq!(easy(&input, 3, 2), 1);
    }

    #[test]
    pub fn test_hard() {
      let input = String::from("0222112222120000");
      assert_eq!(hard(&input, 2, 2), " █
█ ");
    }
}

fn easy(data: &String, width: usize, height: usize) -> usize {
    let mut default = "".chars().collect::<Counter<_>>();
    default[&'0'] = width * height;

    let chars = data.chars().collect::<Vec<_>>();
    let chunks = chars.chunks(width * height);
    let result = chunks
        .map(|x| { x.to_vec().into_iter().collect::<Counter<char>>() })
        .fold(default, |acc, x| {
            if acc[&'0'] < x[&'0'] { acc } else { x }
        });
    result[&'1'] * result[&'2']
}

fn hard(data: &String, width: usize, height: usize) -> String {
    let chars = data.chars().collect::<Vec<_>>();
    let chunks = chars.chunks(width * height).collect::<Vec<_>>();
    let result = chunks
        .iter()
        .fold(chunks[0].iter().collect::<String>(), |image, layer| {
            image.chars()
                .zip(layer.iter())
                .map(|(a, &b)| if a == '2' { b } else { a })
                .collect::<String>()
        });

    let rows = result
        .chars()
        .collect::<Vec<_>>()
        .chunks(width)
        .map(|c| c.iter().collect::<String>())
        .collect::<Vec<_>>()
        .join("\n");

    let rows = str::replace(&rows, "0", " ");
    let rows = str::replace(&rows, "1", "█");
    rows
}

fn main() {
    let code = fs::read_to_string("input/8.txt").unwrap();
    println!("{}", easy(&code, 25, 6));
    println!("{}", hard(&code, 25, 6));
    ()
}
