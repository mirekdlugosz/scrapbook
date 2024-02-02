use std::path::PathBuf;

use chrono::{Local, NaiveDate, ParseError};

pub fn date_arg(reference_date: &str) -> Result<NaiveDate, ParseError> {
    if reference_date == "today" {
        let right_now = Local::now();
        return Ok(right_now.date_naive());
    }

    return NaiveDate::parse_from_str(reference_date, "%Y-%m-%d");
}

pub fn template_arg(template_path: &PathBuf) -> Result<(String, String), String> {
    let mut error = String::with_capacity(80);

    let absolute_path = match template_path.as_path().canonicalize() {
        Ok(p) => p,
        Err(e) => {
            let err_msg = format!(
                "{} doesn't look like a proper path: {}",
                template_path.display(),
                e.kind()
            );
            error.push_str(&err_msg);
            return Err(error);
        }
    };
    let templates_root = match absolute_path.parent() {
        Some(t) => t,
        None => {
            let err_msg = format!("{} must point to the file", template_path.display());
            error.push_str(&err_msg);
            return Err(error);
        }
    };

    let templates_glob = match templates_root.to_str() {
        Some(s) => {
            format!("{}/*", s)
        }
        None => {
            let err_msg = format!("{} contains non-UTF-8 characters", template_path.display());
            error.push_str(&err_msg);
            return Err(error);
        }
    };

    let filename = match absolute_path.file_name() {
        Some(p) => p,
        None => {
            let err_msg = format!("{} must point to the file", template_path.display());
            error.push_str(&err_msg);
            return Err(error);
        }
    };
    let template_name = match filename.to_str() {
        Some(s) => s.to_owned(),
        None => {
            let err_msg = format!("{} contains non-UTF-8 characters", template_path.display());
            error.push_str(&err_msg);
            return Err(error);
        }
    };
    Ok((templates_glob, template_name))
}
