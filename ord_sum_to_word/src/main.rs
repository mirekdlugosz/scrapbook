use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use std::process::ExitCode;

use clap::Parser;

#[derive(Parser)]
#[command(version, about)]
struct Cli {
    /// Sum of codepoints of string
    #[arg(value_parser = clap::value_parser!(u64).range(1..))]
    word_ord_sum: u64,

    /// Path to dictionary of known words
    #[arg(short, long, value_name = "FILE")]
    dictionary: PathBuf,

    /// Don't print anything to STDOUT
    #[arg(short, long, action = clap::ArgAction::SetTrue)]
    quiet: bool,
}

fn main() -> ExitCode {
    let args = Cli::parse();

    let fh = File::open(args.dictionary).expect("Could not open dictionary file");
    let dictionary = BufReader::new(fh);

    let found = ord_sum_to_word::run(dictionary, args.word_ord_sum, &args.quiet);

    if found.is_empty() {
        return ExitCode::FAILURE;
    }

    if !args.quiet {
        println!("{}", found.join("\n"));
    }

    ExitCode::SUCCESS
}
