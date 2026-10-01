use std::sync::LazyLock;

use crate::moves::{Token, parse_tokens};

pub type Algorithm = Vec<Token>;

fn load(name: &str, json: &str) -> Vec<Algorithm> {
    let algorithms: Vec<String> =
        serde_json::from_str(json).unwrap_or_else(|e| panic!("{name}: invalid JSON: {e}"));
    algorithms
        .iter()
        .map(|alg| parse_tokens(alg).unwrap_or_else(|e| panic!("{name}: {e}")))
        .collect()
}

macro_rules! algorithms {
    ($name:ident, $file:literal) => {
        pub static $name: LazyLock<Vec<Algorithm>> =
            LazyLock::new(|| load($file, include_str!(concat!("../../algorithms/", $file))));
    };
}

algorithms!(OLL, "OLL.json");
algorithms!(PLL, "PLL.json");
algorithms!(TOP_F2L, "top_f2l.json");
algorithms!(F2L_CORNER_IN_SLOT, "f2l_case2.json");
algorithms!(F2L_EDGE_IN_SLOT, "f2l_case3.json");

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_algorithms_parse() {
        assert_eq!(OLL.len(), 57);
        assert_eq!(PLL.len(), 21);
        assert!(!TOP_F2L.is_empty());
        assert!(!F2L_CORNER_IN_SLOT.is_empty());
        assert!(!F2L_EDGE_IN_SLOT.is_empty());
    }
}
