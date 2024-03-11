# Bookworm Website

Bookworm is a Django web application designed to provide a platform for managing books and user profiles. It offers a user-friendly interface for book enthusiasts to explore, share, and review their favorite books, while also allowing users to create and manage their profiles within the community.

## Features

### User Authentication

Secure user registration and authentication system, allowing users to create accounts, log in, and manage their profiles.

### Book Management

Comprehensive book management functionality, including adding new books, and categorizing them by genre.

### Review System

Enables users to write detailed reviews for books, including ratings and textual feedback.

### Profile Management

User profile management functionality, allowing users to update their information, upload avatars, and view their activity history.

### Moderation

Ability for administrators to moderate book submissions and reviews before they are published to ensure content quality.


## Technology Stack

This website is built using Python, Django, HTML, and CSS. Python powers the backend logic and database management, while Django provides the web framework for building robust applications. HTML, and CSS create an engaging and visually appealing user interface.

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/PolinaScherby/django4site.git
```

2. Change into the project directory:
```
cd django4site
```

3. Create a virtual environment (optional but recommended):
```
python -m venv venv
```
4. Activate the virtual environment:
```
# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```
5. Install the dependencies:
```
pip install -r requirements.txt
```
6. Apply database migrations:
```
python manage.py migrate
```
7. Run the development server:
```
python manage.py runserver
```
8. Open your web browser and visit [http://localhost:8000](http://localhost:8000) to access the website.

## Contributions

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## Contact

If you have any questions, suggestions, or feedback, feel free to reach out.

## License

This project is licensed under the MIT License.

*Created by PScherby*
