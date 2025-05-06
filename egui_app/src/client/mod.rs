// src/client/mod.rs
pub mod http;
#[allow(unused_imports)]
pub use http::{create_memcell, get_all_memcells, delete_memcell, Memcell};
