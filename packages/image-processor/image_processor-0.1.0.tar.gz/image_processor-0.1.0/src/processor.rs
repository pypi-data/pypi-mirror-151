extern crate image;

use image::imageops::FilterType;
use image::{imageops, GenericImageView};
use std::path::Path;

pub fn resize_image(percentage: f32, input_path: String, output_path: String) {
    // Extract image and compute original dimensions.
    let mut image = image::open(&Path::new(&input_path)).unwrap();
    let image_diamensions = image.dimensions();

    // Compute output diamensions.
    let width: f32 = image_diamensions.0 as f32 * percentage;
    let height: f32 = image_diamensions.1 as f32 * percentage;

    // Resize and save.
    let resized_image =
        imageops::resize(&mut image, width as u32, height as u32, FilterType::Nearest);
    resized_image.save(&output_path).unwrap();
}
