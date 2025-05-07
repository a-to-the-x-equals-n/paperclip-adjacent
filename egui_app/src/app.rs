// use std::sync::Arc; 
use egui::{TextEdit, RichText, TextStyle};
#[allow(unused_imports)]
use crate::client::http::{create_memcell, get_all_memcells, delete_memcell, update_memcell, Memcell};
use crate::utils::auth::{get_evar, fmt_phone_input, clean_phone_number};
use crate::ui::paperclip_adjacent::{PaperclipAdjacent, AppState};

const LG_PAD: f32 = 24.0;
const MD_PAD: f32 = 18.0;
const SM_PAD: f32 = 10.0;

// --- FRAME MANAGEMENT --- 
impl eframe::App for PaperclipAdjacent {
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    // called each time the UI needs repainting 
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {

        match self.state {
            //-------------------
            // --- LOGIN PAGE ---
            //-------------------
            AppState::Login => {

                // --- top panel ---
                egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
                    ui.add_space(MD_PAD);
                    // app title
                    ui.vertical_centered(|ui| {
                        ui.heading(&self.heading);
                        ui.add_space(SM_PAD);
                        ui.label(&self.sub_heading);
                    });
                    ui.add_space(MD_PAD);
                });
                
                // --- center panel ---
                egui::CentralPanel::default().show(ctx, |ui| {
                    ui.add_space(LG_PAD);
        
                    // --- phone number text box ---
                    ui.vertical_centered(|ui| {
                        let hint = RichText::new("phone number")
                            .italics()
                            .color(egui::Color32::from_rgba_unmultiplied(0xF5, 0x22, 0x77, 80));

                        // format phone number input
                        let response = ui.add(TextEdit::singleline(&mut self.phone).hint_text(hint));
                        if response.changed() {
                            let formatted = fmt_phone_input(&self.phone);
                            if formatted != self.phone {
                                self.phone = formatted; // only assign if it's different to avoid flicker
                            }
                        }
                        ui.add_space(SM_PAD);

                        // --- 'login' button ---
                        if ui
                            .add(egui::Button::new(RichText::new("➡")
                                .color(egui::Color32::WHITE))
                                .fill(egui::Color32::from_rgb(0, 255, 0)))
                            .clicked() {

                            // validate phone number
                            if let Some(phone_ev) = get_evar("PHONE") {

                                // clean phone number of all hyphens
                                let clean_input = clean_phone_number(&self.phone);

                                // evaluate login credentials
                                if clean_input == phone_ev {

                                    // --- login success! ---
                                    // pause/block threading
                                    // parse server for memcells
                                    let rt = tokio::runtime::Runtime::new().unwrap();
                                    match rt.block_on(get_all_memcells()) {
                                        Ok(memcells) => self.memcells = memcells,
                                        Err(err) => eprintln!("Failed to fetch memcells: {}", err),
                                    }
                                    self.state = AppState::Main;
                                } else {
                                    // --- login failed ---
                                    // unrecognized number
                                    eprintln!("invalid phone");
                                    self.phone = String::new();
                                }
                            } else {
                                // --- login failed ---
                                // no PHONE envar
                                eprintln!("PHONE not set in .env");
                                std::process::exit(1);
                            }
                        }
                    });
                    ui.add_space(LG_PAD);
                });
            }
            //------------------
            // --- MAIN PAGE ---
            //------------------
            AppState::Main => {
                // --- top control panel ---
                egui::TopBottomPanel::top("main_top").show(ctx, |ui| {
                    ui.add_space(MD_PAD);
                    ui.horizontal(|ui| {
                        // app title
                        ui.vertical_centered(|ui| {
                            ui.heading(&self.heading);
                        });
                    });
                    ui.add_space(SM_PAD);
                });
                
                // --------------------
                // --- MEMCELL LIST ---
                // --------------------
                egui::CentralPanel::default().show(ctx, |ui| {
                    ui.add_space(SM_PAD);

                    egui::ScrollArea::vertical().show(ui, |ui| {
                        let cell_count = self.memcells.len();
                        let mut to_delete: Option<usize> = None;

                        for index in 0..cell_count {
                            let is_selected = self.selected_memcell == Some(index);
                            let task = self.memcells[index].task.clone();
                            let id = self.memcells[index].id;

                            ui.horizontal(|ui| {
                                if ui
                                    .add(egui::Button::new(RichText::new("❌")
                                        .color(egui::Color32::WHITE))
                                        .fill(egui::Color32::from_rgb(255, 0, 0)))
                                    .clicked()
                                {
                                    to_delete = Some(index);
                                }

                                if ui.selectable_label(is_selected, format!("[{}] {}", id.unwrap_or(0), task)).clicked() {
                                    self.selected_memcell = Some(index);
                                }
                            });
                        }

                        // --- memcell delete request ---
                        if let Some(index) = to_delete {
                            // get the mem_id before removing
                            if let Some(mem_id) = self.memcells[index].id {
                                // fire-and-forget HTTP delete call
                                tokio::spawn(async move {
                                    if let Err(err) = delete_memcell(mem_id as i32).await {
                                        eprintln!("Failed to delete memcell {}: {}", mem_id, err);
                                    }
                                });
                            }
                        
                            // update local state
                            self.memcells.remove(index);
                        
                            // fix selection
                            if self.selected_memcell == Some(index) {
                                self.selected_memcell = None;
                            } else if let Some(sel) = self.selected_memcell {
                                if sel > index {
                                    self.selected_memcell = Some(sel - 1);
                                }
                            }
                        }                        
                    });

                    // --- add memcell button ---
                    ui.vertical_centered(|ui| {
                        ui.add_space(SM_PAD);

                        let mut add_btn = egui::Button::new(RichText::new("➕")
                            .color(egui::Color32::WHITE))
                            .fill(egui::Color32::from_rgb(0, 255, 0));

                        if self.memcells.len() >= 10 {
                            add_btn = add_btn.sense(egui::Sense::hover()); // disables clicking
                        }
                        
                        if ui.add(add_btn).clicked() && self.memcells.len() < 10 {
                            self.state = AppState::CreateNew;
                        }
                    });
                    ui.add_space(SM_PAD);
                });

                // ----------------------
                // --- MEMCELL EDITOR ---
                // ----------------------
                egui::TopBottomPanel::bottom("task_editor").show(ctx, |ui| {
                    // ui.add_space(SM_PAD);
                    ui.label(RichText::new("[edit]:").text_style(TextStyle::Button));
                    // ui.add_space(SM_PAD);
                    let hint = RichText::new("description...")
                            .italics()
                            .color(egui::Color32::from_rgba_unmultiplied(0xF5, 0x22, 0x77, 80));

                    ui.vertical_centered(|ui| {
                        if let Some(index) = self.selected_memcell {
                            let cell = &mut self.memcells[index];
                            let response = ui.add(
                                egui::TextEdit::multiline(&mut cell.task)
                                    .hint_text(hint)
                                    .desired_rows(3)
                                    .lock_focus(true)
                                    .frame(true),
                            );
                
                            if response.changed() {
                                if let Some(mem_id) = cell.id {
                                    let task_clone = cell.task.clone();
                                    tokio::spawn(async move {
                                        if let Err(err) = update_memcell(mem_id, &task_clone).await {
                                            eprintln!("Failed to update memcell {}: {}", mem_id, err);
                                        }
                                    });
                                }
                            }
                        } else {
                            let hint = RichText::new("memcell...")
                                .italics()
                                .color(egui::Color32::from_rgba_unmultiplied(0xF5, 0x22, 0x77, 80));

                            // No memcell selected — show an empty, non-editable field
                            let mut placeholder = String::new();
                            ui.add(egui::TextEdit::multiline(&mut placeholder)
                                .hint_text(hint)
                                .desired_rows(3)
                                .interactive(false)
                                .frame(true),
                            );
                        }
                    });
                    ui.add_space(SM_PAD);
                });
            }
            //--------------------
            // --- CREATE PAGE --- 
            //--------------------
            AppState::CreateNew => {

                // --- top control panel ---
                egui::TopBottomPanel::top("main_top").show(ctx, |ui| {
                    ui.add_space(MD_PAD);
                    ui.horizontal(|ui| {
                        // app title
                        ui.vertical_centered(|ui| {
                            ui.heading(&self.heading);
                        });
                    });
                    ui.add_space(SM_PAD);
                });

                // --- center text box panel ---
                egui::CentralPanel::default().show(ctx, |ui| {
                    ui.add_space(MD_PAD);
                    ui.vertical_centered(|ui| {
                        ui.add_space(SM_PAD);

                        if self.creation_error {
                            ui.label(RichText::new("[error]: too long").color(egui::Color32::RED));
                            ui.add_space(SM_PAD);
                        }

                        let hint = RichText::new("new memcell...")
                                .italics()
                                .color(egui::Color32::from_rgba_unmultiplied(0xF5, 0x22, 0x77, 80));

                        ui.add(egui::TextEdit::multiline(&mut self.new_task)
                            .hint_text(hint)
                            .desired_rows(4)
                            .frame(true),
                        );
                    });

                    ui.add_space(SM_PAD);
                    
                    // ui.vertical_centered(|ui| {
                    ui.with_layout(egui::Layout::top_down(egui::Align::Center)
                            .with_main_align(egui::Align::Center),
                        |ui| {
                    //     ui.horizontal_centered(|ui| {
                            // --- submit button --- 
                            if ui
                                .add(egui::Button::new(RichText::new("✅")
                                    .color(egui::Color32::WHITE))
                                    .fill(egui::Color32::from_rgb(0, 255, 0)))
                                .clicked()
                            {
                                if self.new_task.trim().len() > 0 && self.new_task.len() <= 160 {
                                    let task_clone = self.new_task.clone();
                                    let phone = clean_phone_number(&self.phone);
                                    tokio::spawn(async move {
                                        if let Err(err) = create_memcell(&phone, &task_clone).await {
                                            eprintln!("failed to create memcell: {}", err);
                                        }
                                    });
                                    
                                    self.creation_error = false;
                                    self.new_task.clear();
                                    self.state = AppState::Main;
                                } else {
                                    self.creation_error = true;
                                }
                            }

                            // --- cancel button ---
                            if ui
                                .add(egui::Button::new(RichText::new("❌")
                                    .color(egui::Color32::WHITE))
                                    .fill(egui::Color32::from_rgb(255, 0, 0)),)
                                .clicked()
                            {
                                self.creation_error = false;
                                self.new_task.clear();
                                self.state = AppState::Main;
                            }
                        });
                    // });
                    ui.add_space(SM_PAD);
                });
            }
        }
    }
}