# Project Title

This project processes images from the `input_images` folder by converting them into circular images and then assembling them into a single PDF (`output.pdf`). In short, it takes your regular images, crops and masks them into circles, and neatly arranges them on A4 pages. Useful for pins, stickers, etc.

## Table of Contents

- [Project Title](#project-title)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Explanation](#explanation)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**

   ```bash
   git clone git@github.com:IgorVaryvoda/pin-template-creator.git
   ```

2. **Change to the project directory:**

   ```bash
   cd pin-template-creator
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Make sure your images are placed in the `input_images` folder, then run the script:

```bash
python main.py
```

This will process the images and generate `output.pdf` with all the circular images arranged on A4 pages.

## Explanation

The script (`main.py`) does the following:

- **Image Processing:**
  Opens each image, center-crops it to a square, resizes it based on a 58mm target, and applies a circular mask to create a neat round image.
- **PDF Generation:**
  Arranges these circular images in a grid layout on an A4 page (or multiple pages) and outputs a single PDF file.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository.**
2. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit your changes:**
   ```bash
   git commit -am 'Add some feature'
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/your-feature
   ```
5. **Open a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
