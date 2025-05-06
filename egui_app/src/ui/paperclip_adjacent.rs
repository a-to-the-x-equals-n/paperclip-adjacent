use crate::client::http::Memcell;
use std::sync::Arc; 

#[derive(PartialEq, serde::Deserialize, serde::Serialize, Default)]
pub enum AppState {
    #[default]
    Login,
    Main,
    CreateNew,
}

#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give default values when deserializing old state
pub struct PaperclipAdjacent {
    pub login: String,
    pub heading: String,
    pub sub_heading: String,
    pub state: AppState,
    pub phone: String,
    pub memcells: Vec<Memcell>,
    pub selected_memcell: Option<usize>,
    pub new_task: String,
    pub creation_error: bool,
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
            new_task: String::new(),
            creation_error: false,
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
            Arc::new(egui::FontData::from_static(include_bytes!("../../assets/ShareTechMono-Regular.ttf"))), 
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
        // visuals.widgets.inactive.bg_stroke = egui::Stroke::new(1.0, egui::Color32::from_rgb(10, 8, 134)); //rgb(10, 8, 134)

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