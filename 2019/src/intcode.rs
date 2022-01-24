#[cfg(test)]
pub mod tests {
    use super::*;

    #[test]
    pub fn test_add() {
      let data = vec!(1, 0, 0, 0, 99);
      assert_eq!(run_intcode_simple(&data)[0], 2);
    }

    #[test]
    pub fn test_mul() {
      let data = vec!(2, 3, 0, 3, 99);
      assert_eq!(run_intcode_simple(&data)[3], 6);
    }

    #[test]
    pub fn test_easy() {
      let data = vec!(1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50);
      assert_eq!(run_intcode_simple(&data)[0], 3500);
      let data = vec!(2, 4, 4, 5, 99, 0);
      assert_eq!(run_intcode_simple(&data)[5], 9801);
      let data = vec!(1, 1, 1, 4, 99, 5, 6, 0, 99);
      assert_eq!(run_intcode_simple(&data)[0], 30);
    }

    #[test]
    pub fn test_input_repeat() {
      let data = vec!(3,0,4,0,99);
      let mut result:i64 = 0;
      run_intcode(&data, || 10, |val| result = val);
      assert_eq!(result, 10);
    }

    #[test]
    pub fn test_immediate_mode() {
      // Multiply 3 by data[4] and put it into data[4]
      let data = vec!(1002,4,3,4,33);
      let result = run_intcode_simple(&data);
      assert_eq!(result[4], 99);
    }

    #[test]
    pub fn test_negative_values() {
      let data = vec!(1101,100,-1,4,0);
      let result = run_intcode_simple(&data);
      assert_eq!(result[4], 99);
    }

    #[test]
    pub fn test_jumps_position_mode() {
      let data = vec!(3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9);
      let mut result:i64 = 0;
      run_intcode(&data, || 0, |val| result = val);
      assert_eq!(result, 0);

      run_intcode(&data, || 10, |val| result = val);
      assert_eq!(result, 1);
    }

    #[test]
    pub fn test_jumps_immediate_mode() {
      let data = vec!(3,3,1105,-1,9,1101,0,0,12,4,12,99,1);
      let mut result:i64 = 0;
      run_intcode(&data, || 0, |val| result = val);
      assert_eq!(result, 0);

      run_intcode(&data, || 10, |val| result = val);
      assert_eq!(result, 1);
    }

    #[test]
    pub fn test_comparisons() {
      let data = vec!(
        3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99);
      let mut result:i64 = 0;

      run_intcode(&data, || 0, |val| result = val);
      assert_eq!(result, 999);

      run_intcode(&data, || 8, |val| result = val);
      assert_eq!(result, 1000);

      run_intcode(&data, || 16, |val| result = val);
      assert_eq!(result, 1001);
    }
}

enum Mode {
  Positional = 0,
  Immediate = 1,
  Relative = 2,
}

#[derive(Debug, Copy, Clone)]
pub enum Opcode {
  Add,
  Multiply,
  Input,
  Output,
  JumpIfTrue,
  JumpIfFalse,
  LessThan,
  Equals,
  AdjustRelativeBase,
  Exit,
}

pub struct IntCode<'a> {
  code: Vec<i64>,
  modes: i64,
  stack_pointer: usize,
  relative_base: usize,
  opcode: Opcode,
  input: Box<dyn FnMut() -> i64 + 'a>,
  output: Box<dyn FnMut(i64) + 'a>,
}

impl<'a> IntCode<'a>
{
  pub fn new(code: Vec<i64>,
      input: Box<dyn FnMut() -> i64 + 'a>,
      output: Box<dyn FnMut(i64) + 'a>)
        -> IntCode<'a> {
    IntCode {
        code,
        stack_pointer: 0,
        modes: 0,
        opcode: Opcode::Exit,
        relative_base: 0,
        input,
        output
    }
  }

  fn get_mode (&self, index: usize) -> Mode {
    let i = self.modes / (10 as i64).pow(index as u32);
    match i % 10 {
      0 => Mode::Positional,
      1 => Mode::Immediate,
      2 => Mode::Relative,
      _ => panic!("Invalid mode")
    }
  }

  fn get_opcode(&self, value: i64) -> Opcode {
    match value {
      1 => Opcode::Add,
      2 => Opcode::Multiply,
      3 => Opcode::Input,
      4 => Opcode::Output,
      5 => Opcode::JumpIfTrue,
      6 => Opcode::JumpIfFalse,
      7 => Opcode::LessThan,
      8 => Opcode::Equals,
      9 => Opcode::AdjustRelativeBase,
      _ => Opcode::Exit,
    }
  }

  fn get_param (&self, index: usize) -> i64 {
    let code = &self.code;
    let mode = self.get_mode(index - 1);
    let value = code[self.stack_pointer + index] as i64;

    match mode {
      Mode::Immediate => value,
      Mode::Relative => code[(self.relative_base as i64 + value) as usize],
      Mode::Positional => code[value as usize],
    }
  }

  fn get_index (&self, index: usize) -> usize {
    let code = &self.code;
    let mode = self.get_mode(index - 1);
    let value = code[self.stack_pointer + index] as i64;

    match mode {
      Mode::Immediate => panic!("Invalid mode."),
      Mode::Relative => (self.relative_base as i64 + value) as usize,
      Mode::Positional => value as usize,
    }
  }


  pub fn run_step (&mut self) -> Opcode {
    let sp = self.stack_pointer;
    let code = &self.code;
    let value = code[sp];
    self.modes = value / 100;
    self.opcode = self.get_opcode(value % 100);

    let steps = match self.opcode {
      Opcode::Add => {
        let v1 = self.get_param(1);
        let v2 = self.get_param(2);
        let i3 = self.get_index(3);
        self.code[i3] = v1 + v2;
        4
      }
      Opcode::Multiply => {
        let v1 = self.get_param(1);
        let v2 = self.get_param(2);
        let i3 = self.get_index(3);
        self.code[i3] = v1 * v2;
        4
      }
      Opcode::Input => {
        let ia = self.get_index(1);
        let input = &mut self.input;
        let v1l = input();
        self.code[ia] = v1l;
        2
      }
      Opcode::Output => {
        let v1 = self.get_param(1);
        let output = &mut self.output;
        output(v1);
        2
      }
      Opcode::JumpIfTrue => {
        let v1 = self.get_param(1);
        if v1 != 0 {
          self.stack_pointer = self.get_param(2) as usize;
          0
        } else {
          3
        }
      }
      Opcode::JumpIfFalse => {
        let v1 = self.get_param(1);
        if v1 == 0 {
          self.stack_pointer = self.get_param(2) as usize;
          0
        } else {
          3
        }
      }
      Opcode::LessThan => {
        let v1 = self.get_param(1);
        let v2 = self.get_param(2);
        let i3 = self.get_index(3);
        self.code[i3] = if v1 < v2 { 1 } else { 0 };
        4
      }
      Opcode::Equals => {
        let v1 = self.get_param(1);
        let v2 = self.get_param(2);
        let i3 = self.get_index(3);
        self.code[i3] = if v1 == v2 { 1 } else { 0 };
        4
      }
      Opcode::AdjustRelativeBase => {
        let v1 = self.get_param(1);
        self.relative_base = (self.relative_base as i64 + v1) as usize;
        2
      }
      _ => return Opcode::Exit
    };

    self.stack_pointer += steps;

    self.opcode
  }
}

pub fn run_intcode_simple(code: &Vec<i64>) -> Vec<i64> {
  run_intcode(code, || 0, |val| println!("{}", val))
}

pub fn run_intcode_ascii<'a, O: 'a>(code: &Vec<i64>, input: &String, output: O) -> Vec<i64>
    where O: FnMut(i64) {

  let mut index = 0;
  let input = input.chars().collect::<Vec<_>>();

  run_intcode(code, || {
      let value = input[index] as i64;
      // println!("INPUT {} {} {}", index, input[index], value);
      index += 1;
      value
  }, output)
}

pub fn run_intcode<'a, I: 'a, O: 'a>(code: &Vec<i64>, input: I, output: O) -> Vec<i64>
    where I: FnMut() -> i64, O: FnMut(i64) {

  let mut code = code.clone();
  code.resize(10000, 0);

  let mut c = IntCode::new(code.clone(), Box::new(input), Box::new(output));

  loop {
    if let Opcode::Exit = c.run_step() {
      break
    }
  }

  c.code
}