use std::fs;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_easy() {
        let data = String::from("R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83");
        assert_eq!(easy(&data), 159);
        let data = String::from("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7");
        assert_eq!(easy(&data), 135);
    }

    #[test]
    pub fn test_hard() {
        let data = String::from("R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83");
        assert_eq!(hard(&data), 610);
        let data = String::from("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7");
        assert_eq!(hard(&data), 410);
    }
}

#[derive(Debug)]
enum Direction {
    R,
    L,
    U,
    D,
}

#[derive(Debug)]
struct Line {
    sx: i32,
    sy: i32,
    ex: i32,
    ey: i32,
}

impl Line {
    fn min_y(&self) -> i32 { if self.sy < self.ey { self.sy } else { self.ey } }
    fn max_y(&self) -> i32 { if self.sy > self.ey { self.sy } else { self.ey } }
    fn min_x(&self) -> i32 { if self.sx < self.ex { self.sx } else { self.ex } }
    fn max_x(&self) -> i32 { if self.sx > self.ex { self.sx } else { self.ex } }
    fn length(&self) -> u32 {
        ((self.ex - self.sx).abs() + (self.ey - self.sy).abs()) as u32
    }

    fn intersection(&self, other: &Line) -> Option<(i32, i32)> {
        // println!("asdasd {:?}", self.points());
        if self.sx == self.ex && other.sy == other.ey {
            if other.sy < self.min_y() || other.sy > self.max_y() { return None }
            if !(self.sx >= other.min_x() && self.sx <= other.max_x()) { return None }
            return Some((self.sx, other.sy))
        }

        if self.sy == self.ey && other.sx == other.ex {
            if other.sx < self.min_x() || other.sx > self.max_x() { return None }
            if !(self.sy >= other.min_y() && self.sy <= other.max_y()) { return None }
            return Some((other.sx, self.sy))
        }

        None
    }
}

#[derive(Debug)]
struct Intersection {
    distance: u32,
    steps: u32,
}


#[derive(Debug)]
struct Route {
    segments: Vec<Segment>
}

impl Route {
    fn lines(&self) -> Vec<Line> {
        let mut result = Vec::<Line>::new();
        let mut x = 0;
        let mut y = 0;

        for sa in &self.segments {
            let offset: (i32, i32) = match &sa.dir {
                Direction::R => (0, 1),
                Direction::L => (0, -1),
                Direction::U => (-1, 0),
                Direction::D => (1, 0),
            };
            let length = sa.length as i32;

            let sx = x;
            let sy = y;
            let ex = x + offset.0 * length;
            let ey = y + offset.1 * length;
            result.push(Line { sx, sy, ex, ey });
            x = ex;
            y = ey;
        }

        result
    }

    fn intersections(&self, other: &Route) -> Vec<Intersection> {
        let mut v = Vec::<Intersection>::new();
        let mut total_steps_a: u32 = 0;
        for line_a in self.lines() {
            let mut total_steps_b: u32 = 0;
            for line_b in other.lines() {
                // println!("{:?} {:?}", line_a, line_b);
                if let Some(i) = line_a.intersection(&line_b) {
                    let l_a = Line { sx: line_a.sx, sy: line_a.sy, ex: i.0, ey: i.1 }.length();
                    let l_b = Line { sx: line_b.sx, sy: line_b.sy, ex: i.0, ey: i.1 }.length();
                    let steps = total_steps_a + l_a + total_steps_b + l_b;

                    let distance = (i.0.abs() + i.1.abs()) as u32;
                    v.push(Intersection { distance, steps });
                }
                total_steps_b += line_b.length();
            }
            total_steps_a += line_a.length();
        }

        v
    }
}

#[derive(Debug)]
struct Segment {
    dir: Direction,
    length: u32,
}

impl Segment {
    fn from_string(segment: &str) -> Segment {
        let dir = match &segment[..1] {
            "R" => Direction::R,
            "L" => Direction::L,
            "D" => Direction::D,
            "U" => Direction::U,
            _ => Direction::U
        };

        let length = segment[1..].parse::<u32>().unwrap();

        Segment { dir, length }
    }
}

fn parse_input(input: &String) -> Vec<Route> {
    input.split("\n")
        .map(|row| row.split(",")
            .map(|segment| Segment::from_string(segment))
            .collect::<Vec<_>>())
        .map(|segments| Route { segments })
        .collect::<Vec<_>>()
}

fn easy(input: &String) -> u32 {
    let input = parse_input(input);
    let route_a = input.get(0).unwrap();
    let route_b = input.get(1).unwrap();
    let mut intersections = route_a.intersections(route_b)
        .iter()
        .map(|i| i.distance)
        .filter(|i| *i > 0)
        .collect::<Vec<_>>();
    intersections.sort();
    intersections[0]
}

fn hard(input: &String) -> u32 {
    let input = parse_input(input);
    let route_a = input.get(0).unwrap();
    let route_b = input.get(1).unwrap();
    let mut intersections = route_a.intersections(route_b)
        .iter()
        .map(|i| i.steps)
        .filter(|i| *i > 0)
        .collect::<Vec<_>>();
    intersections.sort();
    intersections[0]
}

fn main() {
    let res = fs::read_to_string("input/3.txt").expect("Input file not found");
    println!("{}", easy(&res));
    println!("{}", hard(&res));
    ()
}
