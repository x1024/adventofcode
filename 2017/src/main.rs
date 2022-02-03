use std::env;

mod p1;
mod p2;
mod p3;
mod p4;
mod p5;
mod p6;
mod p7;
mod p8;
mod p9;
mod p10;
mod p11;
mod p12;
mod p13;
mod p14;
mod p15;
mod p16;
mod p17;
mod p18;
mod p19;
mod p20;
mod p21;
mod p22;
mod p23;
mod p24;
mod p25;

fn main() {
    for arg in env::args().skip(1) {
        // println!("{}", arg);
        match &arg as &str {
            "1" => p1::main(),
            "2" => p2::main(),
            "3" => p3::main(),
            "4" => p4::main(),
            "5" => p5::main(),
            "6" => p6::main(),
            "7" => p7::main(),
            "8" => p8::main(),
            "9" => p9::main(),
            "10" => p10::main(),
            "11" => p11::main(),
            "12" => p12::main(),
            "13" => p13::main(),
            "14" => p14::main(),
            "15" => p15::main(),
            "16" => p16::main(),
            "17" => p17::main(),
            "18" => p18::main(),
            "19" => p19::main(),
            "20" => p20::main(),
            "21" => p21::main(),
            "22" => p22::main(),
            "23" => p23::main(),
            "24" => p24::main(),
            "25" => p25::main(),
            _ => panic!("Unknown program specified"),
        }
    }
}
