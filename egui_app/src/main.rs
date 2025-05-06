#![warn(clippy::all, rust_2018_idioms)]
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on windows when built in release mode
mod app;
mod client;
mod ui;
use app::PaperclipAdjacent;



fn main() -> eframe::Result<()> {
    // configure window settings for the native egui app
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("//paperclip_adjacent")
            .with_inner_size([400.0, 300.0])        
            .with_min_inner_size([300.0, 220.0]),                   
        ..Default::default() 
    };

    // launch the app using eframe's native backend
    eframe::run_native(
        "//paperclip_adjacent", // window title                      
        options,                                                
        Box::new(|cc| {
            let app = PaperclipAdjacent::new(cc);
            Ok(Box::new(app))
        }),
    )
}
