use std::fs;
use std::path::PathBuf;

pub fn write(content: &str, output_file: &PathBuf) -> Result<(), String> {
    let mut error = String::with_capacity(80);

    if output_file.display().to_string() == String::from("-") {
        println!("{}", content);
        return Ok(());
    }

    let output_file_dir = match output_file.as_path().parent() {
        Some(p) => p,
        None => {
            let err_msg = format!("{} must point to the file", output_file.display());
            error.push_str(&err_msg);
            return Err(error);
        }
    };

    match fs::create_dir_all(output_file_dir) {
        Ok(_) => (),
        Err(e) => {
            let err_msg = format!(
                "Could not create directory {:?}: {:?}",
                output_file_dir.display(),
                e.kind()
            );
            error.push_str(&err_msg);
            return Err(error);
        }
    };

    match fs::write(output_file, content) {
        Ok(_) => (),
        Err(e) => {
            let err_msg = format!(
                "Could not write to file {:?}: {:?}",
                output_file.display(),
                e.kind()
            );
            error.push_str(&err_msg);
            return Err(error);
        }
    }

    Ok(())
}
