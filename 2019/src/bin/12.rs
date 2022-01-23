use num::abs;
use num::integer::lcm;
use std::collections::HashMap;
use std::ops::Add;
use std::ops::AddAssign;
use std::ops::Sub;
use std::ops::SubAssign;
use std::fs;
use num::signum;

#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_parse_input() {
        let data = "<x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>";
        let moons = parse_input(data);
        assert_eq!(moons[0].position, Point(-1, 0, 2));
        assert_eq!(moons[1].position, Point(2, -10, -7));
        assert_eq!(moons[2].position, Point(4, -8, 8));
        assert_eq!(moons[3].position, Point(3, 5, -1));

        assert_eq!(moons[0].velocity, Point(0, 0, 0));
        assert_eq!(moons[1].velocity, Point(0, 0, 0));
        assert_eq!(moons[2].velocity, Point(0, 0, 0));
        assert_eq!(moons[3].velocity, Point(0, 0, 0));
    }

    #[test]
    pub fn test_simulate() {
        let data = "<x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>";
        let mut moons = parse_input(data);
        Moon::simulate(&mut moons);

        assert_eq!(moons[0].position, Point(2, -1, 1));
        assert_eq!(moons[1].position, Point(3, -7, -4));
        assert_eq!(moons[2].position, Point(1, -7, 5));
        assert_eq!(moons[3].position, Point(2, 2, 0));

        assert_eq!(moons[0].velocity, Point(3, -1, -1));
        assert_eq!(moons[1].velocity, Point(1, 3, 3));
        assert_eq!(moons[2].velocity, Point(-3, 1, -3));
        assert_eq!(moons[3].velocity, Point(-1, -3, 1));
    }

    #[test]
    pub fn test_energy() {
        let data = "<x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>";
        let mut moons = parse_input(data);
        for _ in 0..10 {
            Moon::simulate(&mut moons);
        }

        assert_eq!(moons.iter().map(|moon| moon.energy()).sum::<i32>(), 179);
    }

    #[test]
    pub fn test_full() {
        let data = "<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>";
        let mut moons = parse_input(data);
        for _ in 0..100 {
            Moon::simulate(&mut moons);
        }

        assert_eq!(moons.iter().map(|moon| moon.energy()).sum::<i32>(), 1940);
    }

    #[test]
    pub fn test_hard() {
        let data = "<x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>";
        let mut moons = parse_input(data);
        assert_eq!(hard(&moons), 2772);
    }

    #[test]
    pub fn test_hard_2() {
        let data = "<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>";
        let mut moons = parse_input(data);
        assert_eq!(hard(&moons), 4686774924);
    }
}

#[derive(Debug, Copy, Clone, PartialEq)]
struct Point(i32, i32, i32);

impl Add for Point {
    type Output = Self;
    fn add(self, other: Self) -> Self::Output {
        Point(self.0 + other.0, self.1 + other.1, self.2 + other.2)
    }
}

impl Sub for Point {
    type Output = Self;
    fn sub(self, other: Self) -> Self::Output {
        Self(self.0 - other.0, self.1 - other.1, self.2 - other.2)
    }
}

impl AddAssign for Point {
    fn add_assign(&mut self, other: Self) {
        *self = Self(self.0 + other.0, self.1 + other.1, self.2 + other.2);
    }
}

impl SubAssign for Point {
    fn sub_assign(&mut self, other: Self) {
        *self = Self(self.0 - other.0, self.1 - other.1, self.2 - other.2);
    }
}

#[derive(Debug, Copy, Clone)]
struct Moon {
    position: Point,
    velocity: Point,
}

impl Moon {
    fn add_gravity(&mut self, moons: &Vec<Moon>) {
        let mut total_delta = Point(0, 0, 0);

        for moon in moons {
            let delta = self.position - moon.position;
            total_delta -= Point(signum(delta.0), signum(delta.1), signum(delta.2));
        }

        self.velocity += total_delta;
    }

    fn do_move(&mut self) {
        self.position += self.velocity;
    }

    fn simulate(moons: &mut Vec<Moon>) {
        let tmp = moons.clone();
        for moon in moons.iter_mut() {
            moon.add_gravity(&tmp);
        }
        for moon in moons {
            moon.do_move();
        }
    }

    fn find_cycle(moons: &Vec<Moon>) -> i64 {
        let mut moons = moons.clone();
        let mut seen_x = HashMap::<((i32, i32), (i32, i32), (i32, i32), (i32, i32)), i64>::new();
        let mut seen_y = HashMap::<((i32, i32), (i32, i32), (i32, i32), (i32, i32)), i64>::new();
        let mut seen_z = HashMap::<((i32, i32), (i32, i32), (i32, i32), (i32, i32)), i64>::new();

        let mut period_x: i64 = 0;
        let mut period_y: i64 = 0;
        let mut period_z: i64 = 0;
        let mut i = 0;
        loop {
            let x = moons.iter().map(|m| (m.position.0, m.velocity.0)).collect::<Vec<_>>();
            let x = (x[0], x[1], x[2], x[3]);

            let y = moons.iter().map(|m| (m.position.1, m.velocity.1)).collect::<Vec<_>>();
            let y = (y[0], y[1], y[2], y[3]);

            let z = moons.iter().map(|m| (m.position.2, m.velocity.2)).collect::<Vec<_>>();
            let z = (z[0], z[1], z[2], z[3]);

            if period_x == 0 && seen_x.contains_key(&x) { period_x = i; }
            if period_y == 0 && seen_y.contains_key(&y) { period_y = i; }
            if period_z == 0 && seen_z.contains_key(&z) { period_z = i; }

            if period_x != 0 && period_y != 0 && period_z != 0 {
                break
            }

            // println!("{} {:?} {:?} {:?}", i, period_x, period_y, period_z);

            seen_x.insert(x, i);
            seen_y.insert(y, i);
            seen_z.insert(z, i);

            i += 1;
            Moon::simulate(&mut moons);
        }

        // println!("{:?} {:?} {:?}", period_x, period_y, period_z);
        lcm(lcm(period_x, period_y), period_z)
    }

    fn energy(&self) -> i32 {
        let p = self.position;
        let v = self.velocity;
        let e_p = abs(p.0) + abs(p.1) + abs(p.2);
        let e_k = abs(v.0) + abs(v.1) + abs(v.2);
        e_p * e_k
    }
}

fn parse_input(data: &str) -> Vec<Moon> {
    data.split("\n")
        .map(|line| line.trim()
            .replace("<", "")
            .replace(">", "")
            .split(", ")
            .map(|segment| segment[2..].parse::<i32>().unwrap())
            .collect::<Vec<_>>())
        .map(|numbers| {
            Moon {
                position: Point(numbers[0], numbers[1], numbers[2]),
                velocity: Point(0, 0, 0),
            }
        })
        .collect::<Vec<_>>()
}

fn easy(moons: &Vec<Moon>) -> i32 {
    let mut moons = moons.clone();
    for _ in 0..1000 {
        Moon::simulate(&mut moons);
    }

    moons.iter().map(|moon| moon.energy()).sum::<i32>()
}

fn hard(moons: &Vec<Moon>) -> i64 {
    let mut moons = moons.clone();
    Moon::find_cycle(&moons)
}

fn main() {
    let input = fs::read_to_string("input/12.txt").expect("Unable to read input file");
    let input = parse_input(&input);
    println!("{}", easy(&input));
    println!("{}", hard(&input));
    ()
}
