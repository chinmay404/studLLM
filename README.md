# StudLLM -AI Chatbot Platform (Langgraph)  - Under Development 

![Screenshot 2025-03-24 011548](https://github.com/user-attachments/assets/08de1351-2ee3-4416-b635-5ff58cca0087)
![Screenshot 2025-03-24 012101](https://github.com/user-attachments/assets/1f28e4d8-6d25-476e-95fb-a8d7279143e4)


An AI-powered chatbot platform designed with a modular architecture to ensure scalability and flexibility. The system consists of two primary servers: a **Flask Server** for frontend and user interactions, and a **FastAPI Server** for handling Large Language Model (LLM) processes. This design allows seamless integration, personalized user experiences, and future expansion to accommodate multiple clients.

## System Architecture

The platform utilizes a modular design, where:

- **Flask Server** handles user interactions and communicates with the backend.
- **FastAPI Server** processes chat inputs and responses, manages user states, and delivers LLM responses based on dynamic user contexts.

This architecture allows for multiple client interactions (web, mobile) without needing to redefine APIs, ensuring scalability for future growth.

## Backend Implementation

### FastAPI Server

- **Chat Processing**: Handles chat input and generates responses Using Langgraph.
- **State Management**: Maintains user states, tailoring the LLM response based on the user's current state (e.g., if the user is new, the chatbot adjusts its approach accordingly).
- **Personalization**: The LLM stores key user information for personalized interactions.
- **Entity Memory Graph**: Planned future development to enhance LLM's context-awareness and memory handling.

### Flask Server

- **Integration**: Connects to the FastAPI backend to display chatbot responses.
- **User Authentication**: Uses Google OAuth 2 for user authentication.
- **UI**: The frontend showcases user interaction through UI screenshots.

## AI Features

### Intelligent Search & Discovery
- **search** – Find what you need instantly.
- **location_finder** – Discover places near you.
- **news_search** – Get the latest news in a snap.
- **places_search** – Explore places around the world.
- **flight_search** – Search for flights with ease.
- **google_scholar_search** – Look up scholarly articles effortlessly.

### User State & Personalization
- **update_state** – Keep track of user states.
- **get_user_state** – Retrieve user status anytime.
- **get_user_state_history** – Access past user interactions.

### User Information Management
- **set_things_about_user** – Save important details about users.
- **get_things_about_user** – Retrieve stored user information.
- **update_things_about_user** – Keep user details up to date.
- **add_single_thing_about_user** – Add new details about a user.
- **check_if_user_has_thing** – Verify if a user has specific information stored.

## Database Implementation

The platform uses **MongoDB** to store:
- User sessions
- Chat history
- User states

This setup ensures that the chatbot retains memory of past interactions and can provide more personalized conversations.

## Frontend Implementation

The frontend of the AI chatbot platform is built using:
- **HTML**
- **CSS**
- **JavaScript**

This stack ensures a responsive and user-friendly interface for seamless chatbot interaction.

## File Structure

The project structure is as follows:


