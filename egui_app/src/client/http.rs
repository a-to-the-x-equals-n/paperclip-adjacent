#![allow(dead_code)]
use serde::{Deserialize, Serialize};

const URL: &str = "http://localhost:8007/memcells";

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct Memcell {
    pub id: Option<u32>,
    pub task: String,
}


pub async fn get_all_memcells() -> Result<Vec<Memcell>, reqwest::Error> {
    let res = reqwest::get(URL) // adjust port if needed
        .await?
        .json::<Vec<Memcell>>()
        .await?;

    println!("memcells: {:#?}", res);
    Ok(res)
}


pub async fn create_memcell(phone: &str, task: &str) -> Result<(), reqwest::Error> {
    let payload = serde_json::json!({
        "phone": phone,
        "task": task,
    });

    let client = reqwest::Client::new();
    let res = client
        .post("http://localhost:5000/memcells")
        .json(&payload)
        .send()
        .await?
        .json::<serde_json::Value>()
        .await?;

    println!("created: {:#?}", res);
    Ok(())
}


pub async fn delete_memcell(mem_id: i32) -> Result<(), reqwest::Error> {
    let url = format!("http://localhost:5000/memcells/{}", mem_id);
    let client = reqwest::Client::new();

    let res = client
        .delete(&url)
        .send()
        .await?
        .json::<serde_json::Value>()
        .await?;

    println!("deleted: {:#?}", res);
    Ok(())
}


#[tokio::main]
async fn main() {
    get_all_memcells().await.unwrap();
    create_memcell("1234567890", "Feed dog").await.unwrap();
    delete_memcell(3).await.unwrap();
}
