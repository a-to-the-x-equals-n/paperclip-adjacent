use dotenvy::dotenv;
use std::env;

// returns the expected phone number from the .env file
// loads .env once, silently
pub fn get_evar(key: &str) -> Option<String> {
    let _ = dotenv(); // silently ignore if already loaded

    // `.map()` only runs `if Some`
    // only cleans if necessary
    env::var(key).ok().map(|val|clean_phone_number(&val))
}

// dynamically formats a phone number as "XXX-XXX-XXXX"
pub fn fmt_phone_input(input: &str) -> String {
    let digits_only: String = input.chars().filter(|c| c.is_ascii_digit()).collect();

    match digits_only.len() {
        0..=3 => digits_only,
        4..=6 => format!("{}-{}", &digits_only[..3], &digits_only[3..]),
        7..=10 => format!("{}-{}-{}", &digits_only[..3], &digits_only[3..6], &digits_only[6..]),
        _ => digits_only, // allow overflow without formatting beyond 10 digits
    }
}


// removes all non-digit characters from a phone number string
pub fn clean_phone_number(input: &str) -> String {
    input.chars().filter(|c| c.is_ascii_digit()).collect()
}