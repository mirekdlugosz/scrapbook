use std::path::PathBuf;
use std::process::ExitCode;

use chrono::{Local, Months};
use clap::Parser;
use tera::{Context, Tera};

mod output;
mod parse_input;

#[derive(Parser)]
#[command(version, about)]
struct Cli {
    /// Path to template file
    #[arg(short, long = "template", value_name = "TEMPLATE_FILE")]
    template_file: PathBuf,

    /// Path to output file
    #[arg(
        short,
        long = "output",
        value_name = "OUTPUT_FILE",
        default_value = "-"
    )]
    output_file: PathBuf,

    /// Reference date
    #[arg(long, default_value = "today")]
    reference_date: String,
}

fn main() -> ExitCode {
    let args = Cli::parse();

    let reference_date = match parse_input::date_arg(&args.reference_date) {
        Ok(d) => d,
        Err(e) => {
            println!("Failed to parse {:?}: {:?}", args.reference_date, e.kind());
            return ExitCode::FAILURE;
        }
    };

    let (templates_glob, template_name) = match parse_input::template_arg(&args.template_file) {
        Ok((tg, tn)) => (tg, tn),
        Err(e) => {
            println!("{}", e);
            return ExitCode::FAILURE;
        }
    };

    let tera = match Tera::new(templates_glob.as_str()) {
        Ok(t) => t,
        Err(e) => {
            println!("Parsing error(s): {:?}", e);
            return ExitCode::FAILURE;
        }
    };

    let mut context = Context::new();
    let current_time = Local::now();
    let prev_month = reference_date - Months::new(1);
    let next_month = reference_date + Months::new(1);
    context.insert("this_month", &reference_date.and_hms_opt(1, 0, 0).unwrap().timestamp());
    context.insert("previous_month", &prev_month.and_hms_opt(1, 0, 0).unwrap().timestamp());
    context.insert("next_month", &next_month.and_hms_opt(1, 0, 0).unwrap().timestamp());
    context.insert("current_time", &current_time.timestamp());

    let rendered = match tera.render(template_name.as_str(), &context) {
        Ok(c) => c,
        Err(e) => {
            println!("Failed to render: {:?}", e);
            return ExitCode::FAILURE;
        }
    };

    match output::write(&rendered, &args.output_file) {
        Ok(_) => (),
        Err(e) => {
            println!("{}", e);
            return ExitCode::FAILURE;
        }
    }

    ExitCode::SUCCESS
}
