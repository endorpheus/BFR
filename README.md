# BFR - Bulk File Renamer

![BFR Logo](icons/robot_icon.png)

BFR (Bulk File Renamer) is a powerful and user-friendly desktop application for renaming multiple files simultaneously. Built with Python and PySide6, BFR offers a graphical interface that makes bulk file renaming operations simple and efficient.

## Features

- **Intuitive GUI**: Easy-to-use interface with file browser for selecting files to rename.
- **Flexible Renaming Options**:
  - Custom rename patterns
  - Add sequential numbering (with customizable padding)
  - Option to keep original file extensions
  - Generate random filenames
- **Conflict Resolution**: Automatically handles filename conflicts to prevent overwriting.
- **File Preview**: See the changes before applying them.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Installation

### Prerequisites

- Python 3.6 or higher
- PySide6

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/endorpheus/BFR.git
   ```

2. Navigate to the project directory:
   ```
   cd BFR
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python BFR.py
   ```

2. Use the file browser to select the files you want to rename.

3. Choose your renaming options:
   - Enter a rename pattern (if desired)
   - Check "Add numbering" to include sequential numbers
   - Adjust number padding if using numbering
   - Check "Keep original file extensions" to preserve file types
   - Check "Generate random filenames" for random name generation

4. Click "Rename Files" to apply the changes.

## Contributing

Contributions to BFR are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped to improve BFR.
- Icon made by [Freepik](https://www.freepik.com) from [www.flaticon.com](https://www.flaticon.com/).

## Contact

For any queries or suggestions, please open an issue on this GitHub repository.

---

BFR - Simplifying bulk file renaming operations.
