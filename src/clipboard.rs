//! Copies text to the system clipboard through the platform's own command
//! line tool, so no extra dependency is needed.

use std::io::Write;
use std::process::{Command, Stdio};

/// Clipboard commands to try, in order.
fn candidates() -> &'static [&'static [&'static str]] {
    if cfg!(target_os = "macos") {
        &[&["pbcopy"]]
    } else if cfg!(windows) {
        &[&["clip"]]
    } else {
        &[
            &["wl-copy"],
            &["xclip", "-selection", "clipboard"],
            &["xsel", "--clipboard", "--input"],
        ]
    }
}

fn run(command: &[&str], text: &str) -> std::io::Result<bool> {
    let mut child = Command::new(command[0])
        .args(&command[1..])
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()?;
    child
        .stdin
        .take()
        .expect("stdin is piped")
        .write_all(text.as_bytes())?;
    Ok(child.wait()?.success())
}

pub fn copy(text: &str) -> Result<(), String> {
    for command in candidates() {
        if let Ok(true) = run(command, text) {
            return Ok(());
        }
    }
    let tools: Vec<&str> = candidates().iter().map(|command| command[0]).collect();
    Err(format!(
        "could not copy to the clipboard (tried: {})",
        tools.join(", ")
    ))
}
