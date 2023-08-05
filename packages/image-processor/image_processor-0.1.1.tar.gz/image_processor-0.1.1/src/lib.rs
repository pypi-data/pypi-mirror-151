mod processor;

use processor::resize_image;
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn resize(resize_to: f32, input_path: String, output_path: String) {
    resize_image(resize_to, input_path, output_path)
}

/// A Python module implemented in Rust.
#[pymodule]
fn image_processor(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(resize, m)?)?;
    Ok(())
}
