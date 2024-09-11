import base64

def load_image(image_file):
    """Load a background image and convert it to a Base64 string."""
    try:
        with open(image_file, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        print("Background image file not found.")
        return ""

def get_css(b64_image, image_ext):
    """Generate all CSS including the background image."""
    css = f"""
    <style>
    /* Custom CSS styles for the Laama Chat app */
    [data-testid="stHeader"] {{
        background-color: rgba(14, 17, 23, 0.8) !important;
        color: #ffffff !important;
    }}
    /* Style for the app with background image */
    .stApp {{
        background-image: url('data:image/{image_ext};base64,{b64_image}');
        background-size: cover;
        background-position: center;
        opacity: 0.9;
    }}
    .stApp::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(14, 17, 23, 0.9);
        z-index: -1;
    }}
    /* Styles for chat message avatars */
    [data-testid="chatAvatarIcon-user"] {{
        background-color: #42e59e !important;
    }}
    [data-testid="chatAvatarIcon-assistant"] {{
        background-color: #8f3dd0 !important;
    }}
    /* Style for sidebar */
    [data-testid="stSidebar"] {{
        background-color: rgba(14, 17, 23, 0.8) !important;
    }}
    [data-testid="stSidebar"] hr {{
        background: linear-gradient(90deg, rgba(148, 0, 255, 1) 0%, rgba(0, 255, 148, 1) 100%);
    }}
    /* Style for file uploader */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: rgba(14, 17, 23, 0.6) !important;
    }}
    /* Style the decoration element */
    #stDecoration {{
        background: rgb(148, 0, 255);
        background: linear-gradient(90deg, rgba(148, 0, 255, 1) 0%, rgba(0, 255, 148, 1) 100%);
    }}
    .stDeployButton {{
        visibility: hidden !important;
    }}
    /* Replace the default menu with a hamburger menu */
    #MainMenu {{
        visibility: hidden;
        position: relative;
    }}
    /* Add the hamburger icon in the correct position */
    #MainMenu::before {{
        cursor: pointer;
        content: "\\2630"; /* Unicode for hamburger menu */
        font-size: 1.4em;
        visibility: visible;
        position: absolute;
        top: 50%;
        right: 3px;
        transform: translateY(-50%);
        transition: background-color 0.1s, color 0.1s;
        padding: 8px;
        border-radius: 8px;
        box-sizing: border-box;
    }}
    /* Change background and text color on hover */
    #MainMenu:hover::before {{
        background-color: #262730;
        color: #ffffff;
    }}
    </style>
    """
    return css

def get_full_css(image_file, image_ext):
    """Get the full CSS including background image."""
    b64_image = load_image(image_file)
    return get_css(b64_image, image_ext)
