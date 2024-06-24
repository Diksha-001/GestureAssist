import streamlit as st
import app
import cv2

# Custom CSS to change background and heading colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: blue;
    }
    .css-1d391kg h1 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .container {
        background-color: #333;
        padding: 20px;
        color: yellow;
        border: 2px solid #ffffff;
        border-radius: 10px;
    }
    .stApp {
        background-color: black;
    }

    h1 {
        color: yellow;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        padding: 15px 32px; /* Padding */
        text-align: center; /* Center the text */
        text-decoration: none; /* Remove underline */
        display: inline-block; /* Make it inline-block */
        font-size: 16px; /* Font size */
        margin: 4px 2px; /* Margin */
        cursor: pointer; /* Pointer cursor on hover */
        border: none; /* Remove border */
        border-radius: 12px; /* Rounded corners */
        transition-duration: 0.4s; /* Transition effect */
    }
    .stButton button:hover {
        background-color: white; /* White background on hover */
        color: black; /* Black text on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit heading
st.title("Real-time gesture vocalizer")

# Initialize the state for toggling the camera
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False

# Create a button to toggle the interface
if st.button("Toggle Interface"):
    st.session_state.camera_running = not st.session_state.camera_running

# If the camera is running, show the interface and open the camera
if st.session_state.camera_running:
    app.main()  # Your function to start the webcam
else:
    st.write("Camera is off")

# Add a button to close the camera manually
if st.session_state.camera_running and st.button("Close Camera"):
    st.session_state.camera_running = False
    st.write("Camera has been closed")