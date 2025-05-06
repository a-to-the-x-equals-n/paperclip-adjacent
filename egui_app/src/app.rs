use std::sync::Arc; 
use egui::{TextEdit, RichText};
#[allow(unused_imports)]
use crate::client::{create_memcell, get_all_memcells, delete_memcell, Memcell};

const LR_PAD: f32 = 24.0;
const MD_PAD: f32 = 18.0;
const SM_PAD: f32 = 10.0;

#[derive(PartialEq, serde::Deserialize, serde::Serialize, Default)]
pub enum AppState {
    #[default]
    Login,
    Main,
    // later: New Memcell
}

#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give default values when deserializing old state
pub struct PaperclipAdjacent {
    login: String,
    heading: String,
    sub_heading: String,
    state: AppState,
    phone: String,
    memcells: Vec<Memcell>,
    selected_memcell: Option<usize>,
}

impl Default for PaperclipAdjacent {
    fn default() -> Self {
        Self {
            login: String::new(),
            heading: "<paperclip adjacent>".to_owned(),
            sub_heading: ".:RAM for your brain:.".to_owned(),
            state: AppState::Login,
            phone: String::new(),
            memcells: Vec::new(),
            selected_memcell: None,
        }
    }
}

impl PaperclipAdjacent {
    // called once before the first frame.
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {

        // --- font style ---
        let mut fonts = egui::FontDefinitions::default();

        fonts.font_data.insert(
            "TerminalMono".to_owned(),
            Arc::new(egui::FontData::from_static(include_bytes!("../assets/ShareTechMono-Regular.ttf"))), 
        );

        // assign it to all styles
        fonts.families.entry(egui::FontFamily::Proportional).or_default().insert(0, "TerminalMono".to_owned());
        fonts.families.entry(egui::FontFamily::Monospace).or_default().insert(0, "TerminalMono".to_owned());

        cc.egui_ctx.set_fonts(fonts);

        // --- font sizes ---
        let mut style = (*cc.egui_ctx.style()).clone();

        style.text_styles = [
            (egui::TextStyle::Heading, egui::FontId::new(26.0, egui::FontFamily::Proportional)),
            (egui::TextStyle::Body, egui::FontId::new(18.0, egui::FontFamily::Proportional)),
            (egui::TextStyle::Monospace, egui::FontId::new(16.0, egui::FontFamily::Monospace)),
            (egui::TextStyle::Button, egui::FontId::new(14.0, egui::FontFamily::Proportional)),
            (egui::TextStyle::Small, egui::FontId::new(10.0, egui::FontFamily::Proportional)),
        ].into();
        cc.egui_ctx.set_style(style);

        // --- theme colors --- 
        let mut visuals = egui::Visuals::dark();

        // core background
        visuals.window_fill = egui::Color32::from_rgb(0x10, 0x0F, 0x1A); // #100f1a 
        visuals.panel_fill  = egui::Color32::from_rgb(0x10, 0x0F, 0x1A); // #100f1a 

        // primary foreground color (text)
        visuals.override_text_color = Some(egui::Color32::from_rgb(0xF5, 0x22, 0x77)); // #f52277

        // widget styles
        visuals.widgets.inactive.bg_fill = egui::Color32::from_rgb(12, 0, 26); //rgb(12, 0, 26) 
        visuals.widgets.hovered.bg_fill = egui::Color32::from_rgb(0xF5, 0x22, 0x77); // #f52277
        visuals.widgets.active.bg_fill = egui::Color32::from_rgb(0x93, 0xE0, 0xE3); // #93e0e3

        visuals.widgets.hovered.bg_stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(0x93, 0xE0, 0xE3)); // #93e0e3
        visuals.widgets.hovered.fg_stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(0x93, 0xE0, 0xE3)); // #93e0e3
        visuals.widgets.active.fg_stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(0x93, 0xE0, 0xE3)); // #93e0e3
        visuals.widgets.active.bg_stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(0x93, 0xE0, 0xE3)); // #93e0e3
        visuals.widgets.inactive.bg_stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(10, 8, 134)); //rgb(10, 8, 134)

        // selection and highlights
        visuals.selection.bg_fill = egui::Color32::from_rgb(0x93, 0xE0, 0xE3); // #f52277
        visuals.selection.stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(0x93, 0xE0, 0xE3)); // #93e0e3
        visuals.hyperlink_color = egui::Color32::from_rgb(0xFF, 0xFF, 0x99); // #ffff99
        visuals.faint_bg_color = egui::Color32::from_rgb(0xFF, 0xFF, 0x99); // #ffff99 

        cc.egui_ctx.set_visuals(visuals);
        
        // load previous app state (if any)
        if let Some(storage) = cc.storage {
            return eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default();
        }

        cc.egui_ctx.send_viewport_cmd(egui::ViewportCommand::Title("//paperclip_adjacent".into()));
        Default::default()
    }
}

impl eframe::App for PaperclipAdjacent {
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    // called each time the UI needs repainting 
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {

        
        match self.state {
            AppState::Login => {

                // --- top panel ---
                egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
                    ui.add_space(MD_PAD);
        
                    ui.vertical_centered(|ui| {
                        ui.heading(&self.heading);
                        ui.add_space(SM_PAD);
                        ui.label(&self.sub_heading);
                    });
        
                    ui.add_space(MD_PAD);
                });
                
                // --- top panel ---
                egui::CentralPanel::default().show(ctx, |ui| {
                    ui.add_space(LR_PAD);
        
                    ui.vertical_centered(|ui| {
                        let hint = RichText::new("phone number")
                            .italics()
                            .color(egui::Color32::from_rgba_unmultiplied(0xF5, 0x22, 0x77, 80));
        
                        ui.add(TextEdit::singleline(&mut self.phone).hint_text(hint));

                        ui.add_space(SM_PAD);

                        if ui.button("[login]").clicked() {
                            let rt = tokio::runtime::Runtime::new().unwrap();
                            match rt.block_on(get_all_memcells()) {
                                Ok(memcells) => self.memcells = memcells,
                                Err(err) => eprintln!("Failed to fetch memcells: {}", err),
                            }

                            self.state = AppState::Main;
                        }
                    });
        
                    ui.add_space(LR_PAD);
                });
            }
        
            AppState::Main => {
                egui::TopBottomPanel::top("main_top").show(ctx, |ui| {
                    ui.horizontal(|ui| {
                        // + button (green)
                        let mut add_btn = egui::Button::new("+").fill(egui::Color32::from_rgb(0, 255, 0));
                        if self.memcells.len() >= 10 {
                            add_btn = add_btn.sense(egui::Sense::hover()); // disables clicking
                        }
                        if ui.add(add_btn).clicked() && self.memcells.len() < 10 {
                            // self.state = AppState::CreateNew;
                        }
        
                        // X button (red)
                        if ui.add(egui::Button::new("X").fill(egui::Color32::from_rgb(255, 0, 0))).clicked() {
                            if let Some(index) = self.selected_memcell {
                                let _ = self.memcells.remove(index);
                                self.selected_memcell = None;
                                // optionally call delete_memcell(...)
                            }
                        }
                    });
                });
        
                egui::CentralPanel::default().show(ctx, |ui| {
                    egui::ScrollArea::vertical().show(ui, |ui| {
                        for (index, cell) in self.memcells.iter().enumerate() {
                            let is_selected = self.selected_memcell == Some(index);
                            let row = egui::SelectableLabel::new(is_selected, format!("[{}] {}", cell.id.unwrap_or(0), cell.task));
        
                            if ui.add(row).clicked() {
                                self.selected_memcell = Some(index);
                            }
                        }
                    });
                });
            }
        }
        
    }
}