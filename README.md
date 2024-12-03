# Palava Paraglide

Palava Paraglide is a Python project that fetches and processes weather and reservation data for paragliding activities at Palava.

## Features

- **Weather Data**: Integrates real-time data from the Holfuy API.
- **Reservation Tracking**: Scrapes reservation data from the Palava website.
- **Data Storage**: Uses SQLite for storing and analyzing data.
- **Secure Configuration**: Utilizes environment variables for API tokens.

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (optional for containerized deployment)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/erik-lukac/palava-paraglide.git
   cd palava-paraglide
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file and add your private token:
     ```
     PRIVATE_TOKEN=your_token_here
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

## Usage

The application fetches weather and reservation data and stores it in an SQLite database (`database.db`).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For questions, contact Erik Lukac at [your_email@example.com].
