use std::io::BufRead;

fn ord_sum_of_word(word: &str) -> u64 {
    let normalized_word = word.trim().to_lowercase();
    if normalized_word.is_empty() {
        return 0;
    }
    let mut ord_sum: u64 = 0;
    for letter in word.chars() {
        ord_sum += letter as u64;
    }
    ord_sum
}

pub fn run<R: BufRead>(dictionary: R, word_ord_sum: u64, quiet: &bool) -> Vec<String> {
    let mut found = Vec::new();
    for word in dictionary.lines().flatten() {
        let current_word_ord_sum = ord_sum_of_word(&word);
        if current_word_ord_sum != word_ord_sum {
            continue;
        }
        found.push(word);
        if *quiet {
            return found;
        }
    }
    found
}
