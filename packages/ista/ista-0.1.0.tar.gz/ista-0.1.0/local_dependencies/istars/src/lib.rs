pub mod funcs {
    pub fn add(a: usize, b: usize) -> usize {
        a + b
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(funcs::add(2, 2), 4);
    }
}
