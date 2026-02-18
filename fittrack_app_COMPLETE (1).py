import streamlit as st
import json
import os
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Optional imports for AI workout verification
# These will be imported only when the feature is used
# import cv2
# from PIL import Image
# import base64
# import io

# ============================================
# API CONFIGURATION
# ============================================
# Set these environment variables to enable real APIs
# In Streamlit Cloud: Go to App Settings > Secrets
# Add these keys there

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
USDA_API_KEY = os.environ.get('USDA_API_KEY', '')
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')  # For AI workout verification

# API Mode: 'mock' or 'real'
# Automatically switches to 'real' when API keys are present
API_MODE = 'real' if (OPENWEATHER_API_KEY or USDA_API_KEY or YOUTUBE_API_KEY) else 'mock'

# ============================================

# SST Color Palette
SST_COLORS = {
    'red': '#d32f2f',
    'blue': '#1976d2',
    'gray': '#5a5a5a',
    'light_gray': '#e0e0e0',
    'white': '#ffffff',
    'dark': '#2c2c2c'
}

# Configure page
st.set_page_config(
    page_title="FitTrack - SST Fitness Companion",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for SST styling with dark mode support
st.markdown(f"""
    <style>
    /* Dark mode support - Streamlit uses data-theme attribute */
    [data-theme="dark"] {{
        color-scheme: dark;
    }}
    
    [data-theme="dark"] .stat-card {{
        background: #2d2d2d !important;
        border-left: 5px solid {SST_COLORS['blue']} !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] .stat-card h1,
    [data-theme="dark"] .stat-card h2,
    [data-theme="dark"] .stat-card h3,
    [data-theme="dark"] .stat-card h4 {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] .stat-card p,
    [data-theme="dark"] .stat-card span,
    [data-theme="dark"] .stat-card div {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] h1,
    [data-theme="dark"] h2,
    [data-theme="dark"] h3,
    [data-theme="dark"] h4,
    [data-theme="dark"] h5,
    [data-theme="dark"] h6 {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] p,
    [data-theme="dark"] span,
    [data-theme="dark"] div,
    [data-theme="dark"] label,
    [data-theme="dark"] li,
    [data-theme="dark"] td,
    [data-theme="dark"] th,
    [data-theme="dark"] .stMarkdown,
    [data-theme="dark"] .element-container {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] .stTextInput label,
    [data-theme="dark"] .stNumberInput label,
    [data-theme="dark"] .stSelectbox label,
    [data-theme="dark"] .stRadio label,
    [data-theme="dark"] .stCheckbox label {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] .stAlert {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] .stInfo,
    [data-theme="dark"] .stWarning,
    [data-theme="dark"] .stSuccess,
    [data-theme="dark"] .stError {{
        color: #1a1a1a !important;
    }}
    
    [data-theme="dark"] .stDataFrame {{
        color: #ffffff !important;
    }}
    
    [data-theme="dark"] table {{
        color: #ffffff !important;
    }}
    
    /* Also support prefers-color-scheme for browsers */
    @media (prefers-color-scheme: dark) {{
        body {{
            color: #ffffff !important;
        }}
        
        .stApp {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff !important;
        }}
        
        .stat-card {{
            background: #2d2d2d !important;
            border-left: 5px solid {SST_COLORS['blue']};
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            color: #ffffff !important;
        }}
        
        .stat-card h1,
        .stat-card h2,
        .stat-card h3,
        .stat-card h4 {{
            color: #ffffff !important;
        }}
        
        .stat-card p,
        .stat-card span,
        .stat-card div {{
            color: #ffffff !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #ffffff !important;
        }}
        
        p, span, div, label, li, td, th {{
            color: #ffffff !important;
        }}
        
        .stMarkdown,
        .element-container {{
            color: #ffffff !important;
        }}
        
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label,
        .stRadio label,
        .stCheckbox label {{
            color: #ffffff !important;
        }}
        
        .stDataFrame,
        table {{
            color: #ffffff !important;
        }}
    }}
    
    /* Light mode (default) */
    .stApp {{
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {SST_COLORS['red']} 0%, #b71c1c 100%);
        padding: 30px;
        border-radius: 12px;
        color: white !important;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(211, 47, 47, 0.3);
    }}
    
    .main-header h1,
    .main-header p {{
        color: white !important;
    }}
    
    .stat-card {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {SST_COLORS['blue']};
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }}
    
    .grade-badge {{
        display: inline-block;
        padding: 5px 15px;
        border-radius: 6px;
        font-weight: bold;
        color: white !important;
        margin: 5px;
    }}
    
    .grade-5 {{ background: #4caf50; }}
    .grade-4 {{ background: #8bc34a; }}
    .grade-3 {{ background: #ffc107; color: #000 !important; }}
    .grade-2 {{ background: #ff9800; }}
    .grade-1 {{ background: #f44336; }}
    
    h1, h2, h3 {{ 
        color: {SST_COLORS['dark']};
        font-weight: 700;
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, {SST_COLORS['blue']} 0%, #1565c0 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s;
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
    }}
    
    /* Mobile responsive */
    @media (max-width: 768px) {{
        .main-header {{
            padding: 20px;
        }}
        .stat-card {{
            padding: 15px;
            margin: 8px 0;
        }}
        .stButton>button {{
            padding: 8px 20px;
            font-size: 14px;
        }}
    }}
    
    /* Smooth animations */
    * {{
        transition: background-color 0.3s ease;
    }}
    </style>
""", unsafe_allow_html=True)

# Data storage file
DATA_FILE = 'fittrack_users.json'

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'users_data' not in st.session_state:
    st.session_state.users_data = {}

# Load user data
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save user data
def save_users(users_data):
    with open(DATA_FILE, 'w') as f:
        json.dump(users_data, f, indent=2)

# Load data on startup
st.session_state.users_data = load_users()

# Get current user data
def get_user_data():
    if st.session_state.username in st.session_state.users_data:
        return st.session_state.users_data[st.session_state.username]
    return None

# Update user data
def update_user_data(data):
    st.session_state.users_data[st.session_state.username] = data
    save_users(st.session_state.users_data)

# ============================================
# AI WORKOUT VERIFICATION FUNCTIONS
# ============================================

def verify_workout_with_openai(image, exercise_type):
    """
    Verify workout using OpenAI Vision API
    Returns: (is_valid, feedback, confidence)
    """
    if not OPENAI_API_KEY:
        return None, "OpenAI API key not configured. Please add OPENAI_API_KEY to your Streamlit secrets.", 0
    
    try:
        import requests
        import base64
        import io
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Exercise-specific prompts
        prompts = {
            'pull-up': "Analyze this image. Is the person doing a proper pull-up? Check: 1) Arms fully extended at bottom, 2) Chin above bar at top, 3) No kipping/swinging. Respond with 'VALID' or 'INVALID' followed by specific feedback.",
            'sit-up': "Analyze this image. Is the person doing a proper sit-up? Check: 1) Back flat on ground, 2) Hands behind head or crossed on chest, 3) Shoulders lifting off ground, 4) Controlled movement. Respond with 'VALID' or 'INVALID' followed by specific feedback.",
            'push-up': "Analyze this image. Is the person doing a proper push-up? Check: 1) Body straight line, 2) Elbows at 90 degrees at bottom, 3) Full extension at top, 4) No sagging hips. Respond with 'VALID' or 'INVALID' followed by specific feedback.",
            'squat': "Analyze this image. Is the person doing a proper squat? Check: 1) Feet shoulder-width apart, 2) Knees not past toes, 3) Hips below knees at bottom, 4) Back straight. Respond with 'VALID' or 'INVALID' followed by specific feedback.",
        }
        
        prompt = prompts.get(exercise_type.lower(), f"Analyze if this person is doing a proper {exercise_type}. Respond with 'VALID' or 'INVALID' followed by feedback.")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            feedback = result['choices'][0]['message']['content']
            is_valid = 'VALID' in feedback.upper() and 'INVALID' not in feedback.upper()
            confidence = 85 if is_valid else 75
            
            return is_valid, feedback, confidence
        else:
            return None, f"API Error: {response.status_code} - {response.text}", 0
            
    except Exception as e:
        return None, f"Error: {str(e)}", 0

# ============================================
# NAPFA grading standards
# Format: [Grade A, B, C, D, E cutoffs], reverse scoring (True for time-based)
NAPFA_STANDARDS = {
    12: {
        'm': {
            'SU': [[41,36,32,27,22], False],
            'SBJ': [[202,189,176,163,150], False],
            'SAR': [[39,36,32,28,23], False],
            'PU': [[24,21,16,11,5], False],
            'SR': [[10.4,10.9,11.3,11.7,12.2], True],
            'RUN': [[12.01,13.10,14.20,15.30,16.50], True]
        },
        'f': {
            'SU': [[29,25,21,17,13], False],
            'SBJ': [[167,159,150,141,132], False],
            'SAR': [[39,37,34,30,25], False],
            'PU': [[15,13,10,7,3], False],
            'SR': [[11.5,11.9,12.3,12.7,13.2], True],
            'RUN': [[14.41,15.40,16.40,17.40,18.40], True]
        }
    },
    13: {
        'm': {
            'SU': [[42,38,34,29,25], False],
            'SBJ': [[214,202,189,176,164], False],
            'SAR': [[41,38,34,30,25], False],
            'PU': [[25,22,17,12,7], False],
            'SR': [[10.3,10.7,11.1,11.5,11.9], True],
            'RUN': [[11.31,12.30,13.40,14.50,16.00], True]
        },
        'f': {
            'SU': [[30,26,22,18,14], False],
            'SBJ': [[170,162,153,144,135], False],
            'SAR': [[41,39,36,32,27], False],
            'PU': [[16,13,10,7,3], False],
            'SR': [[11.3,11.7,12.2,12.7,13.2], True],
            'RUN': [[14.31,15.30,16.30,17.30,18.30], True]
        }
    },
    14: {
        'm': {
            'SU': [[42,40,37,33,29], False],
            'SBJ': [[225,216,206,196,186], False],
            'SAR': [[43,40,36,32,27], False],
            'PU': [[26,23,18,13,8], False],
            'SR': [[10.2,10.4,10.8,11.2,11.6], True],
            'RUN': [[11.01,12.00,13.00,14.10,15.20], True]
        },
        'f': {
            'SU': [[30,28,24,20,16], False],
            'SBJ': [[177,169,160,151,142], False],
            'SAR': [[43,41,38,34,29], False],
            'PU': [[16,14,10,7,3], False],
            'SR': [[11.5,11.8,12.2,12.6,13.0], True],
            'RUN': [[14.21,15.20,16.20,17.20,18.20], True]
        }
    },
    15: {
        'm': {
            'SU': [[42,40,37,34,30], False],
            'SBJ': [[237,228,218,208,198], False],
            'SAR': [[45,42,38,34,29], False],
            'PU': [[7,6,5,3,1], False],
            'SR': [[10.2,10.3,10.5,10.9,11.3], True],
            'RUN': [[10.41,11.40,12.40,13.40,14.40], True]
        },
        'f': {
            'SU': [[30,29,25,21,17], False],
            'SBJ': [[182,174,165,156,147], False],
            'SAR': [[45,43,39,35,30], False],
            'PU': [[16,14,10,7,3], False],
            'SR': [[11.3,11.6,12.0,12.4,12.8], True],
            'RUN': [[14.11,15.10,16.10,17.10,18.10], True]
        }
    },
    16: {
        'm': {
            'SU': [[42,40,37,34,31], False],
            'SBJ': [[245,236,226,216,206], False],
            'SAR': [[47,44,40,36,31], False],
            'PU': [[8,7,5,3,1], False],
            'SR': [[10.2,10.3,10.5,10.7,11.1], True],
            'RUN': [[10.31,11.30,12.20,13.20,14.10], True]
        },
        'f': {
            'SU': [[30,29,26,22,18], False],
            'SBJ': [[186,178,169,160,151], False],
            'SAR': [[46,44,40,36,31], False],
            'PU': [[17,14,11,7,3], False],
            'SR': [[11.3,11.5,11.8,12.2,12.6], True],
            'RUN': [[14.01,15.00,16.00,17.00,17.50], True]
        }
    },
    17: {
        'm': {
            'SU': [[42,40,37,34,31], False],
            'SBJ': [[249,240,230,220,210], False],
            'SAR': [[48,45,41,37,32], False],
            'PU': [[9,8,6,4,2], False],
            'SR': [[10.2,10.3,10.5,10.7,10.9], True],
            'RUN': [[10.21,11.10,12.00,12.50,13.40], True]
        },
        'f': {
            'SU': [[30,29,27,23,19], False],
            'SBJ': [[189,181,172,163,154], False],
            'SAR': [[46,44,40,36,32], False],
            'PU': [[17,14,11,7,3], False],
            'SR': [[11.3,11.5,11.8,12.1,12.5], True],
            'RUN': [[14.01,14.50,15.50,16.40,17.30], True]
        }
    },
    18: {
        'm': {
            'SU': [[42,40,37,34,31], False],
            'SBJ': [[251,242,232,222,212], False],
            'SAR': [[48,45,41,37,32], False],
            'PU': [[10,9,7,5,3], False],
            'SR': [[10.2,10.3,10.5,10.7,10.9], True],
            'RUN': [[10.21,11.10,11.50,12.40,13.30], True]
        },
        'f': {
            'SU': [[30,29,27,24,20], False],
            'SBJ': [[192,183,174,165,156], False],
            'SAR': [[46,44,40,36,32], False],
            'PU': [[17,15,11,8,4], False],
            'SR': [[11.3,11.5,11.8,12.1,12.4], True],
            'RUN': [[14.01,14.50,15.40,16.30,17.20], True]
        }
    },
    19: {
        'm': {
            'SU': [[42,40,37,34,31], False],
            'SBJ': [[251,242,232,222,212], False],
            'SAR': [[48,45,41,37,32], False],
            'PU': [[10,9,7,5,3], False],
            'SR': [[10.2,10.3,10.5,10.7,10.9], True],
            'RUN': [[10.21,11.00,11.40,12.30,13.20], True]
        },
        'f': {
            'SU': [[30,29,27,24,21], False],
            'SBJ': [[195,185,174,165,156], False],
            'SAR': [[45,43,39,36,32], False],
            'PU': [[17,15,11,8,5], False],
            'SR': [[11.3,11.5,11.8,12.1,12.4], True],
            'RUN': [[14.21,14.50,15.30,16.20,17.10], True]
        }
    },
    20: {
        'm': {
            'SU': [[39,37,34,31,28], False],
            'SBJ': [[242,234,225,216,207], False],
            'SAR': [[47,44,40,36,32], False],
            'PU': [[10,9,7,5,3], False],
            'SR': [[10.4,10.5,10.7,10.9,11.1], True],
            'RUN': [[10.21,11.00,11.40,12.20,13.00], True]
        },
        'f': {
            'SU': [[28,27,25,23,21], False],
            'SBJ': [[197,186,174,162,150], False],
            'SAR': [[43,41,38,35,31], False],
            'PU': [[17,15,11,8,5], False],
            'SR': [[11.6,11.8,12.1,12.4,12.7], True],
            'RUN': [[15.01,15.30,16.00,16.30,17.00], True]
        }
    }
}

def calc_grade(score, cutoffs, reverse):
    """Calculate grade from score and cutoffs"""
    for i, cutoff in enumerate(cutoffs):
        if reverse:
            if score <= cutoff:
                return 5 - i
        else:
            if score >= cutoff:
                return 5 - i
    return 0

# Body Type Calculator
def calculate_body_type(weight, height):
    """Calculate body type based on BMI and frame"""
    bmi = weight / (height * height)
    
    # Simplified body type classification
    if bmi < 18.5:
        return "Ectomorph", "Naturally lean, fast metabolism, difficulty gaining weight"
    elif bmi < 25:
        if bmi < 21.5:
            return "Ectomorph", "Naturally lean, fast metabolism, difficulty gaining weight"
        else:
            return "Mesomorph", "Athletic build, gains muscle easily, responds well to training"
    elif bmi < 30:
        return "Mesomorph", "Athletic build, gains muscle easily, responds well to training"
    else:
        return "Endomorph", "Larger bone structure, gains weight easily, slower metabolism"

# Recipe API Integration (using TheMealDB - free API)
def search_recipes_by_diet(diet_type, meal_type=""):
    """Search for recipes based on diet goals"""
    # This is a placeholder - TheMealDB API doesn't require auth
    # We'll create a curated list based on diet needs
    
    recipes = {
        "Weight Loss": [
            {"name": "Grilled Chicken Salad", "calories": 350, "protein": "35g", "carbs": "20g", "prep_time": "20 min",
             "ingredients": ["Chicken breast", "Mixed greens", "Cherry tomatoes", "Cucumber", "Olive oil", "Lemon"],
             "instructions": "1. Grill chicken breast until cooked\n2. Chop vegetables\n3. Mix greens with veggies\n4. Slice chicken on top\n5. Drizzle with olive oil and lemon"},
            
            {"name": "Steamed Fish with Vegetables", "calories": 320, "protein": "40g", "carbs": "15g", "prep_time": "25 min",
             "ingredients": ["White fish fillet", "Broccoli", "Carrots", "Ginger", "Soy sauce", "Garlic"],
             "instructions": "1. Season fish with ginger and garlic\n2. Steam fish for 15 min\n3. Steam vegetables separately\n4. Serve with light soy sauce"},
            
            {"name": "Egg White Omelette", "calories": 180, "protein": "20g", "carbs": "8g", "prep_time": "10 min",
             "ingredients": ["Egg whites (4)", "Spinach", "Mushrooms", "Tomatoes", "Black pepper"],
             "instructions": "1. Whisk egg whites\n2. Sauté vegetables\n3. Pour egg whites over veggies\n4. Cook until set"},
            
            {"name": "Greek Yogurt Bowl", "calories": 250, "protein": "18g", "carbs": "30g", "prep_time": "5 min",
             "ingredients": ["Greek yogurt", "Berries", "Chia seeds", "Honey (small amount)", "Almonds"],
             "instructions": "1. Add yogurt to bowl\n2. Top with berries\n3. Sprinkle chia seeds and chopped almonds\n4. Drizzle tiny bit of honey"},
            
            {"name": "Vegetable Soup", "calories": 150, "protein": "8g", "carbs": "25g", "prep_time": "30 min",
             "ingredients": ["Mixed vegetables", "Vegetable broth", "Garlic", "Onion", "Herbs"],
             "instructions": "1. Sauté garlic and onion\n2. Add chopped vegetables\n3. Pour in broth\n4. Simmer 20 minutes\n5. Season with herbs"}
        ],
        
        "Muscle Gain": [
            {"name": "Chicken Rice Bowl", "calories": 650, "protein": "50g", "carbs": "70g", "prep_time": "30 min",
             "ingredients": ["Chicken breast", "Brown rice", "Sweet potato", "Broccoli", "Olive oil"],
             "instructions": "1. Cook brown rice\n2. Grill or bake chicken\n3. Roast sweet potato\n4. Steam broccoli\n5. Combine in bowl with olive oil"},
            
            {"name": "Salmon with Quinoa", "calories": 700, "protein": "45g", "carbs": "60g", "prep_time": "25 min",
             "ingredients": ["Salmon fillet", "Quinoa", "Avocado", "Spinach", "Lemon"],
             "instructions": "1. Cook quinoa\n2. Bake salmon with lemon\n3. Sauté spinach\n4. Serve together with sliced avocado"},
            
            {"name": "Protein Smoothie Bowl", "calories": 550, "protein": "40g", "carbs": "65g", "prep_time": "10 min",
             "ingredients": ["Protein powder", "Banana", "Oats", "Peanut butter", "Milk", "Berries"],
             "instructions": "1. Blend protein powder, banana, oats, milk\n2. Pour into bowl\n3. Top with berries and peanut butter"},
            
            {"name": "Beef Stir Fry", "calories": 600, "protein": "48g", "carbs": "50g", "prep_time": "20 min",
             "ingredients": ["Lean beef", "Mixed vegetables", "Brown rice", "Soy sauce", "Garlic", "Ginger"],
             "instructions": "1. Cook brown rice\n2. Stir fry beef with garlic and ginger\n3. Add vegetables\n4. Season with soy sauce\n5. Serve over rice"},
            
            {"name": "Tuna Pasta", "calories": 620, "protein": "42g", "carbs": "75g", "prep_time": "20 min",
             "ingredients": ["Whole wheat pasta", "Canned tuna", "Cherry tomatoes", "Olive oil", "Garlic", "Basil"],
             "instructions": "1. Cook pasta\n2. Sauté garlic and tomatoes\n3. Add drained tuna\n4. Mix with pasta\n5. Top with fresh basil"}
        ],
        
        "Maintenance": [
            {"name": "Balanced Buddha Bowl", "calories": 500, "protein": "28g", "carbs": "55g", "prep_time": "25 min",
             "ingredients": ["Chickpeas", "Quinoa", "Mixed greens", "Avocado", "Cherry tomatoes", "Tahini"],
             "instructions": "1. Cook quinoa\n2. Roast chickpeas\n3. Arrange greens in bowl\n4. Add quinoa, chickpeas, tomatoes\n5. Top with avocado and tahini"},
            
            {"name": "Chicken Wrap", "calories": 480, "protein": "35g", "carbs": "45g", "prep_time": "15 min",
             "ingredients": ["Whole wheat wrap", "Grilled chicken", "Lettuce", "Tomato", "Hummus", "Cucumber"],
             "instructions": "1. Spread hummus on wrap\n2. Add lettuce and vegetables\n3. Place sliced chicken\n4. Roll tightly and cut"},
            
            {"name": "Egg Fried Rice", "calories": 520, "protein": "22g", "carbs": "62g", "prep_time": "20 min",
             "ingredients": ["Brown rice", "Eggs", "Mixed vegetables", "Soy sauce", "Spring onions"],
             "instructions": "1. Cook rice (preferably day-old)\n2. Scramble eggs separately\n3. Stir fry vegetables\n4. Add rice and eggs\n5. Season with soy sauce"},
            
            {"name": "Grilled Fish Tacos", "calories": 450, "protein": "32g", "carbs": "48g", "prep_time": "20 min",
             "ingredients": ["White fish", "Corn tortillas", "Cabbage", "Lime", "Greek yogurt", "Cilantro"],
             "instructions": "1. Season and grill fish\n2. Warm tortillas\n3. Shred cabbage\n4. Assemble tacos with fish and slaw\n5. Top with yogurt and cilantro"},
            
            {"name": "Oatmeal with Fruits", "calories": 380, "protein": "15g", "carbs": "58g", "prep_time": "10 min",
             "ingredients": ["Oats", "Milk", "Banana", "Berries", "Honey", "Nuts"],
             "instructions": "1. Cook oats with milk\n2. Slice banana\n3. Top with fruits and nuts\n4. Drizzle with honey"}
        ]
    }
    
    return recipes

# AI Helper Functions
def generate_ai_response(question, user_data):
    """Generate AI response based on user question and their data"""
    question_lower = question.lower()
    
    # Analyze user data for context
    has_napfa = len(user_data.get('napfa_history', [])) > 0
    has_bmi = len(user_data.get('bmi_history', [])) > 0
    has_sleep = len(user_data.get('sleep_history', [])) > 0
    
    # NAPFA related questions
    if 'napfa' in question_lower or 'pull' in question_lower or 'sit up' in question_lower or 'run' in question_lower:
        if has_napfa:
            latest = user_data['napfa_history'][-1]
            weak_tests = [test for test, grade in latest['grades'].items() if grade < 3]
            if weak_tests:
                return f"Based on your latest NAPFA test, I see you need work on: {', '.join(weak_tests)}. Check the 'Workout Recommendations' tab for specific exercises! Focus on consistency - train each weak area 3-4x per week."
            else:
                return f"Great NAPFA scores! Your total is {latest['total']} points. To maintain or improve: (1) Keep training all components weekly, (2) Focus on explosive power for jumps, (3) Mix steady runs with sprints, (4) Don't neglect flexibility!"
        else:
            return "Complete a NAPFA test first so I can give you personalized advice! Once you do, I'll analyze your weak areas and create a specific plan."
    
    # BMI/Weight related
    elif 'weight' in question_lower or 'bmi' in question_lower or 'lose' in question_lower or 'gain' in question_lower:
        if has_bmi:
            latest_bmi = user_data['bmi_history'][-1]
            category = latest_bmi['category']
            if category == "Normal":
                return f"Your BMI is {latest_bmi['bmi']} (Normal range). To maintain: eat balanced meals, exercise 4-5x/week, stay hydrated. Focus on building strength and endurance rather than weight change!"
            elif category == "Underweight":
                return "To gain healthy weight: (1) Eat 5-6 small meals daily, (2) Focus on protein + complex carbs, (3) Strength train 3-4x/week, (4) Drink smoothies with banana, oats, peanut butter. Check 'Meal Suggestions' for specific foods!"
            else:
                return "For healthy weight loss: (1) Create small calorie deficit (200-300 cal), (2) Eat lean protein + veggies each meal, (3) Do cardio 4-5x/week, (4) Avoid sugary drinks. Check 'Meal Suggestions' for detailed plan!"
        else:
            return "Calculate your BMI first! Then I can give you personalized nutrition and training advice for your goals."
    
    # Sleep related
    elif 'sleep' in question_lower or 'tired' in question_lower or 'energy' in question_lower:
        if has_sleep:
            sleep_data = user_data['sleep_history']
            avg_hours = sum([s['hours'] + s['minutes']/60 for s in sleep_data]) / len(sleep_data)
            if avg_hours >= 8:
                return f"Your sleep is excellent at {avg_hours:.1f} hours! Keep it consistent. If still tired: check iron levels, reduce screen time before bed, and ensure quality sleep (dark, cool room)."
            else:
                return f"You're averaging {avg_hours:.1f} hours - you need 8-10 hours as a teen! Tips: (1) Set bedtime alarm, (2) No screens 1hr before bed, (3) Same sleep schedule daily, (4) Avoid caffeine after 2pm. Check 'Sleep Insights' for more!"
        else:
            return "Track your sleep for a few days first! Then I can analyze your patterns and give specific advice. Teenagers need 8-10 hours for optimal performance and recovery."
    
    # Strength training
    elif 'strength' in question_lower or 'muscle' in question_lower or 'strong' in question_lower:
        return "To build strength: (1) Focus on compound exercises (push-ups, pull-ups, squats), (2) Progressive overload - increase difficulty weekly, (3) Eat protein after workouts, (4) Rest 48hrs between training same muscles, (5) Start with bodyweight, add resistance gradually. Check 'Custom Workout Plan' for a complete program!"
    
    # Cardio/Endurance
    elif 'cardio' in question_lower or 'endurance' in question_lower or 'stamina' in question_lower:
        return "Build endurance with: (1) Start at comfortable pace - able to talk while running, (2) Gradually increase distance by 10% weekly, (3) Mix steady runs (30-45min) with intervals (sprint 1min, jog 2min x 8), (4) Cross-train with swimming/cycling, (5) Stay hydrated! Aim for 3-4 cardio sessions weekly."
    
    # Diet/Nutrition
    elif 'eat' in question_lower or 'food' in question_lower or 'diet' in question_lower or 'meal' in question_lower:
        return "For athletic performance: (1) Eat breakfast within 1hr of waking, (2) Balance each meal: lean protein + complex carbs + vegetables, (3) Pre-workout: banana + peanut butter, (4) Post-workout: protein + carbs within 1hr, (5) Stay hydrated - 8-10 glasses daily, (6) Limit processed foods and sugar. Check 'Meal Suggestions' for specific plans!"
    
    # Recovery
    elif 'recover' in question_lower or 'sore' in question_lower or 'rest' in question_lower:
        return "Recovery is crucial! (1) Sleep 8-10 hours, (2) Eat protein within 1hr post-workout, (3) Stay hydrated, (4) Active recovery: light walk/swim on rest days, (5) Stretch daily, (6) Ice sore muscles, (7) Rest 1-2 full days/week. Muscle soreness 24-48hrs after workout is normal (DOMS)!"
    
    # Motivation
    elif 'motivat' in question_lower or 'give up' in question_lower or 'hard' in question_lower:
        return "Stay motivated! 💪 (1) Set small, achievable goals, (2) Track progress - celebrate small wins, (3) Find a workout buddy, (4) Mix up your routine to stay interested, (5) Remember your 'why', (6) Progress isn't linear - some weeks are tough, (7) Focus on how you FEEL not just numbers. You've got this!"
    
    # Flexibility
    elif 'stretch' in question_lower or 'flexibility' in question_lower or 'flexib' in question_lower:
        return "Improve flexibility: (1) Stretch AFTER workouts when muscles are warm, (2) Hold each stretch 30-60 seconds, (3) Never bounce, (4) Stretch daily - even on rest days, (5) Focus on hamstrings, hip flexors, shoulders, (6) Try yoga 1-2x/week, (7) Breathe deeply while stretching. Flexibility improves injury prevention and performance!"
    
    # Injury
    elif 'injur' in question_lower or 'pain' in question_lower or 'hurt' in question_lower:
        return "⚠️ If you have pain (not soreness): (1) STOP that activity immediately, (2) Rest and ice the area, (3) See a doctor/physiotherapist if pain persists, (4) Don't train through pain - it makes injuries worse. Prevention: warm up properly, increase intensity gradually, use proper form, rest adequately. Your health comes first!"
    
    # Default helpful response
    else:
        return "I can help with: NAPFA training, strength building, cardio/endurance, nutrition/meals, weight management, sleep optimization, recovery, flexibility, injury prevention, and motivation! Try asking about any of these topics, or check the other tabs for detailed insights based on your data. What specific aspect of fitness would you like to know about?"

def generate_workout_exercises(focus, location, duration_min, fitness_level):
    """Generate exercises based on workout parameters"""
    exercises = []
    
    # Adjust sets/reps based on fitness level
    if fitness_level == "Beginner":
        sets, reps = 2, 10
        rest = "60-90 seconds"
    elif fitness_level == "Intermediate":
        sets, reps = 3, 12
        rest = "45-60 seconds"
    else:  # Advanced
        sets, reps = 4, 15
        rest = "30-45 seconds"
    
    # Generate exercises based on focus
    if focus in ["Upper Body Strength", "Strength Training"]:
        if location == "Home (no equipment)":
            exercises = [
                f"Push-ups: {sets} sets x {reps} reps (rest {rest})",
                f"Diamond push-ups: {sets} sets x {reps-5} reps",
                f"Pike push-ups: {sets} sets x {reps-3} reps",
                f"Tricep dips (chair): {sets} sets x {reps} reps",
                f"Plank shoulder taps: {sets} sets x {reps*2} taps"
            ]
        elif location == "Gym" or location == "School":
            exercises = [
                f"Pull-ups/Chin-ups: {sets} sets x max reps",
                f"Push-ups: {sets} sets x {reps+5} reps",
                f"Dumbbell shoulder press: {sets} sets x {reps} reps",
                f"Bent-over rows: {sets} sets x {reps} reps",
                f"Dips: {sets} sets x {reps} reps"
            ]
        else:
            exercises = [
                f"Pull-ups (bar/tree): {sets} sets x max reps",
                f"Push-ups: {sets} sets x {reps} reps",
                f"Bench dips: {sets} sets x {reps} reps",
                f"Inverted rows: {sets} sets x {reps} reps"
            ]
    
    elif focus in ["Lower Body & Core", "Lower Body"]:
        exercises = [
            f"Squats: {sets} sets x {reps+5} reps",
            f"Lunges: {sets} sets x {reps} reps each leg",
            f"Glute bridges: {sets} sets x {reps+5} reps",
            f"Calf raises: {sets} sets x {reps+10} reps",
            f"Plank: {sets} sets x 30-60 seconds",
            f"Russian twists: {sets} sets x {reps*2} total reps",
            f"Bicycle crunches: {sets} sets x {reps+5} reps"
        ]
    
    elif focus in ["Cardio & Endurance", "Cardio Training"]:
        if duration_min >= 60:
            exercises = [
                "Running: 30 minutes steady pace",
                "Interval sprints: 8 rounds (1 min sprint, 2 min jog)",
                "Jump rope: 3 sets x 3 minutes",
                "High knees: 3 sets x 1 minute",
                "Burpees: 3 sets x 12 reps"
            ]
        else:
            exercises = [
                "Running: 15-20 minutes steady pace",
                "Interval sprints: 6 rounds (1 min sprint, 90 sec jog)",
                "Jumping jacks: 3 sets x 50 reps",
                "Mountain climbers: 3 sets x 30 seconds"
            ]
    
    else:  # Full Body
        exercises = [
            f"Squats: {sets} sets x {reps} reps",
            f"Push-ups: {sets} sets x {reps} reps",
            f"Lunges: {sets} sets x {reps} reps each leg",
            f"Plank: {sets} sets x 45 seconds",
            f"Burpees: {sets} sets x {reps-2} reps",
            f"Sit-ups: {sets} sets x {reps+5} reps",
            f"Jump squats: {sets} sets x {reps} reps"
        ]
    
    return exercises

# Login/Registration Page
def login_page():
    st.markdown('<div class="main-header"><h1>🏋️ FitTrack</h1><p>School of Science and Technology Singapore</p><p>Your Personal Fitness Companion</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Sign In", "Create Account", "Reset Password"])
    
    with tab1:
        st.subheader("Welcome Back!")
        
        # Google-style login
        email = st.text_input("Email Address", key="login_email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Sign In", key="login_btn", type="primary"):
            # Find user by email
            user_found = None
            for username, data in st.session_state.users_data.items():
                if data.get('email', '').lower() == email.lower():
                    # Simple password check (in real app, this would be hashed)
                    if data.get('password') == password:
                        user_found = username
                        break
            
            if user_found:
                st.session_state.logged_in = True
                st.session_state.username = user_found
                st.success("✅ Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid email or password")
        
        st.write("")
        st.info("💡 **Students:** Use any email | **Teachers:** Use any email")
        st.write("")
        
        # Password reset link
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Forgot Password?", key="forgot_link"):
                st.info("Go to 'Reset Password' tab")
    
    with tab2:
        st.subheader("Create Your Account")
        
        # Role selection at the top
        st.write("### Select Your Role")
        role = st.radio("I am a:", ["Student", "Teacher"], key="reg_role", horizontal=True)
        
        st.write("---")
        st.write("### Account Information")
        
        col1, col2 = st.columns(2)
        with col1:
            new_email = st.text_input("Email Address", key="reg_email", 
                                     placeholder="student@example.com" if role == "Student" else "teacher@sst.edu.sg")
            full_name = st.text_input("Full Name", key="reg_name")
        
        with col2:
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
            
            # Password strength indicator
            if new_password:
                strength = 0
                if len(new_password) >= 8:
                    strength += 1
                if any(c.isupper() for c in new_password):
                    strength += 1
                if any(c.isdigit() for c in new_password):
                    strength += 1
                if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in new_password):
                    strength += 1
                
                strength_colors = {0: "#f44336", 1: "#ff9800", 2: "#ffc107", 3: "#8bc34a", 4: "#4caf50"}
                strength_labels = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong"}
                
                st.markdown(f'<div style="background: {strength_colors[strength]}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; margin-top: -10px;">Password Strength: {strength_labels[strength]}</div>', unsafe_allow_html=True)
                
                if strength < 2:
                    st.caption("💡 Use 8+ chars, uppercase, numbers, and symbols for better security")
        
        st.write("### Personal Details")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=12, max_value=100 if role == "Teacher" else 18, 
                                 value=14 if role == "Student" else 30, key="reg_age")
            gender = st.selectbox("Gender", ["Male", "Female"], key="reg_gender")
        
        with col2:
            if role == "Student":
                school = st.text_input("School (Optional)", value="School of Science and Technology", key="reg_school")
                class_name = st.text_input("Class (Optional)", placeholder="e.g., 3-Integrity", key="reg_class")
            else:
                school = "School of Science and Technology"
                st.text_input("School", value=school, disabled=True, key="reg_school_teacher")
                department = st.text_input("Department (Optional)", placeholder="e.g., PE Department", key="reg_department")
        
        if role == "Student":
            st.write("### 🏠 House Selection")
            st.write("Choose your house to earn points for your team!")
            
            house_options = {
                "🟡 Yellow House": "yellow",
                "🔴 Red House": "red",
                "🔵 Blue House": "blue",
                "🟢 Green House": "green",
                "⚫ Black House": "black"
            }
            
            selected_house_display = st.selectbox("Select Your House", list(house_options.keys()), key="reg_house")
            selected_house = house_options[selected_house_display]
            
            st.info("💡 Every hour you exercise earns 1 point for your house!")
        
        if role == "Student":
            st.write("### Privacy Settings")
            show_on_leaderboards = st.checkbox("Show me on public leaderboards", value=False, key="reg_leaderboard")
            
            st.write("### Join a Class (Optional)")
            class_code = st.text_input("Class Code", placeholder="Enter code from your teacher", key="reg_class_code")
        
        if st.button("Create Account", key="register_btn", type="primary"):
            # Validation
            if not new_email or not full_name or not new_password:
                st.error("Please fill in all required fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            elif any(data.get('email', '').lower() == new_email.lower() for data in st.session_state.users_data.values()):
                st.error("Email already registered")
            else:
                # Generate username from email
                username = new_email.split('@')[0].replace('.', '_')
                
                # Ensure username is unique
                original_username = username
                counter = 1
                while username in st.session_state.users_data:
                    username = f"{original_username}{counter}"
                    counter += 1
                
                # Create account based on role
                if role == "Student":
                    st.session_state.users_data[username] = {
                        'email': new_email.lower(),
                        'password': new_password,  # In production, this should be hashed
                        'role': 'student',
                        'name': full_name,
                        'age': age,
                        'gender': 'm' if gender == "Male" else 'f',
                        'school': school,
                        'class': class_name,
                        'house': selected_house,
                        'house_points_contributed': 0,
                        'total_workout_hours': 0,
                        'show_on_leaderboards': show_on_leaderboards,
                        'created': datetime.now().isoformat(),
                        'bmi_history': [],
                        'napfa_history': [],
                        'sleep_history': [],
                        'exercises': [],
                        'goals': [],
                        'schedule': [],
                        'saved_workout_plan': None,
                        'friends': [],
                        'friend_requests': [],
                        'badges': [],
                        'level': 'Novice',
                        'total_points': 0,
                        'last_login': datetime.now().isoformat(),
                        'login_streak': 0,
                        'active_challenges': [],
                        'completed_challenges': [],
                        'teacher_class': None  # Will be set when joining a class
                    }
                    
                    # Join class if code provided
                    if class_code:
                        # Find teacher with this class code
                        for teacher_username, teacher_data in st.session_state.users_data.items():
                            if teacher_data.get('role') == 'teacher' and teacher_data.get('class_code') == class_code:
                                # Check class size limit
                                current_students = teacher_data.get('students', [])
                                if len(current_students) >= 30:
                                    st.warning(f"Class is full (30/30 students). Contact your teacher.")
                                else:
                                    st.session_state.users_data[username]['teacher_class'] = teacher_username
                                    teacher_data['students'].append(username)
                                    st.success(f"✅ Joined {teacher_data['name']}'s class!")
                                break
                        else:
                            st.warning("Invalid class code. You can join a class later.")
                
                else:  # Teacher
                    # Generate unique class code
                    import random
                    import string
                    class_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    
                    st.session_state.users_data[username] = {
                        'email': new_email.lower(),
                        'password': new_password,
                        'role': 'teacher',
                        'name': full_name,
                        'age': age,
                        'gender': 'm' if gender == "Male" else 'f',
                        'school': school,
                        'department': department,
                        'created': datetime.now().isoformat(),
                        'class_code': class_code,
                        'students': [],
                        'classes_created': [],
                        'last_login': datetime.now().isoformat(),
                        # Fitness tracking (teachers can track fitness too!)
                        'house': None,
                        'house_points_contributed': 0,
                        'total_workout_hours': 0,
                        'show_on_leaderboards': False,
                        'bmi_history': [],
                        'napfa_history': [],
                        'sleep_history': [],
                        'exercises': [],
                        'goals': [],
                        'schedule': [],
                        'saved_workout_plan': None,
                        'friends': [],
                        'friend_requests': [],
                        'badges': [],
                        'level': 'Novice',
                        'total_points': 0,
                        'login_streak': 0,
                        'groups': [],
                        'group_invites': [],
                        'smart_goals': []
                    }
                
                save_users(st.session_state.users_data)
                st.success("✅ Account created successfully! Please sign in.")
                
                if role == "Teacher":
                    st.info(f"📝 Your Class Code: **{class_code}** - Share this with your students!")
                
                st.balloons()
                time.sleep(2)
                save_users(st.session_state.users_data)
                st.success("✅ Account created! Please sign in.")
                st.rerun()
    
    with tab3:
        st.subheader("🔐 Reset Password")
        st.write("Enter your email to reset your password")
        
        reset_email = st.text_input("Email Address", key="reset_email", placeholder="your.email@example.com")
        
        if st.button("Send Reset Instructions", key="reset_btn", type="primary"):
            # Find user by email
            user_found = None
            username_found = None
            for username, data in st.session_state.users_data.items():
                if data.get('email', '').lower() == reset_email.lower():
                    user_found = data
                    username_found = username
                    break
            
            if user_found:
                st.success("✅ Account found!")
                st.write("")
                st.write("### Set New Password")
                
                new_pwd = st.text_input("New Password", type="password", key="new_pwd")
                confirm_new_pwd = st.text_input("Confirm New Password", type="password", key="confirm_new_pwd")
                
                if st.button("Reset Password", key="do_reset"):
                    if not new_pwd or len(new_pwd) < 6:
                        st.error("Password must be at least 6 characters")
                    elif new_pwd != confirm_new_pwd:
                        st.error("Passwords do not match")
                    else:
                        # Update password
                        st.session_state.users_data[username_found]['password'] = new_pwd
                        save_users(st.session_state.users_data)
                        st.success("✅ Password reset successful! Please sign in with your new password.")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
            else:
                st.error("❌ Email not found. Please check your email or create a new account.")
        
        st.write("")
        st.info("💡 **Note:** In production, this would send a secure reset link to your email. For now, you can reset directly here.")

# BMI Calculator
def bmi_calculator():
    st.header("📊 BMI Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=60.0, step=0.1)
    with col2:
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.65, step=0.01)
    
    if st.button("Calculate BMI"):
        bmi = weight / (height * height)
        
        if bmi < 18.5:
            category = "Underweight"
            color = "#2196f3"
        elif bmi < 25:
            category = "Normal"
            color = "#4caf50"
        elif bmi < 30:
            category = "Overweight"
            color = "#ff9800"
        else:
            category = "Obesity"
            color = "#f44336"
        
        # Save to history
        user_data = get_user_data()
        user_data['bmi_history'].append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'bmi': round(bmi, 2),
            'weight': weight,
            'height': height,
            'category': category
        })
        update_user_data(user_data)
        
        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="stat-card"><h2 style="color: {color};">BMI: {bmi:.2f}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><h2 style="color: {SST_COLORS["gray"]};">Category: {category}</h2></div>', unsafe_allow_html=True)
        
        st.info(f"📈 You have {len(user_data['bmi_history'])} BMI record(s) saved.")
        
        # Show history chart if there's data
        if len(user_data['bmi_history']) > 1:
            df = pd.DataFrame(user_data['bmi_history'])
            df_chart = df.set_index('date')['bmi']
            st.subheader("BMI History")
            st.line_chart(df_chart)

# NAPFA Test Calculator
def napfa_calculator():
    st.header("🏃 NAPFA Test Calculator")
    
    user_data = get_user_data()
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"], 
                            index=0 if user_data['gender'] == 'm' else 1)
    with col2:
        age = st.number_input("Age", min_value=12, max_value=16, value=user_data['age'])
    
    if age not in NAPFA_STANDARDS:
        st.error("Age must be between 12-16")
        return
    
    gender_key = 'm' if gender == "Male" else 'f'
    
    st.subheader("Enter Your Scores")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        situps = st.number_input("Sit-ups (1 min)", min_value=0, max_value=100, value=30)
        broadjump = st.number_input("Standing Broad Jump (cm)", min_value=0, max_value=300, value=200)
    with col2:
        sitreach = st.number_input("Sit and Reach (cm)", min_value=0, max_value=100, value=35)
        pullups = st.number_input("Pull-ups (30 sec)", min_value=0, max_value=50, value=8)
    with col3:
        shuttlerun = st.number_input("Shuttle Run (seconds)", min_value=5.0, max_value=20.0, value=10.5, step=0.1)
        run_time = st.text_input("2.4km Run (min:sec)", value="10:30")
    
    if st.button("Calculate Grades"):
        try:
            # Convert run time
            time_parts = run_time.split(':')
            run_minutes = int(time_parts[0]) + int(time_parts[1]) / 60
            
            standards = NAPFA_STANDARDS[age][gender_key]
            
            scores = {
                'SU': situps,
                'SBJ': broadjump,
                'SAR': sitreach,
                'PU': pullups,
                'SR': shuttlerun,
                'RUN': run_minutes
            }
            
            test_names = {
                'SU': 'Sit-Ups',
                'SBJ': 'Standing Broad Jump',
                'SAR': 'Sit and Reach',
                'PU': 'Pull-Ups',
                'SR': 'Shuttle Run',
                'RUN': '2.4km Run'
            }
            
            grades = {}
            total = 0
            min_grade = 5
            
            for test in scores:
                grade = calc_grade(scores[test], standards[test][0], standards[test][1])
                grades[test] = grade
                total += grade
                min_grade = min(min_grade, grade)
            
            # Determine medal
            if total >= 21 and min_grade >= 3:
                medal = "🥇 Gold"
                medal_color = "#FFD700"
            elif total >= 15 and min_grade >= 2:
                medal = "🥈 Silver"
                medal_color = "#C0C0C0"
            elif total >= 9 and min_grade >= 1:
                medal = "🥉 Bronze"
                medal_color = "#CD7F32"
            else:
                medal = "No Medal"
                medal_color = SST_COLORS['gray']
            
            # Save to history
            user_data['napfa_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'age': age,
                'gender': gender_key,
                'scores': scores,
                'grades': grades,
                'total': total,
                'medal': medal
            })
            update_user_data(user_data)
            
            # Display results
            st.markdown("### Results")
            
            results_data = []
            for test, grade in grades.items():
                results_data.append({
                    'Test': test_names[test],
                    'Score': scores[test],
                    'Grade': grade
                })
            
            df = pd.DataFrame(results_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="stat-card"><h2 style="color: {SST_COLORS["blue"]};">Total: {total}</h2></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="stat-card"><h2 style="color: {medal_color};">Medal: {medal}</h2></div>', unsafe_allow_html=True)
            
            st.info(f"📈 You have {len(user_data['napfa_history'])} NAPFA test(s) saved.")
            
        except Exception as e:
            st.error(f"Error calculating grades: {str(e)}")

# Sleep Tracker
def sleep_tracker():
    st.header("😴 Sleep Tracker")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep_start = st.time_input("Sleep Start Time", value=None)
    with col2:
        sleep_end = st.time_input("Wake Up Time", value=None)
    
    if st.button("Calculate Sleep"):
        if sleep_start and sleep_end:
            # Convert to datetime for calculation
            start = datetime.combine(datetime.today(), sleep_start)
            end = datetime.combine(datetime.today(), sleep_end)
            
            # Handle overnight sleep
            if end < start:
                end += timedelta(days=1)
            
            diff = end - start
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            
            if hours >= 8:
                quality = "Excellent"
                color = "#4caf50"
                advice = "✓ Great job! You're getting enough sleep."
            elif hours >= 7:
                quality = "Good"
                color = "#8bc34a"
                advice = "👍 Good sleep duration. Try to get a bit more."
            elif hours >= 6:
                quality = "Fair"
                color = "#ff9800"
                advice = "⚠️ You need more sleep. Aim for 8-10 hours per night."
            else:
                quality = "Poor"
                color = "#f44336"
                advice = "⚠️ You need more sleep. Aim for 8-10 hours per night."
            
            # Save to history
            user_data = get_user_data()
            user_data['sleep_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'sleep_start': str(sleep_start),
                'sleep_end': str(sleep_end),
                'hours': hours,
                'minutes': minutes,
                'quality': quality
            })
            update_user_data(user_data)
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="stat-card"><h2 style="color: {color};">Sleep Duration: {hours}h {minutes}m</h2></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="stat-card"><h2 style="color: {SST_COLORS["blue"]};">Quality: {quality}</h2></div>', unsafe_allow_html=True)
            
            st.info(advice)
            st.info(f"📈 You have {len(user_data['sleep_history'])} sleep record(s) saved.")
            
            # Show history chart if there's data
            if len(user_data['sleep_history']) > 1:
                df = pd.DataFrame(user_data['sleep_history'])
                df['total_hours'] = df['hours'] + df['minutes'] / 60
                df_chart = df.set_index('date')['total_hours']
                st.subheader("Sleep Duration History (hours)")
                st.line_chart(df_chart)
        else:
            st.error("Please enter both sleep start and end times")

# Exercise Logger
def exercise_logger():
    st.header("💪 Workout Logger")
    
    user_data = get_user_data()
    has_openai = bool(OPENAI_API_KEY)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "⏱️ Log Workout (Timer + Verify)", 
        "🏃 Running & Steps Tracker",
        "📊 Workout History"
    ])
    
    with tab1:
        st.subheader("⏱️ Log Your Workout with Timer & AI Verification")
        
        # Show verification status
        if has_openai:
            st.success("✅ **AI Verification Active** - Upload a photo to verify and earn points!")
        else:
            st.info("💡 **Mock Mode** - You can still log workouts! Points awarded without verification for testing.")
        
        st.write("---")
        
        # Exercise selection
        col1, col2 = st.columns(2)
        
        with col1:
            exercise_type = st.selectbox(
                "Exercise Type",
                ["Pull-Ups", "Sit-Ups", "Push-Ups", "Squats", "Plank", 
                 "Jumping Jacks", "Burpees", "Mountain Climbers", 
                 "Lunges", "Bicycle Crunches", "Other"],
                help="Select your exercise"
            )
        
        with col2:
            intensity = st.selectbox("Intensity", ["Low", "Medium", "High"])
        
        st.write("---")
        
        # INTEGRATED TIMER SECTION
        st.write("### ⏱️ Workout Timer")
        
        # Timer type selection
        timer_col1, timer_col2 = st.columns(2)
        
        with timer_col1:
            timer_type = st.radio(
                "Timer Type",
                ["⏱️ Simple Timer", "🔄 Interval Timer (HIIT)"],
                horizontal=True
            )
        
        if timer_type == "⏱️ Simple Timer":
            with timer_col2:
                preset_time = st.selectbox(
                    "Preset Duration",
                    ["30 seconds", "1 minute", "2 minutes", "5 minutes", 
                     "10 minutes", "15 minutes", "20 minutes", "30 minutes", "Custom"],
                    index=2
                )
            
            if preset_time == "Custom":
                custom_minutes = st.number_input("Minutes", min_value=0, max_value=120, value=5)
                custom_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)
                total_seconds = custom_minutes * 60 + custom_seconds
            else:
                time_map = {
                    "30 seconds": 30,
                    "1 minute": 60,
                    "2 minutes": 120,
                    "5 minutes": 300,
                    "10 minutes": 600,
                    "15 minutes": 900,
                    "20 minutes": 1200,
                    "30 minutes": 1800
                }
                total_seconds = time_map[preset_time]
            
            # Initialize timer state
            if 'timer_running' not in st.session_state:
                st.session_state.timer_running = False
            if 'timer_seconds_left' not in st.session_state:
                st.session_state.timer_seconds_left = total_seconds
            if 'timer_total' not in st.session_state:
                st.session_state.timer_total = total_seconds
            if 'timer_start_time' not in st.session_state:
                st.session_state.timer_start_time = None
            
            # Calculate actual time remaining if running
            if st.session_state.timer_running and st.session_state.timer_start_time:
                elapsed = time.time() - st.session_state.timer_start_time
                st.session_state.timer_seconds_left = max(0, st.session_state.timer_total - int(elapsed))
                
                # Check if timer finished
                if st.session_state.timer_seconds_left == 0:
                    st.session_state.timer_running = False
                    st.session_state.timer_start_time = None
            
            # Display timer
            mins = st.session_state.timer_seconds_left // 60
            secs = st.session_state.timer_seconds_left % 60
            
            # Color based on time remaining
            if st.session_state.timer_seconds_left == 0 and st.session_state.timer_total > 0:
                timer_color = "#4caf50"  # Green when done
                status_text = "Complete!"
            elif st.session_state.timer_running:
                timer_color = "#ff9800"  # Orange when running
                status_text = "Running..."
            else:
                timer_color = "#1976d2"  # Blue when ready
                status_text = "Ready"
            
            st.markdown(f"""
            <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, {timer_color} 0%, {timer_color}dd 100%); 
                        border-radius: 15px; color: white; margin: 20px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.3);'>
                <h1 style='font-size: 4em; margin: 0; font-weight: bold;'>{mins:02d}:{secs:02d}</h1>
                <p style='font-size: 1.5em; margin-top: 10px;'>{status_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-refresh script when timer is running
            if st.session_state.timer_running:
                st.markdown("""
                <script>
                    setTimeout(function() {
                        window.parent.location.reload();
                    }, 1000);
                </script>
                """, unsafe_allow_html=True)
            
            # Show completion message
            if st.session_state.timer_seconds_left == 0 and st.session_state.timer_total > 0 and not st.session_state.timer_running:
                st.success("🎉 Timer Complete! Great workout!")
                st.balloons()
            
            # Timer controls
            timer_col1, timer_col2, timer_col3 = st.columns(3)
            
            with timer_col1:
                if st.button("▶️ Start", use_container_width=True, disabled=st.session_state.timer_running):
                    st.session_state.timer_running = True
                    st.session_state.timer_seconds_left = total_seconds
                    st.session_state.timer_total = total_seconds
                    st.session_state.timer_start_time = time.time()
                    st.rerun()
            
            with timer_col2:
                if st.button("⏸️ Pause", use_container_width=True, disabled=not st.session_state.timer_running):
                    st.session_state.timer_running = False
                    st.session_state.timer_total = st.session_state.timer_seconds_left  # Save remaining time
                    st.session_state.timer_start_time = None
                    st.rerun()
            
            with timer_col3:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.timer_running = False
                    st.session_state.timer_seconds_left = total_seconds
                    st.session_state.timer_total = total_seconds
                    st.session_state.timer_start_time = None
                    st.rerun()
        
        else:  # Interval Timer
            with timer_col2:
                st.write("")
            
            interval_col1, interval_col2, interval_col3 = st.columns(3)
            
            with interval_col1:
                work_time = st.number_input("Work (seconds)", min_value=5, max_value=300, value=30, key="work_time")
            
            with interval_col2:
                rest_time = st.number_input("Rest (seconds)", min_value=5, max_value=300, value=10, key="rest_time")
            
            with interval_col3:
                rounds = st.number_input("Rounds", min_value=1, max_value=50, value=8, key="rounds")
            
            # Initialize interval timer state
            if 'interval_running' not in st.session_state:
                st.session_state.interval_running = False
            if 'interval_current_round' not in st.session_state:
                st.session_state.interval_current_round = 1
            if 'interval_is_work' not in st.session_state:
                st.session_state.interval_is_work = True
            if 'interval_seconds_left' not in st.session_state:
                st.session_state.interval_seconds_left = work_time
            if 'interval_start_time' not in st.session_state:
                st.session_state.interval_start_time = None
            
            # Calculate time remaining
            if st.session_state.interval_running and st.session_state.interval_start_time:
                elapsed = time.time() - st.session_state.interval_start_time
                current_phase_duration = work_time if st.session_state.interval_is_work else rest_time
                st.session_state.interval_seconds_left = max(0, current_phase_duration - int(elapsed))
                
                # Check if phase is done
                if st.session_state.interval_seconds_left == 0:
                    if st.session_state.interval_is_work:
                        # Work done, switch to rest
                        st.session_state.interval_is_work = False
                        st.session_state.interval_seconds_left = rest_time
                        st.session_state.interval_start_time = time.time()
                    else:
                        # Rest done, go to next round or finish
                        if st.session_state.interval_current_round < rounds:
                            st.session_state.interval_current_round += 1
                            st.session_state.interval_is_work = True
                            st.session_state.interval_seconds_left = work_time
                            st.session_state.interval_start_time = time.time()
                        else:
                            # All rounds complete!
                            st.session_state.interval_running = False
                            st.session_state.interval_start_time = None
                
                # Auto-refresh every second
                if st.session_state.interval_running:
                    time.sleep(1)
                    st.rerun()
            
            # Display
            total_interval_time = (work_time + rest_time) * rounds
            total_mins = total_interval_time // 60
            total_secs = total_interval_time % 60
            
            # Current phase display
            phase_text = "WORK 💪" if st.session_state.interval_is_work else "REST 😌"
            phase_color = "#ff5722" if st.session_state.interval_is_work else "#4caf50"
            
            if not st.session_state.interval_running:
                phase_color = "#1976d2"
                phase_text = "READY"
            
            st.markdown(f"""
            <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, {phase_color} 0%, {phase_color}dd 100%); 
                        border-radius: 15px; color: white; margin: 20px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.3);'>
                <h2 style='margin: 0;'>Round {st.session_state.interval_current_round}/{rounds}</h2>
                <h1 style='font-size: 4em; margin: 10px 0; font-weight: bold;'>{st.session_state.interval_seconds_left}</h1>
                <p style='font-size: 1.8em; margin: 0; font-weight: bold;'>{phase_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"⏱️ Total workout time: {total_mins} min {total_secs} sec")
            
            # Check if complete
            if not st.session_state.interval_running and st.session_state.interval_current_round == rounds and not st.session_state.interval_is_work:
                st.success("🎉 HIIT Workout Complete! Amazing job!")
                st.balloons()
            
            # Controls
            hiit_col1, hiit_col2, hiit_col3 = st.columns(3)
            
            with hiit_col1:
                if st.button("▶️ Start HIIT", type="primary", use_container_width=True, disabled=st.session_state.interval_running):
                    st.session_state.interval_running = True
                    st.session_state.interval_current_round = 1
                    st.session_state.interval_is_work = True
                    st.session_state.interval_seconds_left = work_time
                    st.session_state.interval_start_time = time.time()
                    st.session_state.timer_total = total_interval_time  # Save for points calculation
                    st.rerun()
            
            with hiit_col2:
                if st.button("⏸️ Pause HIIT", use_container_width=True, disabled=not st.session_state.interval_running):
                    st.session_state.interval_running = False
                    st.session_state.interval_start_time = None
                    st.rerun()
            
            with hiit_col3:
                if st.button("🔄 Reset HIIT", use_container_width=True):
                    st.session_state.interval_running = False
                    st.session_state.interval_current_round = 1
                    st.session_state.interval_is_work = True
                    st.session_state.interval_seconds_left = work_time
                    st.session_state.interval_start_time = None
                    st.rerun()
        
        # Calculate duration from timer
        workout_duration_minutes = st.session_state.timer_total / 60 if 'timer_total' in st.session_state and st.session_state.timer_total > 0 else 0
        
        # Show current user stats
        st.write("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Your Total Points", user_data.get('total_points', 0))
        with col2:
            st.metric("Your Level", user_data.get('level', 'Novice'))
        with col3:
            st.metric("House Points", f"{user_data.get('house_points_contributed', 0):.1f}")
        
        st.write("---")
        
        # AI Verification Section
        st.write("### 📸 Upload Photo for Verification")
        
        # Option to manually enter duration if timer not used
        if workout_duration_minutes < 0.1:
            st.warning("⚠️ Timer not used. Please enter duration manually:")
            manual_duration = st.number_input(
                "Workout Duration (minutes)",
                min_value=1,
                max_value=180,
                value=10,
                help="How long did you exercise?"
            )
            workout_duration_minutes = manual_duration
        else:
            st.success(f"✅ Timer duration captured: {workout_duration_minutes:.1f} minutes")
        
        if has_openai:
            st.info("""
            **Photo Requirements:**
            - Show full body or exercise area
            - Good lighting
            - Capture during the exercise
            - Clear view of form
            """)
        else:
            st.info("📝 Upload a photo for your workout log (AI analysis coming soon)")
        
        uploaded_file = st.file_uploader(
            "Upload Workout Photo",
            type=['jpg', 'jpeg', 'png'],
            help="Take a photo during your workout"
        )
        
        # Additional notes
        notes = st.text_area("Workout Notes (optional)", placeholder="How did you feel? Any achievements?")
        
        st.write("---")
        
        # LOG WORKOUT BUTTON
        if st.button("🚀 Complete & Log Workout", type="primary", use_container_width=True):
            if uploaded_file is None:
                st.error("⚠️ Please upload a photo to verify your workout!")
            elif workout_duration_minutes < 1:
                st.error("⚠️ Please use the timer to track your workout duration!")
            else:
                # Save uploaded image
                from PIL import Image
                import base64
                from io import BytesIO
                
                image = Image.open(uploaded_file)
                
                # Convert image to base64 for storage (optional)
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                # AI Verification
                points_earned = 0
                verification_status = "pending"
                
                if has_openai:
                    try:
                        is_valid, feedback, confidence = verify_workout_with_openai(image, exercise_type)
                        
                        if is_valid:
                            # Award points based on duration
                            points_earned = int(workout_duration_minutes * 10)  # 10 points per minute
                            verification_status = "verified"
                            
                            st.success(f"""
                            ✅ **Workout Verified!**
                            
                            **Exercise:** {exercise_type}
                            **Duration:** {workout_duration_minutes:.1f} minutes
                            **Points Earned:** +{points_earned} points! 🎉
                            **AI Confidence:** {confidence}%
                            
                            **Feedback:** {feedback}
                            """)
                        else:
                            verification_status = "failed"
                            st.warning(f"""
                            ⚠️ **Verification Issue**
                            
                            {feedback}
                            
                            Please try uploading a clearer photo showing proper form.
                            """)
                    except Exception as e:
                        st.error(f"AI Verification error: {str(e)}")
                        # Award points anyway in case of API error
                        points_earned = int(workout_duration_minutes * 5)  # Reduced points
                        verification_status = "error"
                else:
                    # Mock mode - award points anyway for testing
                    points_earned = int(workout_duration_minutes * 10)
                    verification_status = "mock"
                    
                    st.success(f"""
                    ✅ **Workout Logged!** (Mock Mode)
                    
                    **Exercise:** {exercise_type}
                    **Duration:** {workout_duration_minutes:.1f} minutes
                    **Points Earned:** +{points_earned} points! 🎉
                    
                    💡 Connect OpenAI API for real verification
                    """)
                
                # Save workout to history
                workout_entry = {
                    'name': exercise_type,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M'),
                    'duration': int(workout_duration_minutes),
                    'intensity': intensity,
                    'notes': notes,
                    'points_earned': points_earned,
                    'verification_status': verification_status,
                    'has_photo': True
                }
                
                user_data['exercises'].insert(0, workout_entry)
                
                # Update points and house points
                user_data['total_points'] = user_data.get('total_points', 0) + points_earned
                
                # House points (1 hour = 1 point)
                house_points_earned = workout_duration_minutes / 60
                user_data['house_points_contributed'] = user_data.get('house_points_contributed', 0) + house_points_earned
                user_data['total_workout_hours'] = user_data.get('total_workout_hours', 0) + (workout_duration_minutes / 60)
                
                # Check for new badges
                new_badges, badge_points = check_and_award_badges(user_data)
                
                if new_badges:
                    user_data['badges'].extend(new_badges)
                    user_data['total_points'] += badge_points
                    
                    st.success("🎖️ **New Badges Earned!**")
                    for badge in new_badges:
                        st.success(f"{badge['name']} - {badge['description']} (+{badge['points']} pts)")
                
                # Update level
                user_data['level'] = calculate_level(user_data['total_points'])[0]
                
                update_user_data(user_data)
                
                st.balloons()
                
                # Show summary
                st.success(f"""
                ✅ **Workout Saved Successfully!**
                
                📊 **Session Summary:**
                - Duration: {workout_duration_minutes:.1f} minutes
                - House Points: +{house_points_earned:.2f} 🏠
                - Workout Points: +{points_earned} ⭐
                - New Total Points: {user_data['total_points']}
                - New Level: {user_data['level']}
                """)
                
                # Wait a moment then refresh to show updated points
                time.sleep(2)
                
                # Reset timer
                st.session_state.timer_running = False
                st.session_state.timer_seconds_left = 0
                st.session_state.timer_total = 0
                
                st.rerun()
    
    with tab2:
        st.subheader("🏃 Running & Steps Tracker")
        
        st.write("Track your daily steps and running sessions! **Earn 1 point for every 10,000 steps!**")
        
        # Initialize steps data
        if 'steps_data' not in user_data:
            user_data['steps_data'] = []
            update_user_data(user_data)
        
        # Create sub-tabs
        steps_tab1, steps_tab2, steps_tab3 = st.tabs([
            "📊 Log Today's Steps",
            "🏃 Log Run/Walk",
            "📈 Steps History"
        ])
        
        with steps_tab1:
            st.write("### 📱 Daily Steps Logger")
            
            today_date = datetime.now().strftime('%Y-%m-%d')
            
            # Check if already logged today
            today_entry = next((s for s in user_data['steps_data'] if s['date'] == today_date), None)
            
            if today_entry:
                st.info(f"""
                ✅ **Today's Steps Already Logged!**
                
                **Steps:** {today_entry['steps']:,} steps
                **Points Earned:** {today_entry['points_earned']} pts
                **Distance:** {today_entry.get('distance_km', 0):.2f} km
                
                You can update below if needed.
                """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                steps_input = st.number_input(
                    "Steps Today",
                    min_value=0,
                    max_value=100000,
                    value=today_entry['steps'] if today_entry else 0,
                    step=100,
                    help="Enter your total steps for today"
                )
            
            with col2:
                # Auto-calculate distance (average: 1 step ≈ 0.000762 km)
                distance_km = steps_input * 0.000762
                st.metric("Estimated Distance", f"{distance_km:.2f} km")
            
            # Show points preview
            points_from_steps = steps_input // 10000  # 1 point per 10,000 steps
            
            if steps_input >= 10000:
                st.success(f"🎉 Great job! You'll earn **{points_from_steps} points** for {steps_input:,} steps!")
            elif steps_input >= 5000:
                st.info(f"💪 Keep going! You need {10000 - steps_input:,} more steps for 1 point!")
            else:
                st.write(f"📊 Current: {steps_input:,} steps | Goal: 10,000 steps for 1 point")
            
            # Progress bar
            progress = min(steps_input / 10000, 1.0)
            st.progress(progress)
            
            if st.button("💾 Log Steps", type="primary", use_container_width=True):
                if steps_input == 0:
                    st.error("Please enter your steps count!")
                else:
                    # Calculate points
                    points_earned = steps_input // 10000
                    
                    # Create or update entry
                    steps_entry = {
                        'date': today_date,
                        'steps': steps_input,
                        'distance_km': distance_km,
                        'points_earned': points_earned,
                        'type': 'daily_steps'
                    }
                    
                    # Remove old today entry if exists
                    user_data['steps_data'] = [s for s in user_data['steps_data'] if s['date'] != today_date]
                    
                    # Add new entry
                    user_data['steps_data'].insert(0, steps_entry)
                    
                    # Award points
                    user_data['total_points'] = user_data.get('total_points', 0) + points_earned
                    
                    update_user_data(user_data)
                    
                    st.success(f"""
                    ✅ **Steps Logged!**
                    
                    **Date:** {today_date}
                    **Steps:** {steps_input:,}
                    **Distance:** {distance_km:.2f} km
                    **Points Earned:** +{points_earned} pts 🎉
                    """)
                    
                    if points_earned > 0:
                        st.balloons()
        
        with steps_tab2:
            st.write("### 🏃 Log Running/Walking Session")
            
            run_col1, run_col2 = st.columns(2)
            
            with run_col1:
                activity_type = st.selectbox(
                    "Activity",
                    ["🏃 Running", "🚶 Walking", "🏃‍♂️ Jogging", "🏃 Sprint Training"]
                )
            
            with run_col2:
                run_date = st.date_input("Date", datetime.now())
            
            # Distance and time inputs
            dist_col1, dist_col2 = st.columns(2)
            
            with dist_col1:
                distance_km = st.number_input(
                    "Distance (km)",
                    min_value=0.1,
                    max_value=50.0,
                    value=5.0,
                    step=0.1,
                    help="How far did you run/walk?"
                )
            
            with dist_col2:
                duration_min = st.number_input(
                    "Duration (minutes)",
                    min_value=1,
                    max_value=300,
                    value=30,
                    help="How long did it take?"
                )
            
            # Calculate pace
            if duration_min > 0:
                pace_min_per_km = duration_min / distance_km
                pace_mins = int(pace_min_per_km)
                pace_secs = int((pace_min_per_km - pace_mins) * 60)
                
                speed_kmh = (distance_km / duration_min) * 60
                
                st.write("### 📊 Performance Metrics")
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.metric("Pace", f"{pace_mins}:{pace_secs:02d} /km")
                
                with metric_col2:
                    st.metric("Speed", f"{speed_kmh:.2f} km/h")
                
                with metric_col3:
                    # Estimate steps (Running: ~1300 steps/km, Walking: ~1500 steps/km)
                    steps_per_km = 1300 if "Running" in activity_type or "Jogging" in activity_type else 1500
                    estimated_steps = int(distance_km * steps_per_km)
                    st.metric("Est. Steps", f"{estimated_steps:,}")
            
            run_notes = st.text_area("Notes", placeholder="How did you feel? Route details?")
            
            if st.button("🏃 Log Run/Walk", type="primary", use_container_width=True):
                # Calculate points (1 point per 10,000 steps equivalent)
                points_earned = estimated_steps // 10000
                
                # House points (based on duration)
                house_points = duration_min / 60
                
                run_entry = {
                    'date': run_date.strftime('%Y-%m-%d'),
                    'type': 'run_walk',
                    'activity': activity_type,
                    'distance_km': distance_km,
                    'duration_min': duration_min,
                    'pace': f"{pace_mins}:{pace_secs:02d}",
                    'speed_kmh': speed_kmh,
                    'steps': estimated_steps,
                    'points_earned': points_earned,
                    'notes': run_notes
                }
                
                user_data['steps_data'].insert(0, run_entry)
                
                # Award points
                user_data['total_points'] = user_data.get('total_points', 0) + points_earned
                
                # House points
                user_data['house_points_contributed'] = user_data.get('house_points_contributed', 0) + house_points
                user_data['total_workout_hours'] = user_data.get('total_workout_hours', 0) + (duration_min / 60)
                
                # Also log as exercise
                exercise_entry = {
                    'name': activity_type,
                    'date': run_date.strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M'),
                    'duration': duration_min,
                    'intensity': 'Medium',
                    'notes': f"{distance_km} km at {pace_mins}:{pace_secs:02d}/km. {run_notes}",
                    'points_earned': points_earned * 10,  # Bonus for running
                    'verification_status': 'auto'
                }
                
                user_data['exercises'].insert(0, exercise_entry)
                
                update_user_data(user_data)
                
                st.success(f"""
                ✅ **{activity_type} Session Logged!**
                
                **Distance:** {distance_km} km
                **Time:** {duration_min} min
                **Pace:** {pace_mins}:{pace_secs:02d} /km
                **Speed:** {speed_kmh:.2f} km/h
                **Est. Steps:** {estimated_steps:,}
                **Points Earned:** +{points_earned} pts
                **House Points:** +{house_points:.2f} 🏠
                """)
                
                st.balloons()
        
        with steps_tab3:
            st.write("### 📈 Steps & Running History")
            
            if not user_data.get('steps_data'):
                st.info("No steps data yet. Start logging your daily steps and runs!")
            else:
                # Calculate statistics
                total_steps = sum(s.get('steps', 0) for s in user_data['steps_data'])
                total_distance = sum(s.get('distance_km', 0) for s in user_data['steps_data'])
                total_points_steps = sum(s.get('points_earned', 0) for s in user_data['steps_data'])
                
                # Display stats
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("Total Steps", f"{total_steps:,}")
                
                with stat_col2:
                    st.metric("Total Distance", f"{total_distance:.1f} km")
                
                with stat_col3:
                    st.metric("Points from Steps", f"{total_points_steps}")
                
                with stat_col4:
                    avg_daily = total_steps / len(user_data['steps_data']) if user_data['steps_data'] else 0
                    st.metric("Avg Daily Steps", f"{int(avg_daily):,}")
                
                st.write("")
                st.write("### 📊 Recent Activity")
                
                # Show recent entries
                for entry in user_data['steps_data'][:10]:
                    if entry['type'] == 'daily_steps':
                        st.markdown(f"""
                        <div class="stat-card">
                            <p><strong>📅 {entry['date']}</strong> - Daily Steps</p>
                            <p>👣 <strong>{entry['steps']:,} steps</strong> | 
                               📏 {entry.get('distance_km', 0):.2f} km | 
                               ⭐ +{entry['points_earned']} pts</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # run_walk
                        st.markdown(f"""
                        <div class="stat-card">
                            <p><strong>📅 {entry['date']}</strong> - {entry['activity']}</p>
                            <p>🏃 <strong>{entry['distance_km']} km</strong> in {entry['duration_min']} min | 
                               ⏱️ Pace: {entry['pace']} /km | 
                               👣 ~{entry['steps']:,} steps | 
                               ⭐ +{entry['points_earned']} pts</p>
                            {f"<p>📝 {entry['notes']}</p>" if entry.get('notes') else ""}
                        </div>
                        """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("📊 Workout History")
        
        # Display exercise history
        if user_data.get('exercises'):
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            
            total_workouts = len(user_data['exercises'])
            verified_workouts = sum(1 for ex in user_data['exercises'] if ex.get('verified', False))
            total_points = sum(ex.get('points_earned', 0) for ex in user_data['exercises'])
            
            # This week's workouts
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            this_week = [ex for ex in user_data['exercises'] if ex['date'] >= week_ago]
            
            with col1:
                st.metric("Total Workouts", total_workouts)
            with col2:
                st.metric("Verified ✓", verified_workouts)
            with col3:
                st.metric("Total Points", total_points)
            with col4:
                st.metric("This Week", len(this_week))
            
            st.write("")
            
            # Show recent workouts
            st.write("### Recent Workouts")
            
            for idx, exercise in enumerate(user_data['exercises'][:10]):  # Show last 10
                verified = exercise.get('verified', False)
                points = exercise.get('points_earned', 0)
                
                status_color = "#4caf50" if verified else "#ff9800"
                status_icon = "✅" if verified else "⚠️"
                status_text = "VERIFIED" if verified else "UNVERIFIED"
                
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: {status_color};">
                    <strong>{exercise['date']} {exercise.get('time', '')}</strong> - {exercise.get('name', exercise.get('type', 'Exercise'))}<br>
                    <strong>Status:</strong> {status_icon} {status_text}<br>
                    <strong>Reps/Duration:</strong> {exercise['duration']} | 
                    <strong>Intensity:</strong> {exercise.get('intensity', 'N/A')} | 
                    <strong>Points:</strong> {points}<br>
                    {f"<em>Note: {exercise.get('notes', '')}</em>" if exercise.get('notes') else ''}
                </div>
                """, unsafe_allow_html=True)
            
            # Exercise breakdown chart
            st.write("")
            st.write("### 📈 Exercise Breakdown")
            
            exercise_counts = {}
            for ex in user_data['exercises']:
                ex_type = ex.get('type', ex.get('name', 'Unknown'))
                exercise_counts[ex_type] = exercise_counts.get(ex_type, 0) + 1
            
            df_chart = pd.DataFrame({
                'Exercise': list(exercise_counts.keys()),
                'Count': list(exercise_counts.values())
            })
            df_chart = df_chart.set_index('Exercise')
            st.bar_chart(df_chart)
            
            # Verification rate
            st.write("")
            st.write("### ✅ Verification Rate")
            
            if total_workouts > 0:
                verification_rate = (verified_workouts / total_workouts) * 100
                st.progress(verification_rate / 100)
                st.write(f"**{verification_rate:.0f}%** of workouts verified ({verified_workouts}/{total_workouts})")
                
                if verification_rate < 50:
                    st.warning("💡 Verify more workouts to earn more points!")
                elif verification_rate < 80:
                    st.info("👍 Good job! Keep verifying your workouts.")
                else:
                    st.success("🌟 Excellent! You're consistently verifying your workouts!")
        else:
            st.info("No exercises logged yet. Upload your first workout photo above to get started!")

# Goal Setting
def goal_setting():
    st.header("🎯 Fitness Goals")
    
    with st.form("goal_form"):
        goal_type = st.selectbox("Goal Type", 
                                ["Weight Loss", "Muscle Gain", "NAPFA Improvement", 
                                 "Endurance", "Flexibility"])
        target = st.text_input("Target Value", placeholder="e.g., 60kg, Grade 5, 30 min run")
        target_date = st.date_input("Target Date")
        progress = st.slider("Current Progress (%)", 0, 100, 0)
        
        submitted = st.form_submit_button("Set Goal")
        
        if submitted:
            if target:
                user_data = get_user_data()
                user_data['goals'].append({
                    'type': goal_type,
                    'target': target,
                    'date': target_date.strftime('%Y-%m-%d'),
                    'progress': progress,
                    'created': datetime.now().strftime('%Y-%m-%d')
                })
                update_user_data(user_data)
                st.success("Goal set successfully!")
                st.rerun()
            else:
                st.error("Please enter target value")
    
    # Display goals
    user_data = get_user_data()
    if user_data['goals']:
        st.subheader("Your Goals")
        for idx, goal in enumerate(user_data['goals']):
            with st.expander(f"{goal['type']} - {goal['target']}"):
                st.write(f"**Target Date:** {goal['date']}")
                st.write(f"**Created:** {goal['created']}")
                st.progress(goal['progress'] / 100)
                st.write(f"Progress: {goal['progress']}%")
    else:
        st.info("No goals set yet.")

# Badge and Achievement System
def check_and_award_badges(user_data):
    """Check if user earned any new badges and award points"""
    badges_earned = []
    points_earned = 0
    
    existing_badges = [b['name'] for b in user_data.get('badges', [])]
    
    # NAPFA Badges
    if user_data.get('napfa_history'):
        latest_napfa = user_data['napfa_history'][-1]
        
        # First Gold Medal
        if '🥇 First Gold' not in existing_badges and '🥇 Gold' in latest_napfa['medal']:
            badges_earned.append({
                'name': '🥇 First Gold',
                'description': 'Earned your first NAPFA Gold medal!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 100
            })
            points_earned += 100
        
        # Perfect Score
        all_grade_5 = all(grade == 5 for grade in latest_napfa['grades'].values())
        if '💯 Perfect Score' not in existing_badges and all_grade_5:
            badges_earned.append({
                'name': '💯 Perfect Score',
                'description': 'All Grade 5s on NAPFA test!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 200
            })
            points_earned += 200
    
    # Workout Badges
    if user_data.get('exercises'):
        total_workouts = len(user_data['exercises'])
        
        # Century Club
        if '💪 Century Club' not in existing_badges and total_workouts >= 100:
            badges_earned.append({
                'name': '💪 Century Club',
                'description': 'Completed 100 total workouts!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 150
            })
            points_earned += 150
        
        # Fifty Strong
        if '🏋️ Fifty Strong' not in existing_badges and total_workouts >= 50:
            badges_earned.append({
                'name': '🏋️ Fifty Strong',
                'description': 'Completed 50 workouts!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 75
            })
            points_earned += 75
        
        # Getting Started
        if '🎯 Getting Started' not in existing_badges and total_workouts >= 10:
            badges_earned.append({
                'name': '🎯 Getting Started',
                'description': 'Completed 10 workouts!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 25
            })
            points_earned += 25
        
        # Check workout streak
        workout_dates = sorted(list(set([e['date'] for e in user_data['exercises']])), reverse=True)
        if len(workout_dates) >= 2:
            streak = 1
            current_date = datetime.strptime(workout_dates[0], '%Y-%m-%d')
            
            for i in range(1, len(workout_dates)):
                prev_date = datetime.strptime(workout_dates[i], '%Y-%m-%d')
                diff = (current_date - prev_date).days
                
                if diff <= 2:
                    streak += 1
                    current_date = prev_date
                else:
                    break
            
            # 7-day streak
            if '🔥 Week Warrior' not in existing_badges and streak >= 7:
                badges_earned.append({
                    'name': '🔥 Week Warrior',
                    'description': '7-day workout streak!',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'points': 50
                })
                points_earned += 50
            
            # 30-day streak
            if '🔥🔥 Month Master' not in existing_badges and streak >= 30:
                badges_earned.append({
                    'name': '🔥🔥 Month Master',
                    'description': '30-day workout streak!',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'points': 150
                })
                points_earned += 150
    
    # Sleep Badges
    if user_data.get('sleep_history'):
        # Check last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        recent_sleep = [s for s in user_data['sleep_history'] 
                       if datetime.strptime(s['date'], '%Y-%m-%d') >= week_ago]
        
        if len(recent_sleep) >= 7:
            good_sleep_count = sum(1 for s in recent_sleep if s['hours'] >= 8)
            
            if '🌙 Sleep Champion' not in existing_badges and good_sleep_count >= 7:
                badges_earned.append({
                    'name': '🌙 Sleep Champion',
                    'description': '7 days of 8+ hours sleep!',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'points': 50
                })
                points_earned += 50
    
    # Goal Badges
    if user_data.get('goals'):
        completed_goals = sum(1 for g in user_data['goals'] if g['progress'] >= 100)
        
        if '🎯 Goal Crusher' not in existing_badges and completed_goals >= 5:
            badges_earned.append({
                'name': '🎯 Goal Crusher',
                'description': 'Completed 5 fitness goals!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 100
            })
            points_earned += 100
        
        if '🎯 First Goal' not in existing_badges and completed_goals >= 1:
            badges_earned.append({
                'name': '🎯 First Goal',
                'description': 'Completed your first goal!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 30
            })
            points_earned += 30
    
    # Daily Login
    if '📅 Daily Visitor' not in existing_badges and user_data.get('login_streak', 0) >= 7:
        badges_earned.append({
            'name': '📅 Daily Visitor',
            'description': '7-day login streak!',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'points': 40
        })
        points_earned += 40
    
    # House Badges (Phase 7 - NEW!)
    if user_data.get('role') == 'student' and user_data.get('house'):
        house_points = user_data.get('house_points_contributed', 0)
        
        # House Point Milestones
        if '🏠 House Hero' not in existing_badges and house_points >= 100:
            badges_earned.append({
                'name': '🏠 House Hero',
                'description': '100 points for your house!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 150
            })
            points_earned += 150
        
        if '🏠 House Champion' not in existing_badges and house_points >= 50:
            badges_earned.append({
                'name': '🏠 House Champion',
                'description': '50 points for your house!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 75
            })
            points_earned += 75
        
        if '🏠 House Starter' not in existing_badges and house_points >= 10:
            badges_earned.append({
                'name': '🏠 House Starter',
                'description': '10 points for your house!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 25
            })
            points_earned += 25
    
    # Social Badges (Phase 7 - NEW!)
    if user_data.get('friends'):
        friend_count = len(user_data['friends'])
        
        if '👥 Social Butterfly' not in existing_badges and friend_count >= 10:
            badges_earned.append({
                'name': '👥 Social Butterfly',
                'description': '10 friends added!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 50
            })
            points_earned += 50
        
        if '👥 Friend Finder' not in existing_badges and friend_count >= 5:
            badges_earned.append({
                'name': '👥 Friend Finder',
                'description': '5 friends added!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 25
            })
            points_earned += 25
    
    # Group Badges (Phase 7 - NEW!)
    if user_data.get('groups'):
        group_count = len(user_data['groups'])
        
        if '👫 Group Leader' not in existing_badges and group_count >= 3:
            badges_earned.append({
                'name': '👫 Group Leader',
                'description': 'Member of 3 groups!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 40
            })
            points_earned += 40
    
    # Consistency Badges (Phase 7 - NEW!)
    if user_data.get('exercises'):
        # Check workout variety
        exercise_types = set([e['name'] for e in user_data['exercises']])
        
        if '🎨 Variety Master' not in existing_badges and len(exercise_types) >= 10:
            badges_earned.append({
                'name': '🎨 Variety Master',
                'description': '10 different exercise types!',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'points': 60
            })
            points_earned += 60
    
    # Total Hours Badge (Phase 7 - NEW!)
    total_hours = user_data.get('total_workout_hours', 0)
    
    if '⏰ Time Champion' not in existing_badges and total_hours >= 100:
        badges_earned.append({
            'name': '⏰ Time Champion',
            'description': '100 hours of exercise!',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'points': 200
        })
        points_earned += 200
    
    if '⏰ Time Warrior' not in existing_badges and total_hours >= 50:
        badges_earned.append({
            'name': '⏰ Time Warrior',
            'description': '50 hours of exercise!',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'points': 100
        })
        points_earned += 100
    
    if '⏰ Time Starter' not in existing_badges and total_hours >= 10:
        badges_earned.append({
            'name': '⏰ Time Starter',
            'description': '10 hours of exercise!',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'points': 30
        })
        points_earned += 30
    
    return badges_earned, points_earned

def calculate_level(total_points):
    """Calculate user level based on total points"""
    if total_points < 50:
        return "Novice", 0, 50
    elif total_points < 150:
        return "Beginner", 50, 150
    elif total_points < 300:
        return "Intermediate", 150, 300
    elif total_points < 500:
        return "Advanced", 300, 500
    elif total_points < 800:
        return "Expert", 500, 800
    elif total_points < 1200:
        return "Master", 800, 1200
    else:
        return "Legend", 1200, 1200

def update_login_streak(user_data):
    """Update login streak for daily login tracking"""
    last_login = user_data.get('last_login')
    if last_login:
        last_login_date = datetime.fromisoformat(last_login).date()
        today = datetime.now().date()
        days_diff = (today - last_login_date).days
        
        if days_diff == 1:
            # Consecutive day
            user_data['login_streak'] = user_data.get('login_streak', 0) + 1
        elif days_diff == 0:
            # Same day, no change
            pass
        else:
            # Streak broken
            user_data['login_streak'] = 1
    else:
        user_data['login_streak'] = 1
    
    user_data['last_login'] = datetime.now().isoformat()
    return user_data

# Community and Social Features
def community_features():
    st.header("🏆 Community & Achievements")
    
    user_data = get_user_data()
    all_users = st.session_state.users_data
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Houses",
        "🏆 Leaderboards",
        "🎖️ My Achievements", 
        "👥 Friends",
        "⚡ Challenges",
        "⚙️ Privacy Settings"
    ])
    
    with tab1:
        st.subheader("🏠 House System")
        st.write("Compete for house glory! Every hour you exercise earns 1 point for your house.")
        
        # Calculate house standings
        house_stats = {
            'yellow': {'points': 0, 'members': 0, 'workouts': 0, 'display': '🟡 Yellow House', 'color': '#FFD700'},
            'red': {'points': 0, 'members': 0, 'workouts': 0, 'display': '🔴 Red House', 'color': '#DC143C'},
            'blue': {'points': 0, 'members': 0, 'workouts': 0, 'display': '🔵 Blue House', 'color': '#1E90FF'},
            'green': {'points': 0, 'members': 0, 'workouts': 0, 'display': '🟢 Green House', 'color': '#32CD32'},
            'black': {'points': 0, 'members': 0, 'workouts': 0, 'display': '⚫ Black House', 'color': '#2F4F4F'}
        }
        
        # Calculate total points for each house
        for username, data in all_users.items():
            if data.get('role') == 'student' and data.get('house'):
                house = data['house']
                if house in house_stats:
                    house_stats[house]['points'] += data.get('house_points_contributed', 0)
                    house_stats[house]['members'] += 1
                    house_stats[house]['workouts'] += len(data.get('exercises', []))
        
        # Sort houses by points
        sorted_houses = sorted(house_stats.items(), key=lambda x: x[1]['points'], reverse=True)
        
        # Display house leaderboard
        st.write("### 🏆 House Standings")
        
        for rank, (house_name, stats) in enumerate(sorted_houses, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            
            with st.container():
                st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, {stats['color']} 0%, {stats['color']}dd 100%); color: white; margin: 10px 0;">
                    <h2>{medal} {stats['display']}</h2>
                    <h1>{stats['points']:.1f} Points</h1>
                    <p style="font-size: 1.1em;">
                        👥 {stats['members']} members | 
                        💪 {stats['workouts']} total workouts | 
                        📊 {(stats['points']/stats['members'] if stats['members'] > 0 else 0):.1f} pts/member
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # User's house info
        if user_data.get('role') == 'student' and user_data.get('house'):
            st.write("")
            st.write("---")
            st.write("### 🏠 Your House")
            
            user_house = user_data['house']
            user_house_stats = house_stats.get(user_house, {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Your House", user_house_stats.get('display', user_house.title()))
            with col2:
                st.metric("Your Contribution", f"{user_data.get('house_points_contributed', 0):.1f} pts")
            with col3:
                st.metric("Total Workout Hours", f"{user_data.get('total_workout_hours', 0):.1f}h")
            
            # House rank
            house_rank = next((i+1 for i, (h, s) in enumerate(sorted_houses) if h == user_house), 0)
            if house_rank == 1:
                st.success(f"🥇 Your house is in 1ST PLACE! Keep it up!")
            elif house_rank == 2:
                st.info(f"🥈 Your house is in 2nd place. Keep training to reach 1st!")
            elif house_rank == 3:
                st.info(f"🥉 Your house is in 3rd place. Every workout counts!")
            else:
                st.warning(f"Your house is in {house_rank}th place. Time to train harder!")
            
            # Top contributors in user's house
            st.write("")
            st.write(f"### ⭐ Top Contributors - {user_house_stats.get('display', 'Your House')}")
            
            house_members = [(username, data) for username, data in all_users.items() 
                           if data.get('house') == user_house and data.get('role') == 'student']
            house_members.sort(key=lambda x: x[1].get('house_points_contributed', 0), reverse=True)
            
            for idx, (username, member) in enumerate(house_members[:5], 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                points = member.get('house_points_contributed', 0)
                
                highlight = " 🌟 (You)" if username == st.session_state.username else ""
                st.write(f"{medal} **{member['name']}**{highlight} - {points:.1f} points")
        else:
            st.info("💡 Students: Your house information will appear here after you log workouts!")
    
    with tab2:
        st.subheader("🏆 Leaderboards & High Scores")
        
        if not user_data.get('show_on_leaderboards', False):
            st.warning("⚠️ You're not visible on leaderboards. Update your privacy settings to join!")
            st.info("Go to 'Privacy Settings' tab to enable leaderboard participation.")
        
        # Create sub-tabs for different leaderboard types
        lb_tab1, lb_tab2, lb_tab3, lb_tab4, lb_tab5, lb_tab6 = st.tabs([
            "🌍 Global",
            "🏠 House Rankings", 
            "🏅 High Scores",
            "👥 Friends",
            "👫 Groups",
            "📚 Class"
        ])
        
        # Filter users who opted in to leaderboards
        leaderboard_users = {username: data for username, data in all_users.items() 
                            if data.get('show_on_leaderboards', False) and data.get('role') == 'student'}
        
        with lb_tab1:
            st.write("### 🌍 Global Leaderboards")
            st.write("Compete with everyone who opted in!")
            
            if len(leaderboard_users) == 0:
                st.info("No users on leaderboards yet. Be the first to opt in!")
            else:
                global_board_type = st.selectbox("Select Ranking", [
                    "Total House Points",
                    "Weekly Warriors", 
                    "Workout Streak",
                    "Total Workouts"
                ], key="global_board")
                
                if global_board_type == "Total House Points":
                    st.write("### 🏆 Top House Point Earners")
                    
                    rankings = []
                    for username, data in leaderboard_users.items():
                        points = data.get('house_points_contributed', 0)
                        if points > 0:
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'points': points,
                                'house': data.get('house', 'N/A'),
                                'school': data.get('school', 'N/A')
                            })
                    
                    rankings.sort(key=lambda x: x['points'], reverse=True)
                    
                    for idx, user in enumerate(rankings[:20], 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        
                        house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                        
                        st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['points']:.1f} points")
                
                elif global_board_type == "Weekly Warriors":
                    st.write("### 💪 Most Workouts This Week")
                    
                    week_ago = datetime.now() - timedelta(days=7)
                    weekly_counts = []
                    
                    for username, data in leaderboard_users.items():
                        if data.get('exercises'):
                            weekly_workouts = [e for e in data['exercises'] 
                                             if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                            
                            if weekly_workouts:
                                weekly_counts.append({
                                    'username': username,
                                    'name': data['name'],
                                    'count': len(weekly_workouts),
                                    'total_time': sum(e['duration'] for e in weekly_workouts),
                                    'house': data.get('house', 'N/A')
                                })
                    
                    weekly_counts.sort(key=lambda x: x['count'], reverse=True)
                    
                    for idx, user in enumerate(weekly_counts[:20], 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                        
                        st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['count']} workouts ({user['total_time']} min)")
                
                elif global_board_type == "Workout Streak":
                    st.write("### 🔥 Longest Workout Streaks")
                    
                    streaks = []
                    for username, data in leaderboard_users.items():
                        if data.get('exercises'):
                            workout_dates = sorted(list(set([e['date'] for e in data['exercises']])), reverse=True)
                            if len(workout_dates) >= 1:
                                streak = 1
                                current_date = datetime.strptime(workout_dates[0], '%Y-%m-%d')
                                
                                for i in range(1, len(workout_dates)):
                                    prev_date = datetime.strptime(workout_dates[i], '%Y-%m-%d')
                                    diff = (current_date - prev_date).days
                                    
                                    if diff <= 2:
                                        streak += 1
                                        current_date = prev_date
                                    else:
                                        break
                                
                                streaks.append({
                                    'username': username,
                                    'name': data['name'],
                                    'streak': streak,
                                    'house': data.get('house', 'N/A')
                                })
                    
                    streaks.sort(key=lambda x: x['streak'], reverse=True)
                    
                    for idx, user in enumerate(streaks[:20], 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                        
                        st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['streak']} days 🔥")
                
                else:  # Total Workouts
                    st.write("### 💪 Most Total Workouts")
                    
                    rankings = []
                    for username, data in leaderboard_users.items():
                        total_workouts = len(data.get('exercises', []))
                        if total_workouts > 0:
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'workouts': total_workouts,
                                'house': data.get('house', 'N/A')
                            })
                    
                    rankings.sort(key=lambda x: x['workouts'], reverse=True)
                    
                    for idx, user in enumerate(rankings[:20], 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                        
                        st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['workouts']} workouts")
        
        with lb_tab2:
            st.write("### 🏠 House Rankings")
            st.write("See how each house member ranks!")
            
            user_house = user_data.get('house')
            
            if not user_house:
                st.warning("You need to be in a house to view house rankings!")
            else:
                house_display = {'yellow': '🟡 Yellow', 'red': '🔴 Red', 'blue': '🔵 Blue', 
                               'green': '🟢 Green', 'black': '⚫ Black'}.get(user_house, user_house.title())
                
                st.write(f"### {house_display} House Leaderboard")
                
                # Get all members of user's house who opted in
                house_members = {username: data for username, data in leaderboard_users.items() 
                               if data.get('house') == user_house}
                
                if not house_members:
                    st.info("No house members on leaderboards yet. Encourage your housemates to opt in!")
                else:
                    house_rank_type = st.selectbox("Rank By", [
                        "House Points",
                        "NAPFA Score",
                        "Weekly Workouts"
                    ], key="house_rank")
                    
                    rankings = []
                    
                    if house_rank_type == "House Points":
                        for username, data in house_members.items():
                            points = data.get('house_points_contributed', 0)
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'value': points,
                                'display': f"{points:.1f} points"
                            })
                    
                    elif house_rank_type == "NAPFA Score":
                        for username, data in house_members.items():
                            if data.get('napfa_history'):
                                score = data['napfa_history'][-1]['total']
                                rankings.append({
                                    'username': username,
                                    'name': data['name'],
                                    'value': score,
                                    'display': f"{score}/30"
                                })
                    
                    else:  # Weekly Workouts
                        week_ago = datetime.now() - timedelta(days=7)
                        for username, data in house_members.items():
                            if data.get('exercises'):
                                weekly = [e for e in data['exercises'] 
                                        if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                                rankings.append({
                                    'username': username,
                                    'name': data['name'],
                                    'value': len(weekly),
                                    'display': f"{len(weekly)} workouts"
                                })
                    
                    rankings.sort(key=lambda x: x['value'], reverse=True)
                    
                    for idx, user in enumerate(rankings, 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        
                        st.write(f"{medal} {highlight}**{user['name']}** - {user['display']}")
        
        with lb_tab3:
            st.write("### 🏅 NAPFA High Scores")
            st.write("Record-breaking performances!")
            
            if len(leaderboard_users) == 0:
                st.info("No users on leaderboards yet.")
            else:
                # Age and gender filters
                col1, col2 = st.columns(2)
                with col1:
                    score_age = st.selectbox("Age Group", ["All Ages"] + list(range(12, 19)), key="score_age")
                with col2:
                    score_gender = st.selectbox("Gender", ["All", "Male", "Female"], key="score_gender")
                
                # Filter users
                filtered = leaderboard_users
                if score_age != "All Ages":
                    filtered = {u: d for u, d in filtered.items() if d['age'] == score_age}
                if score_gender != "All":
                    gender_key = 'm' if score_gender == "Male" else 'f'
                    filtered = {u: d for u, d in filtered.items() if d['gender'] == gender_key}
                
                if not filtered:
                    st.info("No users in this category yet")
                else:
                    score_type = st.selectbox("Component", [
                        "Total NAPFA Score",
                        "Sit-Ups",
                        "Standing Broad Jump",
                        "Sit and Reach",
                        "Pull-Ups",
                        "Shuttle Run",
                        "2.4km Run"
                    ], key="score_component")
                    
                    high_scores = []
                    
                    component_map = {
                        'Sit-Ups': 'SU',
                        'Standing Broad Jump': 'SBJ',
                        'Sit and Reach': 'SAR',
                        'Pull-Ups': 'PU',
                        'Shuttle Run': 'SR',
                        '2.4km Run': 'RUN'
                    }
                    
                    for username, data in filtered.items():
                        if data.get('napfa_history'):
                            latest = data['napfa_history'][-1]
                            
                            if score_type == "Total NAPFA Score":
                                high_scores.append({
                                    'username': username,
                                    'name': data['name'],
                                    'score': latest['total'],
                                    'display': f"{latest['total']}/30",
                                    'house': data.get('house', 'N/A'),
                                    'age': data['age']
                                })
                            else:
                                component_key = component_map[score_type]
                                if component_key in latest['scores']:
                                    score_value = latest['scores'][component_key]
                                    
                                    if component_key in ['SR', 'RUN']:
                                        display = f"{score_value:.2f}s" if component_key == 'SR' else f"{int(score_value)}:{int((score_value % 1) * 60):02d}"
                                        reverse_sort = True
                                    else:
                                        display = f"{score_value}"
                                        reverse_sort = False
                                    
                                    high_scores.append({
                                        'username': username,
                                        'name': data['name'],
                                        'score': score_value,
                                        'display': display,
                                        'house': data.get('house', 'N/A'),
                                        'age': data['age']
                                    })
                    
                    # Sort (lower is better for SR and RUN)
                    if score_type in ['Shuttle Run', '2.4km Run']:
                        high_scores.sort(key=lambda x: x['score'])
                    else:
                        high_scores.sort(key=lambda x: x['score'], reverse=True)
                    
                    if high_scores:
                        st.write(f"### 🏆 Top {score_type} Scores")
                        
                        for idx, user in enumerate(high_scores[:15], 1):
                            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                            highlight = "🌟 " if user['username'] == st.session_state.username else ""
                            house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                            
                            st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} (Age {user['age']}) - {user['display']}")
                        
                        # Show record
                        if high_scores:
                            record_holder = high_scores[0]
                            st.success(f"🏆 **Record:** {record_holder['name']} - {record_holder['display']}")
                    else:
                        st.info("No scores available for this component")
        
        with lb_tab4:
            st.write("### 👥 Friends Leaderboard")
            st.write("Compete with your friends!")
            
            friends = user_data.get('friends', [])
            
            if not friends:
                st.info("Add friends to see friend leaderboards!")
            else:
                # Include self in friend leaderboard
                friend_users = {st.session_state.username: user_data}
                for friend in friends:
                    if friend in all_users:
                        friend_users[friend] = all_users[friend]
                
                friend_rank_type = st.selectbox("Rank By", [
                    "House Points",
                    "NAPFA Score",
                    "Total Workouts",
                    "Weekly Workouts"
                ], key="friend_rank")
                
                rankings = []
                
                if friend_rank_type == "House Points":
                    for username, data in friend_users.items():
                        points = data.get('house_points_contributed', 0)
                        rankings.append({
                            'username': username,
                            'name': data['name'],
                            'value': points,
                            'display': f"{points:.1f} points",
                            'house': data.get('house', 'N/A')
                        })
                
                elif friend_rank_type == "NAPFA Score":
                    for username, data in friend_users.items():
                        if data.get('napfa_history'):
                            score = data['napfa_history'][-1]['total']
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'value': score,
                                'display': f"{score}/30",
                                'house': data.get('house', 'N/A')
                            })
                
                elif friend_rank_type == "Total Workouts":
                    for username, data in friend_users.items():
                        total = len(data.get('exercises', []))
                        rankings.append({
                            'username': username,
                            'name': data['name'],
                            'value': total,
                            'display': f"{total} workouts",
                            'house': data.get('house', 'N/A')
                        })
                
                else:  # Weekly Workouts
                    week_ago = datetime.now() - timedelta(days=7)
                    for username, data in friend_users.items():
                        if data.get('exercises'):
                            weekly = [e for e in data['exercises'] 
                                    if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'value': len(weekly),
                                'display': f"{len(weekly)} workouts",
                                'house': data.get('house', 'N/A')
                            })
                
                rankings.sort(key=lambda x: x['value'], reverse=True)
                
                for idx, user in enumerate(rankings, 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    highlight = "🌟 " if user['username'] == st.session_state.username else ""
                    house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                    
                    st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['display']}")
        
        with lb_tab5:
            st.write("### 👫 Group Leaderboards")
            st.write("See how your groups rank!")
            
            user_groups = user_data.get('groups', [])
            
            if not user_groups:
                st.info("Join a group to see group leaderboards!")
            else:
                all_groups = st.session_state.get('all_groups', {})
                
                selected_group_id = st.selectbox(
                    "Select Group",
                    user_groups,
                    format_func=lambda x: all_groups.get(x, {}).get('name', 'Unknown Group'),
                    key="select_group_lb"
                )
                
                group = all_groups.get(selected_group_id, {})
                
                if group:
                    st.write(f"### {group['name']} Leaderboard")
                    
                    group_rank_type = st.selectbox("Rank By", [
                        "House Points",
                        "NAPFA Score",
                        "Total Workouts"
                    ], key="group_rank")
                    
                    rankings = []
                    
                    for member in group['members']:
                        member_data = all_users.get(member, {})
                        
                        if group_rank_type == "House Points":
                            value = member_data.get('house_points_contributed', 0)
                            display = f"{value:.1f} points"
                        elif group_rank_type == "NAPFA Score":
                            if member_data.get('napfa_history'):
                                value = member_data['napfa_history'][-1]['total']
                                display = f"{value}/30"
                            else:
                                continue
                        else:  # Total Workouts
                            value = len(member_data.get('exercises', []))
                            display = f"{value} workouts"
                        
                        rankings.append({
                            'username': member,
                            'name': member_data.get('name', 'Unknown'),
                            'value': value,
                            'display': display,
                            'house': member_data.get('house', 'N/A')
                        })
                    
                    rankings.sort(key=lambda x: x['value'], reverse=True)
                    
                    for idx, user in enumerate(rankings, 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                        
                        st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['display']}")
        
        with lb_tab6:
            st.write("### 📚 Class Leaderboards")
            st.write("See your class rankings!")
            
            user_class = user_data.get('class')
            
            if not user_class:
                st.info("Set your class in Privacy Settings to view class leaderboards!")
            else:
                st.write(f"### Class: {user_class}")
                
                # Get classmates who opted in
                classmates = {username: data for username, data in leaderboard_users.items() 
                            if data.get('class') == user_class}
                
                if not classmates:
                    st.info("No classmates on leaderboards yet!")
                else:
                    class_rank_type = st.selectbox("Rank By", [
                        "NAPFA Score",
                        "House Points",
                        "Total Workouts"
                    ], key="class_rank")
                    
                    rankings = []
                    
                    if class_rank_type == "NAPFA Score":
                        for username, data in classmates.items():
                            if data.get('napfa_history'):
                                score = data['napfa_history'][-1]['total']
                                rankings.append({
                                    'username': username,
                                    'name': data['name'],
                                    'value': score,
                                    'display': f"{score}/30",
                                    'house': data.get('house', 'N/A')
                                })
                    
                    elif class_rank_type == "House Points":
                        for username, data in classmates.items():
                            points = data.get('house_points_contributed', 0)
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'value': points,
                                'display': f"{points:.1f} points",
                                'house': data.get('house', 'N/A')
                            })
                    
                    else:  # Total Workouts
                        for username, data in classmates.items():
                            total = len(data.get('exercises', []))
                            rankings.append({
                                'username': username,
                                'name': data['name'],
                                'value': total,
                                'display': f"{total} workouts",
                                'house': data.get('house', 'N/A')
                            })
                    
                    rankings.sort(key=lambda x: x['value'], reverse=True)
                    
                    for idx, user in enumerate(rankings, 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                        highlight = "🌟 " if user['username'] == st.session_state.username else ""
                        house_emoji = {'yellow': '🟡', 'red': '🔴', 'blue': '🔵', 'green': '🟢', 'black': '⚫'}.get(user['house'], '')
                        
                        st.write(f"{medal} {highlight}**{user['name']}** {house_emoji} - {user['display']}")
    
    with tab3:
                st.write("### 🔥 Longest Workout Streaks")
                
                streaks = []
                for username, data in leaderboard_users.items():
                    if data.get('exercises'):
                        workout_dates = sorted(list(set([e['date'] for e in data['exercises']])), reverse=True)
                        if len(workout_dates) >= 1:
                            streak = 1
                            current_date = datetime.strptime(workout_dates[0], '%Y-%m-%d')
                            
                            for i in range(1, len(workout_dates)):
                                prev_date = datetime.strptime(workout_dates[i], '%Y-%m-%d')
                                diff = (current_date - prev_date).days
                                
                                if diff <= 2:
                                    streak += 1
                                    current_date = prev_date
                                else:
                                    break
                            
                            streaks.append({
                                'username': username,
                                'name': data['name'],
                                'streak': streak,
                                'age': data['age'],
                                'school': data.get('school', 'N/A')
                            })
                
                streaks.sort(key=lambda x: x['streak'], reverse=True)
                
                for idx, user in enumerate(streaks[:10], 1):
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                    
                    highlight = "🌟 " if user['username'] == st.session_state.username else ""
                    st.write(f"{medal} {highlight}**{user['name']}** (@{user['username']}) - {user['streak']} days 🔥")
            
    with tab3:
        st.subheader("🎖️ My Achievements")
        
        # Check for new badges
        new_badges, new_points = check_and_award_badges(user_data)
        
        if new_badges:
            st.balloons()
            st.success(f"🎉 You earned {len(new_badges)} new badge(s) and {new_points} points!")
            
            for badge in new_badges:
                user_data['badges'].append(badge)
                user_data['total_points'] = user_data.get('total_points', 0) + badge['points']
            
            update_user_data(user_data)
        
        # Display level and progress
        current_level, level_min, level_max = calculate_level(user_data.get('total_points', 0))
        user_data['level'] = current_level
        update_user_data(user_data)
        
        st.write("### 📊 Your Progress")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Level", current_level)
        with col2:
            st.metric("Total Points", user_data.get('total_points', 0))
        with col3:
            st.metric("Login Streak", f"{user_data.get('login_streak', 0)} days")
        
        # Progress bar to next level
        if current_level != "Legend":
            progress = (user_data.get('total_points', 0) - level_min) / (level_max - level_min)
            st.progress(progress)
            st.write(f"**Next Level:** {level_max - user_data.get('total_points', 0)} points to go!")
        else:
            st.success("🏆 You've reached the maximum level!")
        
        # Display badges
        st.write("")
        st.write("### 🎖️ Earned Badges")
        
        if user_data.get('badges'):
            # Sort by date
            badges = sorted(user_data['badges'], key=lambda x: x['date'], reverse=True)
            
            cols = st.columns(3)
            for idx, badge in enumerate(badges):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); 
                                padding: 15px; border-radius: 10px; color: white; margin: 5px;">
                        <h3>{badge['name']}</h3>
                        <p>{badge['description']}</p>
                        <small>Earned: {badge['date']} | +{badge['points']} pts</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No badges earned yet. Keep working out to unlock achievements!")
        
        # Available badges to earn
        st.write("")
        st.write("### 🎯 Available Badges")
        
        all_possible_badges = [
            "🥇 First Gold - Earn your first NAPFA Gold medal",
            "💯 Perfect Score - All Grade 5s on NAPFA",
            "💪 Century Club - Complete 100 workouts",
            "🏋️ Fifty Strong - Complete 50 workouts", 
            "🎯 Getting Started - Complete 10 workouts",
            "🔥 Week Warrior - 7-day workout streak",
            "🔥🔥 Month Master - 30-day workout streak",
            "🌙 Sleep Champion - 7 days of 8+ hours sleep",
            "🎯 Goal Crusher - Complete 5 goals",
            "🎯 First Goal - Complete your first goal",
            "📅 Daily Visitor - 7-day login streak"
        ]
        
        earned_names = [b['name'] for b in user_data.get('badges', [])]
        remaining = [b for b in all_possible_badges if not any(name in b for name in earned_names)]
        
        for badge in remaining:
            st.write(f"🔒 {badge}")
    
    with tab4:
        st.subheader("👥 Friends")
        
        # Friend requests
        friend_requests = user_data.get('friend_requests', [])
        if friend_requests:
            st.write("### 📬 Friend Requests")
            for requester in friend_requests:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    requester_data = all_users.get(requester, {})
                    st.write(f"**{requester_data.get('name', 'Unknown')}** (@{requester})")
                with col2:
                    if st.button("✅ Accept", key=f"accept_{requester}"):
                        user_data['friends'].append(requester)
                        user_data['friend_requests'].remove(requester)
                        
                        # Add to requester's friends too
                        all_users[requester]['friends'].append(st.session_state.username)
                        
                        update_user_data(user_data)
                        save_users(all_users)
                        st.success(f"Added {requester} as friend!")
                        st.rerun()
                with col3:
                    if st.button("❌ Decline", key=f"decline_{requester}"):
                        user_data['friend_requests'].remove(requester)
                        update_user_data(user_data)
                        st.rerun()
        
        # Add friend
        st.write("### ➕ Add Friend")
        new_friend = st.text_input("Enter username", key="add_friend_input")
        if st.button("Send Friend Request"):
            if new_friend in all_users:
                if new_friend == st.session_state.username:
                    st.error("You can't add yourself!")
                elif new_friend in user_data.get('friends', []):
                    st.error("Already friends!")
                elif new_friend in all_users[new_friend].get('friend_requests', []):
                    st.error("Request already sent!")
                else:
                    # Add request to target user
                    all_users[new_friend]['friend_requests'].append(st.session_state.username)
                    save_users(all_users)
                    st.success(f"Friend request sent to {new_friend}!")
            else:
                st.error("User not found")
        
        # Friends list
        st.write("### 👥 My Friends")
        friends = user_data.get('friends', [])
        
        if friends:
            for friend in friends:
                friend_data = all_users.get(friend, {})
                
                with st.expander(f"👤 {friend_data.get('name', 'Unknown')} (@{friend})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Age:** {friend_data.get('age', 'N/A')}")
                        st.write(f"**School:** {friend_data.get('school', 'N/A')}")
                        st.write(f"**Level:** {friend_data.get('level', 'Novice')}")
                    
                    with col2:
                        if friend_data.get('napfa_history'):
                            latest = friend_data['napfa_history'][-1]
                            st.write(f"**NAPFA:** {latest['total']}/30")
                            st.write(f"**Medal:** {latest['medal']}")
                        
                        if friend_data.get('exercises'):
                            st.write(f"**Workouts:** {len(friend_data['exercises'])}")
                    
                    # Recent activity
                    if friend_data.get('badges'):
                        recent_badge = friend_data['badges'][-1]
                        st.info(f"🎖️ Recently earned: {recent_badge['name']}")
                    
                    if st.button(f"Remove Friend", key=f"remove_{friend}"):
                        user_data['friends'].remove(friend)
                        all_users[friend]['friends'].remove(st.session_state.username)
                        update_user_data(user_data)
                        save_users(all_users)
                        st.rerun()
        else:
            st.info("No friends yet. Add friends to see their progress!")
        
        # GROUPS SECTION
        st.write("")
        st.write("---")
        st.write("## 👫 Groups")
        st.write("Create or join groups to workout together!")
        
        # Initialize groups in session state if not exists
        if 'all_groups' not in st.session_state:
            st.session_state.all_groups = {}
        
        # Initialize user groups
        if 'groups' not in user_data:
            user_data['groups'] = []
            user_data['group_invites'] = []
            update_user_data(user_data)
        
        group_tab1, group_tab2 = st.tabs(["My Groups", "Create/Join Group"])
        
        with group_tab1:
            st.write("### 👫 My Groups")
            
            user_groups = user_data.get('groups', [])
            
            if user_groups:
                all_groups = st.session_state.all_groups
                
                for group_id in user_groups:
                    group = all_groups.get(group_id, {})
                    if group:
                        with st.expander(f"👫 {group['name']} ({len(group['members'])}/{group['max_members']} members)"):
                            st.write(f"**Type:** {group['type']}")
                            st.write(f"**Description:** {group['description']}")
                            st.write(f"**Admin:** {all_users.get(group['admin'], {}).get('name', 'Unknown')}")
                            st.write(f"**Created:** {group['created']}")
                            
                            # Members list
                            st.write("")
                            st.write("**Members:**")
                            for member in group['members']:
                                member_data = all_users.get(member, {})
                                admin_badge = " 👑" if member == group['admin'] else ""
                                st.write(f"• {member_data.get('name', 'Unknown')} (@{member}){admin_badge}")
                            
                            # Group stats
                            st.write("")
                            group_workouts = sum([len(all_users.get(m, {}).get('exercises', [])) for m in group['members']])
                            group_house_points = sum([all_users.get(m, {}).get('house_points_contributed', 0) for m in group['members']])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Total Workouts", group_workouts)
                            with col2:
                                st.metric("Total House Points", f"{group_house_points:.1f}")
                            
                            # Group leaderboard
                            st.write("")
                            st.write("**Group Leaderboard:**")
                            member_scores = [(m, all_users.get(m, {}).get('house_points_contributed', 0)) 
                                           for m in group['members']]
                            member_scores.sort(key=lambda x: x[1], reverse=True)
                            
                            for idx, (member, score) in enumerate(member_scores[:5], 1):
                                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                                member_name = all_users.get(member, {}).get('name', 'Unknown')
                                highlight = " 🌟" if member == st.session_state.username else ""
                                st.write(f"{medal} {member_name}{highlight} - {score:.1f} points")
                            
                            # Invite friends (admin only)
                            if group['admin'] == st.session_state.username:
                                st.write("")
                                st.write("**Invite Friends:**")
                                
                                available_friends = [f for f in user_data.get('friends', []) if f not in group['members']]
                                
                                if available_friends and len(group['members']) < group['max_members']:
                                    invite_friend = st.selectbox(
                                        "Select friend",
                                        available_friends,
                                        format_func=lambda x: all_users.get(x, {}).get('name', 'Unknown'),
                                        key=f"invite_{group_id}"
                                    )
                                    
                                    if st.button(f"Send Invite", key=f"send_{group_id}"):
                                        all_users[invite_friend].setdefault('group_invites', []).append(group_id)
                                        save_users(all_users)
                                        st.success(f"Invite sent!")
                                        st.rerun()
                                elif len(group['members']) >= group['max_members']:
                                    st.info("Group is full!")
                            
                            # Leave group
                            if st.button(f"Leave Group", key=f"leave_{group_id}"):
                                group['members'].remove(st.session_state.username)
                                user_data['groups'].remove(group_id)
                                update_user_data(user_data)
                                st.rerun()
            else:
                st.info("You're not in any groups yet. Create or join one in the other tab!")
        
        with group_tab2:
            st.write("### 🆕 Create New Group")
            
            col1, col2 = st.columns(2)
            with col1:
                group_name = st.text_input("Group Name", placeholder="e.g., Running Club")
                group_description = st.text_area("Description", placeholder="Group goals...")
            
            with col2:
                group_type = st.selectbox("Type", 
                                         ["Study Group", "CCA Team", "Running Club", "Gym Buddies", "General Fitness"])
                max_members = st.number_input("Max Members", min_value=2, max_value=50, value=10)
            
            if st.button("Create Group", type="primary"):
                if group_name:
                    group_id = f"group_{st.session_state.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    new_group = {
                        'id': group_id,
                        'name': group_name,
                        'description': group_description,
                        'type': group_type,
                        'admin': st.session_state.username,
                        'members': [st.session_state.username],
                        'max_members': max_members,
                        'created': datetime.now().strftime('%Y-%m-%d'),
                        'total_points': 0
                    }
                    
                    st.session_state.all_groups[group_id] = new_group
                    user_data['groups'].append(group_id)
                    update_user_data(user_data)
                    
                    st.success(f"Group '{group_name}' created!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please enter a group name")
            
            # Group Invites
            group_invites = user_data.get('group_invites', [])
            if group_invites:
                st.write("")
                st.write("### 📬 Group Invitations")
                
                for group_id in group_invites:
                    group = st.session_state.all_groups.get(group_id, {})
                    if group:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{group['name']}** - {group['type']}")
                        with col2:
                            if st.button("✅ Join", key=f"join_{group_id}"):
                                if len(group['members']) < group['max_members']:
                                    group['members'].append(st.session_state.username)
                                    user_data['groups'].append(group_id)
                                    user_data['group_invites'].remove(group_id)
                                    update_user_data(user_data)
                                    st.success(f"Joined {group['name']}!")
                                    st.rerun()
                                else:
                                    st.error("Group is full!")
                        with col3:
                            if st.button("❌", key=f"decline_{group_id}"):
                                user_data['group_invites'].remove(group_id)
                                update_user_data(user_data)
                                st.rerun()
    
    with tab5:
        st.subheader("⚡ Challenges")
        
        # Weekly Challenges
        st.write("### 🏃 Weekly Challenges")
        
        # Define weekly challenges
        weekly_challenges = [
            {
                'name': 'Workout Warrior',
                'description': 'Complete 5 workouts this week',
                'target': 5,
                'type': 'workouts',
                'points': 50
            },
            {
                'name': 'Cardio King',
                'description': 'Total 150 minutes of exercise this week',
                'target': 150,
                'type': 'minutes',
                'points': 60
            },
            {
                'name': 'Early Bird',
                'description': 'Log 7 days of sleep tracking',
                'target': 7,
                'type': 'sleep',
                'points': 40
            }
        ]
        
        # Check progress
        week_ago = datetime.now() - timedelta(days=7)
        
        for challenge in weekly_challenges:
            with st.expander(f"{'✅' if challenge['name'] in [c['name'] for c in user_data.get('completed_challenges', [])] else '⚡'} {challenge['name']} (+{challenge['points']} pts)", expanded=True):
                st.write(f"**Goal:** {challenge['description']}")
                
                # Calculate progress
                if challenge['type'] == 'workouts':
                    weekly_workouts = [e for e in user_data.get('exercises', []) 
                                     if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                    progress = len(weekly_workouts)
                elif challenge['type'] == 'minutes':
                    weekly_workouts = [e for e in user_data.get('exercises', []) 
                                     if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                    progress = sum(e['duration'] for e in weekly_workouts)
                else:  # sleep
                    weekly_sleep = [s for s in user_data.get('sleep_history', []) 
                                  if datetime.strptime(s['date'], '%Y-%m-%d') >= week_ago]
                    progress = len(weekly_sleep)
                
                st.progress(min(progress / challenge['target'], 1.0))
                st.write(f"**Progress:** {progress}/{challenge['target']}")
                
                if progress >= challenge['target']:
                    completed_names = [c['name'] for c in user_data.get('completed_challenges', [])]
                    if challenge['name'] not in completed_names:
                        st.success("🎉 Challenge completed! Points awarded!")
                        user_data.setdefault('completed_challenges', []).append({
                            'name': challenge['name'],
                            'completed_date': datetime.now().strftime('%Y-%m-%d'),
                            'points': challenge['points']
                        })
                        user_data['total_points'] = user_data.get('total_points', 0) + challenge['points']
                        update_user_data(user_data)
        
        # Friend Challenges
        st.write("")
        st.write("### 🤝 Friend Challenges")
        
        friends = user_data.get('friends', [])
        if not friends:
            st.info("Add friends to create challenges with them!")
        else:
            selected_friend = st.selectbox("Challenge a friend", friends)
            
            challenge_types = [
                "Most workouts this week",
                "Highest NAPFA score",
                "Longest workout streak"
            ]
            
            challenge_type = st.selectbox("Challenge type", challenge_types)
            
            if st.button("Send Challenge"):
                st.success(f"Challenge sent to {selected_friend}! (Feature coming soon)")
        
        # Class Challenges
        st.write("")
        st.write("### 🏫 Class Challenges")
        
        if user_data.get('class'):
            st.write(f"**Your Class:** {user_data['class']}")
            
            # Get class members
            class_members = {u: d for u, d in all_users.items() 
                           if d.get('class') == user_data['class'] and d.get('show_on_leaderboards', False)}
            
            if len(class_members) > 1:
                st.write(f"**Class Members:** {len(class_members)}")
                
                # Show class goal
                st.info("🎯 **Class Goal:** Average NAPFA score of 20+ by end of month!")
                
                # Calculate class average
                napfa_scores = []
                for data in class_members.values():
                    if data.get('napfa_history'):
                        napfa_scores.append(data['napfa_history'][-1]['total'])
                
                if napfa_scores:
                    class_avg = sum(napfa_scores) / len(napfa_scores)
                    st.metric("Current Class Average", f"{class_avg:.1f}/30")
                    
                    if class_avg >= 20:
                        st.success("🎉 Class goal achieved!")
            else:
                st.info("Not enough class members on leaderboards yet")
        else:
            st.info("Set your class in Privacy Settings to join class challenges!")
    
    with tab6:
        st.subheader("⚙️ Privacy Settings")
        
        st.write("### 👁️ Leaderboard Visibility")
        
        current_setting = user_data.get('show_on_leaderboards', False)
        new_setting = st.checkbox("Show me on public leaderboards", value=current_setting)
        
        if new_setting != current_setting:
            user_data['show_on_leaderboards'] = new_setting
            update_user_data(user_data)
            st.success("✅ Settings updated!")
            st.rerun()
        
        st.info("ℹ️ When enabled, your stats will be visible on leaderboards. Your friends can always see your profile.")
        
        # Update school/class
        st.write("")
        st.write("### 🏫 School & Class")
        
        col1, col2 = st.columns(2)
        with col1:
            current_school = user_data.get('school', '')
            new_school = st.text_input("School", value=current_school, key="update_school")
        
        with col2:
            current_class = user_data.get('class', '')
            new_class = st.text_input("Class", value=current_class, key="update_class")
        
        if st.button("Update School/Class Info"):
            user_data['school'] = new_school
            user_data['class'] = new_class
            update_user_data(user_data)
            st.success("✅ Updated!")
            st.rerun()
        
        # Personal Data Export (Phase 7 BONUS!)
        st.write("")
        st.write("### 📥 Export Your Data")
        st.write("Download all your personal fitness data")
        
        if st.button("📥 Download My Data (JSON)", type="secondary"):
            import json
            
            # Create exportable data
            export_data = {
                'account_info': {
                    'name': user_data.get('name'),
                    'email': user_data.get('email'),
                    'age': user_data.get('age'),
                    'gender': 'Male' if user_data.get('gender') == 'm' else 'Female',
                    'school': user_data.get('school'),
                    'class': user_data.get('class'),
                    'house': user_data.get('house'),
                    'created': user_data.get('created'),
                    'role': user_data.get('role')
                },
                'fitness_data': {
                    'bmi_history': user_data.get('bmi_history', []),
                    'napfa_history': user_data.get('napfa_history', []),
                    'sleep_history': user_data.get('sleep_history', []),
                    'exercises': user_data.get('exercises', []),
                    'total_workout_hours': user_data.get('total_workout_hours', 0),
                    'house_points_contributed': user_data.get('house_points_contributed', 0)
                },
                'achievements': {
                    'badges': user_data.get('badges', []),
                    'level': user_data.get('level'),
                    'total_points': user_data.get('total_points', 0),
                    'login_streak': user_data.get('login_streak', 0)
                },
                'social': {
                    'friends': user_data.get('friends', []),
                    'groups': user_data.get('groups', [])
                },
                'goals': user_data.get('smart_goals', []),
                'exported_date': datetime.now().isoformat()
            }
            
            # Convert to JSON
            json_data = json.dumps(export_data, indent=2)
            
            st.download_button(
                label="📥 Download JSON File",
                data=json_data,
                file_name=f"fittrack_data_{user_data.get('name', 'user')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
            st.success("✅ Your data is ready for download!")
            st.info("💡 This JSON file contains all your FitTrack data. Keep it safe as a backup!")

# AI Insights and Recommendations
def ai_insights():
    st.header("🤖 AI Fitness Coach")
    
    user_data = get_user_data()
    
    # Create tabs for AI features - cleaned up, removed empty/duplicate tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 ML Predictions",
        "🎯 SMART Goals",
        "🗓️ AI Schedule Generator",
        "🍳 Health Recipes"
    ])
    
    with tab1:
        st.subheader("🤖 Machine Learning Predictions & Statistical Analysis")
        st.write("AI-powered predictions based on your performance data")
        
        # Check if enough data
        has_napfa = len(user_data.get('napfa_history', [])) > 0
        has_multiple_napfa = len(user_data.get('napfa_history', [])) >= 2
        has_sleep = len(user_data.get('sleep_history', [])) >= 7
        has_exercises = len(user_data.get('exercises', [])) >= 5
        
        # Prediction 1: When will you reach NAPFA Gold?
        st.write("### 🥇 NAPFA Gold Prediction")
        
        if not has_napfa:
            st.info("Complete your first NAPFA test to get predictions!")
        elif not has_multiple_napfa:
            latest_napfa = user_data['napfa_history'][-1]
            current_score = latest_napfa['total']
            
            if current_score >= 21:
                st.success(f"🎉 You already have NAPFA Gold! (Score: {current_score}/30)")
            else:
                points_needed = 21 - current_score
                st.info(f"**Current Score:** {current_score}/30")
                st.info(f"**Points Needed for Gold:** {points_needed}")
                st.write("Complete another NAPFA test to get improvement rate predictions!")
        else:
            # ML Prediction: Linear regression on NAPFA scores
            napfa_history = user_data['napfa_history']
            scores = [test['total'] for test in napfa_history]
            dates = [datetime.strptime(test['date'], '%Y-%m-%d') for test in napfa_history]
            
            # Calculate improvement rate
            days_between = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            score_changes = [scores[i] - scores[i-1] for i in range(1, len(scores))]
            
            if sum(days_between) > 0:
                avg_improvement_per_day = sum(score_changes) / sum(days_between)
                avg_improvement_per_month = avg_improvement_per_day * 30
                
                current_score = scores[-1]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Current NAPFA", f"{current_score}/30")
                    st.metric("Improvement Rate", f"+{avg_improvement_per_month:.2f} pts/month")
                
                with col2:
                    if current_score >= 21:
                        st.success("🥇 Gold Medal Achieved!")
                    else:
                        points_needed = 21 - current_score
                        if avg_improvement_per_day > 0:
                            days_to_gold = points_needed / avg_improvement_per_day
                            months_to_gold = days_to_gold / 30
                            predicted_date = datetime.now() + timedelta(days=days_to_gold)
                            
                            st.metric("Points to Gold", points_needed)
                            st.metric("Predicted Gold Date", predicted_date.strftime('%B %Y'))
                            
                            st.info(f"📅 At your current rate, you'll reach Gold in ~{months_to_gold:.1f} months!")
                        else:
                            st.warning("Your score is decreasing. Focus on training to improve!")
                
                # Show prediction chart
                st.write("### 📈 Score Projection")
                
                # Project next 6 months
                future_dates = [datetime.now() + timedelta(days=30*i) for i in range(7)]
                future_scores = [current_score + (avg_improvement_per_day * 30 * i) for i in range(7)]
                future_scores = [min(max(s, 0), 30) for s in future_scores]  # Cap at 0-30
                
                df = pd.DataFrame({
                    'Date': [d.strftime('%b %Y') for d in future_dates],
                    'Predicted Score': future_scores
                })
                
                st.line_chart(df.set_index('Date'))
                
                st.write(f"**Model:** Linear regression based on {len(napfa_history)} test(s)")
                st.write(f"**Confidence:** {'High' if len(napfa_history) >= 4 else 'Medium' if len(napfa_history) >= 3 else 'Low'}")
        
        st.write("---")
        
        # Prediction 2: Sleep Impact on Performance
        st.write("### 😴 Sleep Impact Analysis")
        
        if not has_sleep or not has_napfa:
            st.info("Track sleep for 7+ days and complete NAPFA to see correlation!")
        else:
            sleep_data = user_data['sleep_history']
            
            # Calculate average sleep
            avg_sleep_hours = sum([s['hours'] + s['minutes']/60 for s in sleep_data]) / len(sleep_data)
            
            # Analyze NAPFA performance vs sleep
            napfa_score = user_data['napfa_history'][-1]['total']
            
            # Statistical correlation (simplified)
            if avg_sleep_hours >= 8:
                performance_rating = "Optimal"
                color = "#4caf50"
                insight = "Your sleep supports peak performance! Keep it up."
                predicted_improvement = 0
            elif avg_sleep_hours >= 7:
                performance_rating = "Good"
                color = "#8bc34a"
                insight = "Good sleep, but getting 8+ hours could improve your NAPFA score by ~2-3 points."
                predicted_improvement = 2.5
            else:
                performance_rating = "Below Optimal"
                color = "#ff9800"
                insight = "⚠️ Poor sleep is limiting your performance. Getting 8+ hours could improve your score by ~5 points!"
                predicted_improvement = 5
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Sleep", f"{avg_sleep_hours:.1f} hours")
                st.metric("Current NAPFA", f"{napfa_score}/30")
            
            with col2:
                st.markdown(f'<div class="stat-card" style="background: {color}; color: white;"><h3>{performance_rating}</h3></div>', unsafe_allow_html=True)
                if predicted_improvement > 0:
                    st.metric("Potential Gain", f"+{predicted_improvement:.1f} points")
            
            st.info(f"💡 **Insight:** {insight}")
            
            # Show correlation
            st.write("**Research shows:** Students who sleep 8+ hours score on average 15% higher on NAPFA tests.")
        
        st.write("---")
        
        # Prediction 3: Injury Risk Prediction
        st.write("### 🏥 Injury Risk Assessment")
        
        if not has_exercises:
            st.info("Log 5+ workouts to get injury risk analysis!")
        else:
            exercises = user_data['exercises']
            
            # Calculate workout intensity distribution
            intensity_counts = {'Low': 0, 'Medium': 0, 'High': 0}
            for ex in exercises:
                intensity_counts[ex['intensity']] += 1
            
            total = sum(intensity_counts.values())
            high_intensity_ratio = intensity_counts['High'] / total if total > 0 else 0
            
            # Check workout frequency (last 2 weeks)
            two_weeks_ago = datetime.now() - timedelta(days=14)
            recent_workouts = [e for e in exercises 
                             if datetime.strptime(e['date'], '%Y-%m-%d') >= two_weeks_ago]
            
            workouts_per_week = len(recent_workouts) / 2
            
            # Risk calculation
            risk_score = 0
            risk_factors = []
            
            if high_intensity_ratio > 0.7:
                risk_score += 30
                risk_factors.append("⚠️ Too many high-intensity workouts (>70%)")
            
            if workouts_per_week > 6:
                risk_score += 25
                risk_factors.append("⚠️ Insufficient rest days (<1 per week)")
            
            if workouts_per_week < 2:
                risk_score += 15
                risk_factors.append("⚠️ Inconsistent training increases injury risk")
            
            # Sleep factor
            if has_sleep:
                if avg_sleep_hours < 7:
                    risk_score += 20
                    risk_factors.append("⚠️ Poor sleep reduces recovery")
            
            # Determine risk level
            if risk_score >= 50:
                risk_level = "High Risk"
                risk_color = "#f44336"
                recommendation = "🚨 REDUCE intensity and take more rest days!"
            elif risk_score >= 25:
                risk_level = "Moderate Risk"
                risk_color = "#ff9800"
                recommendation = "⚠️ Balance your training intensity and rest."
            else:
                risk_level = "Low Risk"
                risk_color = "#4caf50"
                recommendation = "✅ Your training is well-balanced!"
            
            st.markdown(f'<div class="stat-card" style="background: {risk_color}; color: white;"><h2>Risk Level: {risk_level}</h2><p>{recommendation}</p></div>', unsafe_allow_html=True)
            
            if risk_factors:
                st.write("**Risk Factors:**")
                for factor in risk_factors:
                    st.write(factor)
            
            st.write("")
            st.write("**Injury Prevention Tips:**")
            st.write("1. Include 1-2 rest days per week")
            st.write("2. Mix high, medium, and low intensity workouts")
            st.write("3. Sleep 8+ hours for recovery")
            st.write("4. Warm up before and cool down after exercise")
            st.write("5. Listen to your body - rest if you feel pain")
    
    with tab2:
        st.subheader("🎯 SMART Goals System")
        st.write("Set Specific, Measurable, Achievable, Relevant, and Time-bound goals")
        
        # Initialize smart_goals if it doesn't exist
        if 'smart_goals' not in user_data:
            user_data['smart_goals'] = []
            update_user_data(user_data)
        
        # Create or view SMART goals
        goal_tab1, goal_tab2 = st.tabs(["Create New Goal", "My SMART Goals"])
        
        with goal_tab1:
            st.write("### Create a SMART Goal")
            
            # Goal type selection
            goal_category = st.selectbox(
                "Goal Category",
                ["NAPFA Improvement", "Weight Management", "Strength Building", 
                 "Endurance Training", "Flexibility", "Consistency/Habits"]
            )
            
            # Specific
            st.write("#### 📝 Specific - What exactly do you want to achieve?")
            
            if goal_category == "NAPFA Improvement":
                specific_options = [
                    "Achieve NAPFA Gold Medal",
                    "Improve specific component to Grade 5",
                    "Increase total NAPFA score by X points",
                    "Get all components to Grade 3+"
                ]
                specific_goal = st.selectbox("Choose specific goal", specific_options)
                
                if "specific component" in specific_goal:
                    component = st.selectbox("Which component?", 
                                            ["Sit-Ups", "Standing Broad Jump", "Sit and Reach", 
                                             "Pull-Ups", "Shuttle Run", "2.4km Run"])
                    target_grade = 5
                elif "increase total" in specific_goal:
                    target_increase = st.number_input("Points to increase", min_value=1, max_value=10, value=3)
                
            elif goal_category == "Weight Management":
                current_weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=60.0)
                target_weight = st.number_input("Target Weight (kg)", min_value=30.0, max_value=150.0, value=58.0)
                specific_goal = f"Change weight from {current_weight}kg to {target_weight}kg"
                
            elif goal_category == "Strength Building":
                exercise = st.selectbox("Exercise", ["Push-ups", "Pull-ups", "Sit-ups", "Squats"])
                current_reps = st.number_input(f"Current max {exercise}", min_value=0, max_value=200, value=10)
                target_reps = st.number_input(f"Target {exercise}", min_value=0, max_value=200, value=20)
                specific_goal = f"Increase {exercise} from {current_reps} to {target_reps} reps"
                
            elif goal_category == "Endurance Training":
                distance = st.selectbox("Distance", ["1km", "2.4km", "5km", "10km"])
                current_time = st.text_input("Current time (min:sec)", value="10:00")
                target_time = st.text_input("Target time (min:sec)", value="9:00")
                specific_goal = f"Run {distance} from {current_time} to {target_time}"
                
            elif goal_category == "Flexibility":
                current_reach = st.number_input("Current Sit & Reach (cm)", min_value=0, max_value=100, value=30)
                target_reach = st.number_input("Target Sit & Reach (cm)", min_value=0, max_value=100, value=40)
                specific_goal = f"Improve flexibility from {current_reach}cm to {target_reach}cm"
                
            else:  # Consistency
                workout_days = st.number_input("Workouts per week", min_value=1, max_value=7, value=4)
                duration = st.number_input("For how many weeks?", min_value=1, max_value=52, value=8)
                specific_goal = f"Workout {workout_days} days/week for {duration} weeks"
            
            # Measurable
            st.write("#### 📊 Measurable - How will you track progress?")
            tracking_method = st.multiselect(
                "Tracking methods",
                ["Weekly NAPFA practice tests", "Daily workout logs", "Weekly measurements",
                 "Progress photos", "Performance records"],
                default=["Daily workout logs"]
            )
            
            # Achievable - AI calculates
            st.write("#### ✅ Achievable - Is this realistic?")
            
            # Calculate if goal is achievable based on current data
            timeline_weeks = st.slider("Timeline (weeks)", min_value=1, max_value=52, value=12)
            
            achievability = "Achievable"
            ai_feedback = ""
            
            if goal_category == "NAPFA Improvement":
                if user_data.get('napfa_history'):
                    current_napfa = user_data['napfa_history'][-1]['total']
                    if "Gold" in specific_goal and current_napfa < 15 and timeline_weeks < 12:
                        achievability = "Very Challenging"
                        ai_feedback = "⚠️ This is ambitious! Consider extending timeline to 16+ weeks."
                    elif current_napfa >= 18:
                        achievability = "Highly Achievable"
                        ai_feedback = "✅ Great goal! You're close to Gold already."
                    else:
                        ai_feedback = "✅ Realistic with consistent training!"
                        
            elif goal_category == "Weight Management":
                weight_change = abs(target_weight - current_weight)
                safe_rate = 0.5  # kg per week
                safe_weeks = weight_change / safe_rate
                
                if timeline_weeks < safe_weeks * 0.7:
                    achievability = "Too Aggressive"
                    ai_feedback = f"⚠️ Recommended timeline: {int(safe_weeks)} weeks for safe {weight_change}kg change"
                else:
                    ai_feedback = "✅ Safe and achievable rate!"
            
            st.info(f"**AI Assessment:** {achievability} - {ai_feedback}")
            
            # Relevant
            st.write("#### 🎯 Relevant - Why is this important to you?")
            motivation = st.text_area("Your motivation", 
                                     placeholder="e.g., I want to improve my fitness for school sports...")
            
            # Time-bound
            st.write("#### ⏰ Time-bound - When will you achieve this?")
            target_date = st.date_input("Target completion date", 
                                        value=datetime.now() + timedelta(weeks=timeline_weeks))
            
            # AI generates milestones
            st.write("### 📅 AI-Generated Weekly Milestones")
            
            weeks = (target_date - datetime.now().date()).days // 7
            if weeks > 0:
                st.write(f"**Timeline:** {weeks} weeks")
                
                # Generate milestones
                milestones = []
                
                if goal_category == "NAPFA Improvement" and "total" in specific_goal.lower():
                    if user_data.get('napfa_history'):
                        points_per_week = target_increase / weeks
                        current_score = user_data['napfa_history'][-1]['total']
                        
                        for week in range(1, min(weeks + 1, 9)):
                            milestone_score = current_score + (points_per_week * week)
                            milestones.append(f"**Week {week}:** Target score {milestone_score:.1f}/30")
                        
                elif goal_category == "Weight Management":
                    weight_per_week = (target_weight - current_weight) / weeks
                    
                    for week in range(1, min(weeks + 1, 9)):
                        milestone_weight = current_weight + (weight_per_week * week)
                        milestones.append(f"**Week {week}:** Target weight {milestone_weight:.1f}kg")
                        
                elif goal_category == "Strength Building":
                    reps_per_week = (target_reps - current_reps) / weeks
                    
                    for week in range(1, min(weeks + 1, 9)):
                        milestone_reps = int(current_reps + (reps_per_week * week))
                        milestones.append(f"**Week {week}:** Target {milestone_reps} {exercise}")
                
                for milestone in milestones:
                    st.write(milestone)
            
            # Save goal
            if st.button("💾 Save SMART Goal", type="primary"):
                smart_goal = {
                    'category': goal_category,
                    'specific': specific_goal,
                    'measurable': tracking_method,
                    'achievable': achievability,
                    'relevant': motivation,
                    'time_bound': target_date.strftime('%Y-%m-%d'),
                    'milestones': milestones,
                    'created_date': datetime.now().strftime('%Y-%m-%d'),
                    'progress': 0,
                    'weekly_checkpoints': []
                }
                
                user_data['smart_goals'].append(smart_goal)
                update_user_data(user_data)
                
                st.success("✅ SMART Goal created!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        
        with goal_tab2:
            st.write("### My Active SMART Goals")
            
            if not user_data['smart_goals']:
                st.info("No SMART goals yet. Create your first goal in the other tab!")
            else:
                for idx, goal in enumerate(user_data['smart_goals']):
                    with st.expander(f"🎯 {goal['specific']}", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Category:** {goal['category']}")
                            st.write(f"**Target Date:** {goal['time_bound']}")
                            st.write(f"**Created:** {goal['created_date']}")
                            st.write(f"**Achievability:** {goal['achievable']}")
                        
                        with col2:
                            st.write("**Tracking Methods:**")
                            for method in goal['measurable']:
                                st.write(f"• {method}")
                        
                        st.write("")
                        st.write(f"**Motivation:** {goal['relevant']}")
                        
                        # Progress tracking
                        st.write("")
                        st.write("### Progress Tracking")
                        
                        new_progress = st.slider(
                            "Update Progress",
                            min_value=0,
                            max_value=100,
                            value=goal['progress'],
                            key=f"progress_{idx}"
                        )
                        
                        if st.button("Update Progress", key=f"update_{idx}"):
                            user_data['smart_goals'][idx]['progress'] = new_progress
                            user_data['smart_goals'][idx]['weekly_checkpoints'].append({
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'progress': new_progress
                            })
                            update_user_data(user_data)
                            st.success("Progress updated!")
                            st.rerun()
                        
                        # Show milestones
                        if goal.get('milestones'):
                            st.write("")
                            st.write("**Weekly Milestones:**")
                            for milestone in goal['milestones']:
                                st.write(milestone)
                        
                        # Delete goal
                        if st.button("🗑️ Delete Goal", key=f"delete_{idx}"):
                            user_data['smart_goals'].pop(idx)
                            update_user_data(user_data)
                            st.rerun()
    
    
    with tab3:
        st.subheader("🗓️ Comprehensive AI Schedule Generator")
        st.write("Generate a complete personalized schedule based on your fitness data!")
        
        # Check if user has necessary data
        has_napfa = len(user_data.get('napfa_history', [])) > 0
        has_bmi = len(user_data.get('bmi_history', [])) > 0
        has_sleep = len(user_data.get('sleep_history', [])) > 0
        
        if not has_napfa or not has_bmi or not has_sleep:
            st.warning("⚠️ To generate a complete schedule, please complete:")
            if not has_napfa:
                st.write("- ❌ NAPFA Test")
            if not has_bmi:
                st.write("- ❌ BMI Calculation")
            if not has_sleep:
                st.write("- ❌ Sleep Tracking (at least 3 days)")
            st.info("Once you have this data, come back to generate your personalized schedule!")
        else:
            st.success("✅ All data available! Ready to generate your schedule.")
            
            # Get latest data
            latest_napfa = user_data['napfa_history'][-1]
            latest_bmi_record = user_data['bmi_history'][-1]
            latest_bmi = latest_bmi_record['bmi']
            
            # Calculate body type
            body_type, body_description = calculate_body_type(
                latest_bmi_record['weight'], 
                latest_bmi_record['height']
            )
            
            # Display current data
            st.write("### 📊 Your Current Data")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Latest BMI", f"{latest_bmi:.1f}")
                st.write(f"**Body Type:** {body_type}")
            with col2:
                st.metric("NAPFA Score", f"{latest_napfa['total']}/30")
                st.write(f"**Medal:** {latest_napfa['medal']}")
            with col3:
                sleep_week = [s for s in user_data['sleep_history'][-7:]]
                if sleep_week:
                    avg_sleep = sum([s['hours'] + s['minutes']/60 for s in sleep_week]) / len(sleep_week)
                    st.metric("Avg Sleep", f"{avg_sleep:.1f}h")
                    st.write(f"**Records:** {len(sleep_week)} days")
            
            st.write("---")
            
            # School schedule input
            st.write("### 🏫 Your School Schedule")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Weekdays**")
                weekday_start = st.time_input("School Start Time (Weekdays)", value=datetime.strptime("06:30", "%H:%M").time(), key="weekday_start")
                weekday_end = st.time_input("School End Time (Weekdays)", value=datetime.strptime("19:00", "%H:%M").time(), key="weekday_end")
            
            with col2:
                st.write("**Weekends**")
                weekend_schedule = st.radio("Weekend Schedule", 
                                           ["Full day available", "Half day (morning)", "Half day (afternoon)"],
                                           key="weekend_sched")
            
            # Generate button
            if st.button("🚀 Generate My Complete Schedule", type="primary"):
                st.write("---")
                st.success("✅ Your Personalized Schedule Generated!")
                
                # Analyze NAPFA weaknesses
                weak_stations = []
                for station, grade in latest_napfa['grades'].items():
                    if grade <= 2:  # D or E grade
                        weak_stations.append(station)
                
                # Determine focus areas
                focus_cardio = 'RUN' in weak_stations
                focus_strength = any(s in weak_stations for s in ['PU', 'SU'])
                focus_flexibility = 'SAR' in weak_stations
                
                # Weekly schedule
                st.write("### 📅 Your Weekly Training Schedule")
                
                schedule_data = {
                    "Monday": [],
                    "Tuesday": [],
                    "Wednesday": [],
                    "Thursday": [],
                    "Friday": [],
                    "Saturday": [],
                    "Sunday": []
                }
                
                # Build schedule based on analysis
                if focus_cardio:
                    schedule_data["Monday"].append({"time": "06:00-06:45", "activity": "🏃 Morning Run (2-3km)", "type": "Cardio"})
                    schedule_data["Wednesday"].append({"time": "17:30-18:15", "activity": "🏃 Interval Training", "type": "Cardio"})
                    schedule_data["Friday"].append({"time": "17:30-18:30", "activity": "🏃 Long Distance Run (3-4km)", "type": "Cardio"})
                
                if focus_strength:
                    schedule_data["Tuesday"].append({"time": "17:30-18:30", "activity": "💪 Upper Body: Pull-ups, Push-ups, Sit-ups", "type": "Strength"})
                    schedule_data["Thursday"].append({"time": "17:30-18:30", "activity": "💪 Core & Lower Body: Planks, Squats, Lunges", "type": "Strength"})
                    schedule_data["Saturday"].append({"time": "09:00-10:00", "activity": "💪 Full Body Circuit Training", "type": "Strength"})
                
                if focus_flexibility:
                    schedule_data["Monday"].append({"time": "19:30-20:00", "activity": "🧘 Stretching & Flexibility", "type": "Flexibility"})
                    schedule_data["Wednesday"].append({"time": "19:30-20:00", "activity": "🧘 Yoga/Stretching", "type": "Flexibility"})
                    schedule_data["Friday"].append({"time": "19:30-20:00", "activity": "🧘 Deep Stretching", "type": "Flexibility"})
                
                # Add general workouts if no specific weaknesses
                if not weak_stations:
                    schedule_data["Monday"].append({"time": "06:00-06:45", "activity": "🏃 Morning Run (3km)", "type": "Cardio"})
                    schedule_data["Tuesday"].append({"time": "17:30-18:30", "activity": "💪 Strength Training", "type": "Strength"})
                    schedule_data["Wednesday"].append({"time": "06:00-06:45", "activity": "🏃 Speed Work", "type": "Cardio"})
                    schedule_data["Thursday"].append({"time": "17:30-18:30", "activity": "💪 Core & Upper Body", "type": "Strength"})
                    schedule_data["Friday"].append({"time": "17:30-18:30", "activity": "🏃 Endurance Run", "type": "Cardio"})
                    schedule_data["Saturday"].append({"time": "09:00-10:00", "activity": "🧘 Flexibility & Recovery", "type": "Flexibility"})
                
                # Add rest day
                schedule_data["Sunday"].append({"time": "All Day", "activity": "😌 Rest & Recovery", "type": "Rest"})
                
                # Display schedule
                for day, activities in schedule_data.items():
                    if activities:
                        st.markdown(f"#### {day}")
                        for activity in activities:
                            activity_type = activity['type']
                            color = {
                                'Cardio': '#ff5722',
                                'Strength': '#2196f3', 
                                'Flexibility': '#4caf50',
                                'Rest': '#9e9e9e'
                            }.get(activity_type, '#607d8b')
                            
                            st.markdown(f"""
                            <div style="background: {color}; color: white; padding: 10px; border-radius: 8px; margin: 5px 0;">
                                <strong>{activity['time']}</strong><br>
                                {activity['activity']}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Diet recommendations
                st.write("---")
                st.write("### 🍽️ Nutrition Plan")
                
                if latest_bmi < 18.5:
                    st.info("**Goal:** Healthy weight gain with muscle building")
                    st.write("""
                    - **Daily Calories:** 2,800-3,200 kcal
                    - **Protein:** 1.8-2.2g per kg body weight
                    - **Meals:** 5-6 small meals throughout the day
                    - **Focus:** Lean proteins, complex carbs, healthy fats
                    """)
                elif latest_bmi > 25:
                    st.info("**Goal:** Healthy weight loss with muscle preservation")
                    st.write("""
                    - **Daily Calories:** 1,800-2,200 kcal
                    - **Protein:** 1.6-2.0g per kg body weight
                    - **Meals:** 4-5 balanced meals
                    - **Focus:** High protein, moderate carbs, healthy fats
                    """)
                else:
                    st.info("**Goal:** Maintain weight and build fitness")
                    st.write("""
                    - **Daily Calories:** 2,200-2,600 kcal
                    - **Protein:** 1.6-1.8g per kg body weight
                    - **Meals:** 4-5 balanced meals
                    - **Focus:** Balanced macros, nutrient-dense foods
                    """)
                
                # Sleep recommendations
                st.write("---")
                st.write("### 😴 Sleep Schedule")
                
                if avg_sleep < 8:
                    st.warning(f"⚠️ You're averaging {avg_sleep:.1f}h - aim for 8-10h for teens!")
                    st.write("""
                    **Target:** 8-10 hours per night
                    - **Bedtime:** 22:00-22:30
                    - **Wake time:** 06:00-06:30
                    - **Pre-bed routine:** No screens 1hr before, light stretching
                    - **Weekend:** Keep similar schedule (±1 hour)
                    """)
                else:
                    st.success(f"✅ Great sleep average: {avg_sleep:.1f}h - keep it up!")
                    st.write("""
                    **Target:** Maintain 8-10 hours per night
                    - **Bedtime:** 22:00-22:30
                    - **Wake time:** 06:00-06:30
                    - **Keep consistent schedule** on weekends too
                    """)
                
                # Specific recommendations based on weaknesses
                if weak_stations:
                    st.write("---")
                    st.write("### 🎯 Focus Areas (Based on NAPFA Weaknesses)")
                    
                    station_names = {
                        'SU': 'Sit-ups',
                        'SBJ': 'Standing Broad Jump',
                        'SAR': 'Sit & Reach',
                        'PU': 'Pull-ups',
                        'SR': 'Shuttle Run',
                        'RUN': '2.4km Run'
                    }
                    
                    for station in weak_stations:
                        st.write(f"**{station_names.get(station, station)}** - Grade {['F', 'E', 'D', 'C', 'B', 'A'][latest_napfa['grades'].get(station, 0)]}")
                    
                    st.info("💡 Your training schedule above is customized to improve these areas. Stay consistent!")
                
                st.write("---")
                st.success("💪 Schedule generated! Track your progress in the Exercise Log and NAPFA Test sections.")
    
    with tab4:
        st.subheader("🍳 Health Recipes Database")
        st.write("Healthy recipes tailored to your fitness goals!")
        
        # Recipe categories
        st.write("### Select Your Dietary Goal")
        
        diet_type = st.selectbox(
            "Choose goal",
            ["Weight Loss", "Muscle Gain", "Maintenance"]
        )
        
        # Get recipes
        all_recipes = search_recipes_by_diet(diet_type)
        
        if diet_type in all_recipes:
            recipes = all_recipes[diet_type]
            
            st.write(f"### 🍽️ {diet_type} Recipes ({len(recipes)} recipes)")
            
            for recipe in recipes:
                with st.expander(f"📖 {recipe['name']}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Nutritional Info:**")
                        st.write(f"- Calories: {recipe['calories']} kcal")
                        st.write(f"- Protein: {recipe['protein']}")
                        st.write(f"- Carbs: {recipe['carbs']}")
                        st.write(f"- Prep Time: {recipe['prep_time']}")
                    
                    with col2:
                        st.write("**Meal Type:**")
                        if recipe['calories'] < 300:
                            st.write("🥗 Snack/Light meal")
                        elif recipe['calories'] < 450:
                            st.write("🍽️ Main meal")
                        else:
                            st.write("🍖 Post-workout meal")
                    
                    st.write("")
                    st.write("**Ingredients:**")
                    for ingredient in recipe['ingredients']:
                        st.write(f"• {ingredient}")
                    
                    st.write("")
                    st.write("**Instructions:**")
                    st.write(recipe['instructions'])
        else:
            st.info("No recipes found. Select a dietary goal above.")
        
        st.write("---")
        st.info("💡 **Tip:** These recipes align with your fitness goals. Mix and match to create variety in your diet!")

def reminders_and_progress():
    st.header("📊 Weekly Progress Report")
    
    user_data = get_user_data()
    
    # Quick Stats Widget (Phase 7 BONUS!)
    st.markdown("### ⚡ Quick Stats")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_workouts = len(user_data.get('exercises', []))
        st.metric("💪 Total Workouts", total_workouts)
    
    with col2:
        house_points = user_data.get('house_points_contributed', 0)
        st.metric("🏠 House Points", f"{house_points:.1f}")
    
    with col3:
        total_badges = len(user_data.get('badges', []))
        st.metric("🎖️ Badges", total_badges)
    
    with col4:
        level = user_data.get('level', 'Novice')
        st.metric("⭐ Level", level)
    
    with col5:
        streak = user_data.get('login_streak', 0)
        st.metric("🔥 Streak", f"{streak} days")
    
    # Show progress bar for current level
    total_points = user_data.get('total_points', 0)
    level_name, min_points, max_points = calculate_level(total_points)
    
    if max_points > min_points:
        progress = min(100, ((total_points - min_points) / (max_points - min_points)) * 100)
        st.progress(progress / 100)
        st.caption(f"🎯 {total_points} / {max_points} points to next level")
    
    st.write("---")
    
    # Reminder Bar at the top
    st.markdown("### 🔔 Today's Reminders")
    
    today = datetime.now().strftime('%A')
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Check scheduled activities for today
    today_activities = [s for s in user_data.get('schedule', []) if s['day'] == today]
    
    if today_activities:
        for activity in today_activities:
            st.info(f"⏰ **Today:** {activity['activity']} - {activity['time']} ({activity['duration']} min)")
    else:
        st.success(f"✅ No workouts scheduled for {today}. Good rest day or add a session!")
    
    # Smart reminders based on data
    reminders = []
    
    # Check last NAPFA test
    if user_data.get('napfa_history'):
        last_napfa_date = datetime.strptime(user_data['napfa_history'][-1]['date'], '%Y-%m-%d')
        days_since_napfa = (datetime.now() - last_napfa_date).days
        if days_since_napfa > 30:
            reminders.append(f"📝 It's been {days_since_napfa} days since your last NAPFA test. Consider retesting to track progress!")
    
    # Check last BMI
    if user_data.get('bmi_history'):
        last_bmi_date = datetime.strptime(user_data['bmi_history'][-1]['date'], '%Y-%m-%d')
        days_since_bmi = (datetime.now() - last_bmi_date).days
        if days_since_bmi > 14:
            reminders.append(f"⚖️ Update your BMI - last recorded {days_since_bmi} days ago")
    
    # Check sleep tracking
    if user_data.get('sleep_history'):
        last_sleep_date = datetime.strptime(user_data['sleep_history'][-1]['date'], '%Y-%m-%d')
        if last_sleep_date.strftime('%Y-%m-%d') != today_date:
            reminders.append("😴 Don't forget to log your sleep from last night!")
    else:
        reminders.append("😴 Start tracking your sleep for better recovery insights!")
    
    # Check exercise logging
    if user_data.get('exercises'):
        last_exercise_date = datetime.strptime(user_data['exercises'][0]['date'], '%Y-%m-%d')
        days_since_exercise = (datetime.now() - last_exercise_date).days
        if days_since_exercise > 2:
            reminders.append(f"💪 It's been {days_since_exercise} days since your last logged workout. Time to get moving!")
    else:
        reminders.append("💪 Start logging your exercises to track your fitness journey!")
    
    # Check goals progress
    if user_data.get('goals'):
        for goal in user_data['goals']:
            target_date = datetime.strptime(goal['date'], '%Y-%m-%d')
            days_until = (target_date - datetime.now()).days
            if 0 <= days_until <= 7:
                reminders.append(f"🎯 Goal deadline approaching: '{goal['target']}' in {days_until} days!")
    
    if reminders:
        st.markdown("### 💡 Smart Reminders")
        for reminder in reminders:
            st.warning(reminder)
    
    st.write("---")
    
    # Weekly Progress Report
    st.markdown("### 📈 Your Weekly Summary")
    
    # Calculate date range
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    # Create tabs for different metrics
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏃 NAPFA Progress", "💪 Exercise Stats", "😴 Sleep Analysis"])
    
    with tab1:
        st.subheader("This Week at a Glance")
        
        # Count activities this week
        exercises_this_week = [e for e in user_data.get('exercises', []) 
                              if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
        
        sleep_this_week = [s for s in user_data.get('sleep_history', []) 
                          if datetime.strptime(s['date'], '%Y-%m-%d') >= week_ago]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Workouts Logged", len(exercises_this_week))
        with col2:
            if exercises_this_week:
                total_mins = sum([e['duration'] for e in exercises_this_week])
                st.metric("Total Exercise", f"{total_mins} min")
            else:
                st.metric("Total Exercise", "0 min")
        with col3:
            st.metric("Sleep Tracked", len(sleep_this_week))
        with col4:
            if sleep_this_week:
                avg_sleep = sum([s['hours'] + s['minutes']/60 for s in sleep_this_week]) / len(sleep_this_week)
                st.metric("Avg Sleep", f"{avg_sleep:.1f}h")
            else:
                st.metric("Avg Sleep", "No data")
        
        # All-time stats
        st.write("")
        st.markdown("#### 📚 All-Time Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Workouts", len(user_data.get('exercises', [])))
        with col2:
            st.metric("NAPFA Tests", len(user_data.get('napfa_history', [])))
        with col3:
            st.metric("BMI Records", len(user_data.get('bmi_history', [])))
        with col4:
            st.metric("Active Goals", len(user_data.get('goals', [])))
        
        # Workout consistency
        if user_data.get('exercises'):
            st.write("")
            st.markdown("#### 🔥 Workout Consistency")
            
            # Get unique workout dates
            workout_dates = list(set([e['date'] for e in user_data.get('exercises', [])]))
            workout_dates.sort(reverse=True)
            
            if len(workout_dates) >= 2:
                # Calculate streak
                streak = 1
                current_date = datetime.strptime(workout_dates[0], '%Y-%m-%d')
                
                for i in range(1, len(workout_dates)):
                    prev_date = datetime.strptime(workout_dates[i], '%Y-%m-%d')
                    diff = (current_date - prev_date).days
                    
                    if diff <= 2:  # Allow 1 rest day
                        streak += 1
                        current_date = prev_date
                    else:
                        break
                
                if streak >= 3:
                    st.success(f"🔥 {streak} day streak! Keep it up!")
                else:
                    st.info(f"Current streak: {streak} days. Aim for 3+ for consistency!")
    
    with tab4:
        st.subheader("🏃 NAPFA Performance")
        
        if not user_data.get('napfa_history'):
            st.info("No NAPFA tests recorded yet. Complete your first test to track progress!")
        else:
            napfa_data = user_data['napfa_history']
            
            # Show latest scores
            latest = napfa_data[-1]
            st.write(f"**Latest Test:** {latest['date']}")
            st.write(f"**Total Score:** {latest['total']} points")
            st.write(f"**Medal:** {latest['medal']}")
            
            # Show grades breakdown
            test_names = {
                'SU': 'Sit-Ups',
                'SBJ': 'Standing Broad Jump',
                'SAR': 'Sit and Reach',
                'PU': 'Pull-Ups',
                'SR': 'Shuttle Run',
                'RUN': '2.4km Run'
            }
            
            st.write("")
            st.write("**Grade Breakdown:**")
            
            grades_df = pd.DataFrame([
                {
                    'Test': test_names[test],
                    'Score': latest['scores'][test],
                    'Grade': grade
                }
                for test, grade in latest['grades'].items()
            ])
            
            st.dataframe(grades_df, use_container_width=True, hide_index=True)
            
            # Progress over time
            if len(napfa_data) > 1:
                st.write("")
                st.write("**Progress Over Time:**")
                
                df = pd.DataFrame([
                    {'Date': test['date'], 'Total Score': test['total']}
                    for test in napfa_data
                ])
                df = df.set_index('Date')
                st.line_chart(df)
                
                # Calculate improvement
                first_score = napfa_data[0]['total']
                latest_score = napfa_data[-1]['total']
                improvement = latest_score - first_score
                
                if improvement > 0:
                    st.success(f"📈 You've improved by {improvement} points since your first test!")
                elif improvement < 0:
                    st.warning(f"📉 Score decreased by {abs(improvement)} points. Review your training plan.")
                else:
                    st.info("Score unchanged. Time to push harder!")
    
    with tab3:
        st.subheader("💪 Exercise Statistics")
        
        if not user_data.get('exercises'):
            st.info("No exercises logged yet. Start logging your workouts!")
        else:
            exercises = user_data['exercises']
            
            # Total stats
            total_workouts = len(exercises)
            total_minutes = sum([e['duration'] for e in exercises])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Workouts", total_workouts)
            with col2:
                st.metric("Total Time", f"{total_minutes} min ({total_minutes/60:.1f} hrs)")
            
            # Exercise frequency
            st.write("")
            st.write("**Exercise Frequency:**")
            exercise_counts = {}
            for ex in exercises:
                exercise_counts[ex['name']] = exercise_counts.get(ex['name'], 0) + 1
            
            df_chart = pd.DataFrame({
                'Exercise': list(exercise_counts.keys()),
                'Count': list(exercise_counts.values())
            }).sort_values('Count', ascending=False)
            
            df_chart = df_chart.set_index('Exercise')
            st.bar_chart(df_chart)
            
            # Intensity breakdown
            st.write("")
            st.write("**Intensity Distribution:**")
            intensity_counts = {'Low': 0, 'Medium': 0, 'High': 0}
            for ex in exercises:
                intensity_counts[ex['intensity']] += 1
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Low Intensity", intensity_counts['Low'])
            with col2:
                st.metric("Medium Intensity", intensity_counts['Medium'])
            with col3:
                st.metric("High Intensity", intensity_counts['High'])
            
            # Recent workouts
            st.write("")
            st.write("**Recent Workouts:**")
            recent = exercises[:5]  # Last 5
            for ex in recent:
                st.write(f"• {ex['date']}: {ex['name']} - {ex['duration']}min ({ex['intensity']} intensity)")
    
    with tab4:
        st.subheader("😴 Sleep Analysis")
        
        if not user_data.get('sleep_history'):
            st.info("No sleep data yet. Start tracking your sleep!")
        else:
            sleep_data = user_data['sleep_history']
            
            # Calculate stats
            total_records = len(sleep_data)
            avg_hours = sum([s['hours'] + s['minutes']/60 for s in sleep_data]) / total_records
            
            quality_counts = {'Excellent': 0, 'Good': 0, 'Fair': 0, 'Poor': 0}
            for s in sleep_data:
                quality_counts[s['quality']] += 1
            
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Average Sleep", f"{avg_hours:.1f} hours")
            with col2:
                st.metric("Records Tracked", total_records)
            
            # Quality breakdown
            st.write("")
            st.write("**Sleep Quality Distribution:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("😊 Excellent", quality_counts['Excellent'])
            with col2:
                st.metric("👍 Good", quality_counts['Good'])
            with col3:
                st.metric("😐 Fair", quality_counts['Fair'])
            with col4:
                st.metric("😴 Poor", quality_counts['Poor'])
            
            # Sleep trend
            if len(sleep_data) > 1:
                st.write("")
                st.write("**Sleep Duration Trend:**")
                df = pd.DataFrame(sleep_data)
                df['total_hours'] = df['hours'] + df['minutes'] / 60
                df_chart = df.set_index('date')['total_hours']
                st.line_chart(df_chart)
            
            # Sleep insights
            st.write("")
            st.write("**Insights:**")
            if avg_hours >= 8:
                st.success("✅ Excellent sleep habits! Keep it up for optimal recovery and performance.")
            elif avg_hours >= 7:
                st.info("👍 Good sleep duration. Try to get closer to 8-10 hours for peak performance.")
            else:
                st.warning("⚠️ You're not getting enough sleep. Aim for 8-10 hours for teenagers!")
            
            # Best and worst
            if len(sleep_data) >= 3:
                sleep_sorted = sorted(sleep_data, key=lambda x: x['hours'] + x['minutes']/60, reverse=True)
                best = sleep_sorted[0]
                worst = sleep_sorted[-1]
                
                st.write(f"**Best night:** {best['date']} - {best['hours']}h {best['minutes']}m")
                st.write(f"**Shortest night:** {worst['date']} - {worst['hours']}h {worst['minutes']}m")

# Advanced Health Metrics
def advanced_metrics():
    st.header("🏥 Advanced Health Metrics")
    st.write("Track detailed health and fitness metrics")
    
    user_data = get_user_data()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔥 BMR & Calories",
        "❤️ Heart Rate Zones",
        "💧 Hydration Tracker",
        "📐 Body Composition"
    ])
    
    with tab1:
        st.subheader("🔥 Basal Metabolic Rate (BMR) Calculator")
        st.write("Calculate your daily calorie needs")
        
        # Get user data
        if user_data.get('bmi_history'):
            latest_bmi = user_data['bmi_history'][-1]
            default_weight = latest_bmi['weight']
            default_height = latest_bmi['height'] * 100  # Convert to cm
        else:
            default_weight = 60.0
            default_height = 165.0
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, 
                                    value=float(default_weight), step=0.1, key="bmr_weight")
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                    value=float(default_height), step=0.5, key="bmr_height")
        
        with col2:
            age = user_data.get('age', 14)
            gender = user_data.get('gender', 'm')
            
            st.metric("Age", age)
            st.metric("Gender", "Male" if gender == 'm' else "Female")
        
        activity_level = st.selectbox(
            "Activity Level",
            [
                "Sedentary (little/no exercise)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)",
                "Extremely Active (athlete, 2x/day)"
            ],
            index=2
        )
        
        if st.button("Calculate BMR & Calories", type="primary"):
            # Mifflin-St Jeor Equation (most accurate for teens)
            if gender == 'm':
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
            
            # Activity multipliers
            activity_multipliers = {
                "Sedentary (little/no exercise)": 1.2,
                "Lightly Active (1-3 days/week)": 1.375,
                "Moderately Active (3-5 days/week)": 1.55,
                "Very Active (6-7 days/week)": 1.725,
                "Extremely Active (athlete, 2x/day)": 1.9
            }
            
            multiplier = activity_multipliers[activity_level]
            tdee = bmr * multiplier  # Total Daily Energy Expenditure
            
            # Calculate macros
            protein_grams = weight * 1.6  # 1.6g per kg for active teens
            protein_cals = protein_grams * 4
            
            fat_cals = tdee * 0.25  # 25% from fat
            fat_grams = fat_cals / 9
            
            carb_cals = tdee - protein_cals - fat_cals
            carb_grams = carb_cals / 4
            
            # Display results
            st.write("---")
            st.write("### Your Metabolic Profile")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("BMR", f"{bmr:.0f} cal/day")
                st.write("*Calories burned at rest*")
            
            with col2:
                st.metric("TDEE", f"{tdee:.0f} cal/day")
                st.write("*Total daily calories needed*")
            
            with col3:
                calories_per_workout = 300  # Average
                workout_days = 4  # Estimate
                weekly_exercise_cals = calories_per_workout * workout_days
                st.metric("Exercise Burns", f"{weekly_exercise_cals:.0f} cal/week")
            
            # Goals-based recommendations
            st.write("")
            st.write("### Calorie Targets by Goal")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="stat-card" style="background: #f44336; color: white;">
                    <h3>💪 Weight Loss</h3>
                    <h2>{:.0f} cal/day</h2>
                    <p>Deficit: -500 cal/day</p>
                    <p>Rate: -0.5kg/week</p>
                </div>
                """.format(tdee - 500), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="stat-card" style="background: #4caf50; color: white;">
                    <h3>⚖️ Maintenance</h3>
                    <h2>{:.0f} cal/day</h2>
                    <p>No deficit/surplus</p>
                    <p>Maintain weight</p>
                </div>
                """.format(tdee), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="stat-card" style="background: #2196f3; color: white;">
                    <h3>🏋️ Muscle Gain</h3>
                    <h2>{:.0f} cal/day</h2>
                    <p>Surplus: +300 cal/day</p>
                    <p>Rate: +0.25kg/week</p>
                </div>
                """.format(tdee + 300), unsafe_allow_html=True)
            
            # Macronutrients
            st.write("")
            st.write("### Recommended Macronutrients")
            
            st.write(f"**For your activity level ({activity_level}):**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Protein", f"{protein_grams:.0f}g/day")
                st.write(f"({protein_cals:.0f} cal)")
                st.progress(protein_cals / tdee)
            
            with col2:
                st.metric("Carbs", f"{carb_grams:.0f}g/day")
                st.write(f"({carb_cals:.0f} cal)")
                st.progress(carb_cals / tdee)
            
            with col3:
                st.metric("Fats", f"{fat_grams:.0f}g/day")
                st.write(f"({fat_cals:.0f} cal)")
                st.progress(fat_cals / tdee)
            
            # Save to user data
            if 'bmr_history' not in user_data:
                user_data['bmr_history'] = []
            
            user_data['bmr_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'bmr': round(bmr),
                'tdee': round(tdee),
                'weight': weight,
                'height': height,
                'activity_level': activity_level
            })
            update_user_data(user_data)
    
    with tab2:
        st.subheader("❤️ Heart Rate Training Zones")
        st.write("Optimize your training with heart rate zones")
        
        # Calculate max heart rate
        age = user_data.get('age', 14)
        max_hr = 220 - age
        
        # Resting heart rate input
        st.write("### Calculate Your Training Zones")
        
        resting_hr = st.number_input(
            "Resting Heart Rate (bpm)",
            min_value=40,
            max_value=100,
            value=70,
            help="Measure first thing in the morning before getting out of bed"
        )
        
        # Heart Rate Reserve method (Karvonen Formula)
        hr_reserve = max_hr - resting_hr
        
        # Define zones
        zones = {
            "Zone 1 - Very Light": {
                "range": (0.50, 0.60),
                "description": "Recovery, warm-up",
                "benefits": "Promotes recovery, builds base endurance",
                "duration": "Long (45-60+ min)",
                "color": "#90caf9"
            },
            "Zone 2 - Light": {
                "range": (0.60, 0.70),
                "description": "Fat burning, base training",
                "benefits": "Builds aerobic base, burns fat",
                "duration": "Moderate-Long (30-60 min)",
                "color": "#81c784"
            },
            "Zone 3 - Moderate": {
                "range": (0.70, 0.80),
                "description": "Aerobic endurance",
                "benefits": "Improves cardiovascular fitness",
                "duration": "Moderate (20-40 min)",
                "color": "#fff176"
            },
            "Zone 4 - Hard": {
                "range": (0.80, 0.90),
                "description": "Lactate threshold",
                "benefits": "Increases NAPFA performance, speed",
                "duration": "Short-Moderate (10-30 min)",
                "color": "#ffb74d"
            },
            "Zone 5 - Maximum": {
                "range": (0.90, 1.00),
                "description": "VO2 Max, sprints",
                "benefits": "Max power, NAPFA 2.4km final sprint",
                "duration": "Very Short (1-5 min intervals)",
                "color": "#e57373"
            }
        }
        
        st.write("")
        st.write(f"### Your Heart Rate Zones (Max HR: {max_hr} bpm)")
        
        for zone_name, zone_info in zones.items():
            min_percent, max_percent = zone_info['range']
            min_hr = int(resting_hr + (hr_reserve * min_percent))
            max_hr_zone = int(resting_hr + (hr_reserve * max_percent))
            
            with st.expander(f"{zone_name}: {min_hr}-{max_hr_zone} bpm", expanded=True):
                st.markdown(f"""
                <div class="stat-card" style="background: {zone_info['color']};">
                    <h3>{zone_info['description']}</h3>
                    <h2>{min_hr} - {max_hr_zone} bpm</h2>
                    <p><strong>Benefits:</strong> {zone_info['benefits']}</p>
                    <p><strong>Duration:</strong> {zone_info['duration']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # NAPFA-specific recommendations
        st.write("")
        st.write("### 🏃 NAPFA Training Recommendations")
        
        st.info("""
        **For 2.4km Run:**
        - Zone 2-3: 70% of training (build endurance)
        - Zone 4: 20% of training (improve speed)
        - Zone 5: 10% of training (final sprint power)
        
        **For Shuttle Run:**
        - Zone 4-5: High-intensity intervals
        - 30 sec sprints, 90 sec rest
        
        **For Recovery:**
        - Zone 1: Active recovery days
        - Light jogging or walking
        """)
        
        # Save resting HR
        if 'heart_rate_data' not in user_data:
            user_data['heart_rate_data'] = []
        
        if st.button("Save Resting HR"):
            user_data['heart_rate_data'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'resting_hr': resting_hr,
                'max_hr': max_hr
            })
            update_user_data(user_data)
            st.success("Resting heart rate saved!")
    
    with tab3:
        st.subheader("💧 Hydration Calculator & Tracker")
        st.write("Stay properly hydrated for optimal performance")
        
        # Calculate daily hydration needs
        st.write("### Daily Hydration Needs")
        
        if user_data.get('bmi_history'):
            weight = user_data['bmi_history'][-1]['weight']
        else:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, value=60.0)
        
        # Calculate exercises today
        today = datetime.now().strftime('%Y-%m-%d')
        today_exercises = [e for e in user_data.get('exercises', []) if e['date'] == today]
        workout_duration = sum(e['duration'] for e in today_exercises)
        
        # Base hydration (30-35 ml per kg)
        base_hydration = weight * 35  # ml
        
        # Add for exercise (500-1000ml per hour)
        exercise_hydration = (workout_duration / 60) * 750  # ml
        
        # Add for climate (if hot, +500ml)
        climate_bonus = 0  # We'll let them select
        
        st.write("**Factors:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Base Need", f"{base_hydration:.0f} ml")
            st.write(f"({weight} kg × 35 ml)")
        
        with col2:
            st.metric("Exercise Bonus", f"+{exercise_hydration:.0f} ml")
            st.write(f"({workout_duration} min workout)")
        
        climate = st.selectbox(
            "Climate/Temperature",
            ["Cool (<25°C)", "Moderate (25-30°C)", "Hot (>30°C)"]
        )
        
        if "Moderate" in climate:
            climate_bonus = 500
        elif "Hot" in climate:
            climate_bonus = 1000
        
        total_hydration = base_hydration + exercise_hydration + climate_bonus
        
        st.write("")
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, {SST_COLORS['blue']} 0%, #1565c0 100%); color: white;">
            <h2>💧 Total Daily Target</h2>
            <h1>{total_hydration:.0f} ml</h1>
            <h3>({total_hydration/1000:.1f} liters)</h3>
            <p>≈ {total_hydration/250:.0f} glasses (250ml each)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hydration tracker
        st.write("")
        st.write("### Track Today's Intake")
        
        # Initialize today's hydration
        if 'hydration_log' not in user_data:
            user_data['hydration_log'] = []
        
        today_log = [h for h in user_data['hydration_log'] if h['date'] == today]
        current_intake = sum(h['amount'] for h in today_log)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.progress(min(current_intake / total_hydration, 1.0))
            st.write(f"**Progress:** {current_intake:.0f} / {total_hydration:.0f} ml ({(current_intake/total_hydration*100):.0f}%)")
        
        with col2:
            remaining = max(0, total_hydration - current_intake)
            st.metric("Remaining", f"{remaining:.0f} ml")
        
        # Quick add buttons
        st.write("**Quick Add:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💧 Glass (250ml)"):
                user_data['hydration_log'].append({
                    'date': today,
                    'time': datetime.now().strftime('%H:%M'),
                    'amount': 250
                })
                update_user_data(user_data)
                st.rerun()
        
        with col2:
            if st.button("🥤 Bottle (500ml)"):
                user_data['hydration_log'].append({
                    'date': today,
                    'time': datetime.now().strftime('%H:%M'),
                    'amount': 500
                })
                update_user_data(user_data)
                st.rerun()
        
        with col3:
            if st.button("🧃 Large (750ml)"):
                user_data['hydration_log'].append({
                    'date': today,
                    'time': datetime.now().strftime('%H:%M'),
                    'amount': 750
                })
                update_user_data(user_data)
                st.rerun()
        
        with col4:
            if st.button("💧 Custom"):
                custom_amount = st.number_input("Amount (ml)", min_value=0, max_value=2000, value=250, step=50)
                if st.button("Add Custom"):
                    user_data['hydration_log'].append({
                        'date': today,
                        'time': datetime.now().strftime('%H:%M'),
                        'amount': custom_amount
                    })
                    update_user_data(user_data)
                    st.rerun()
        
        # Today's log
        if today_log:
            st.write("")
            st.write("**Today's Log:**")
            for log in reversed(today_log):
                st.write(f"• {log['time']} - {log['amount']} ml")
        
        # Hydration tips
        st.write("")
        st.info("""
        **💡 Hydration Tips:**
        - Drink before you feel thirsty
        - Hydrate 2 hours before exercise
        - Drink 150-250ml every 15-20 min during exercise
        - Rehydrate after exercise (1.5x fluid lost)
        - Urine should be light yellow (not clear, not dark)
        - Avoid sugary drinks - water is best
        """)
    
    with tab4:
        st.subheader("📐 Body Composition Analyzer")
        st.write("Estimate body fat percentage using the Navy Method")
        
        # Get user data
        user_data = get_user_data()
        age = user_data.get('age', 14)
        gender = user_data.get('gender', 'm')
        
        if user_data.get('bmi_history'):
            latest_bmi = user_data['bmi_history'][-1]
            default_weight = latest_bmi['weight']
            default_height = latest_bmi['height'] * 100  # Convert to cm
        else:
            default_weight = 60.0
            default_height = 165.0
        
        st.write("### Body Measurements")
        st.info("💡 **Tip:** Use a measuring tape and measure at the widest/thickest point. Take measurements in the morning for consistency.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Basic Info**")
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, 
                                    value=float(default_weight), step=0.1, key="comp_weight")
            height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                       value=float(default_height), step=0.5, key="comp_height")
            
            st.metric("Age", age)
            st.metric("Gender", "Male" if gender == 'm' else "Female")
        
        with col2:
            st.write("**Circumference Measurements (cm)**")
            neck = st.number_input("Neck circumference", min_value=20.0, max_value=60.0, 
                                  value=35.0, step=0.5,
                                  help="Measure just below the larynx (Adam's apple)")
            waist = st.number_input("Waist circumference", min_value=40.0, max_value=150.0, 
                                   value=75.0, step=0.5,
                                   help="Measure at the narrowest point, usually at belly button level")
            
            if gender == 'f':
                hip = st.number_input("Hip circumference", min_value=50.0, max_value=180.0, 
                                     value=95.0, step=0.5,
                                     help="Measure at the widest point of the hips")
        
        if st.button("Calculate Body Composition", type="primary"):
            # Navy Method formulas
            if gender == 'm':
                # Male formula
                body_fat_pct = (495 / (1.0324 - 0.19077 * np.log10(waist - neck) + 0.15456 * np.log10(height_cm))) - 450
            else:
                # Female formula
                body_fat_pct = (495 / (1.29579 - 0.35004 * np.log10(waist + hip - neck) + 0.22100 * np.log10(height_cm))) - 450
            
            # Calculate fat mass and lean mass
            fat_mass = (body_fat_pct / 100) * weight
            lean_mass = weight - fat_mass
            
            # Determine category based on age and gender
            if gender == 'm':
                if body_fat_pct < 6:
                    category = "Essential Fat Only"
                    color = "#2196f3"
                    desc = "⚠️ Too low - health risks"
                elif body_fat_pct < 14:
                    category = "Athletes"
                    color = "#4caf50"
                    desc = "✅ Athletic/Fit"
                elif body_fat_pct < 18:
                    category = "Fitness"
                    color = "#8bc34a"
                    desc = "✅ Good fitness level"
                elif body_fat_pct < 25:
                    category = "Average"
                    color = "#ffc107"
                    desc = "📊 Average range"
                else:
                    category = "Above Average"
                    color = "#ff9800"
                    desc = "⚠️ Consider reducing"
            else:
                if body_fat_pct < 14:
                    category = "Essential Fat Only"
                    color = "#2196f3"
                    desc = "⚠️ Too low - health risks"
                elif body_fat_pct < 21:
                    category = "Athletes"
                    color = "#4caf50"
                    desc = "✅ Athletic/Fit"
                elif body_fat_pct < 25:
                    category = "Fitness"
                    color = "#8bc34a"
                    desc = "✅ Good fitness level"
                elif body_fat_pct < 32:
                    category = "Average"
                    color = "#ffc107"
                    desc = "📊 Average range"
                else:
                    category = "Above Average"
                    color = "#ff9800"
                    desc = "⚠️ Consider reducing"
            
            # Display results
            st.write("---")
            st.write("### Your Body Composition")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card" style="background: {color}; color: white;">
                    <h3>Body Fat %</h3>
                    <h1>{body_fat_pct:.1f}%</h1>
                    <p><strong>{category}</strong></p>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Fat Mass", f"{fat_mass:.1f} kg")
                st.write(f"{(fat_mass/weight*100):.1f}% of body weight")
            
            with col3:
                st.metric("Lean Mass", f"{lean_mass:.1f} kg")
                st.write(f"{(lean_mass/weight*100):.1f}% of body weight")
            
            # Body composition breakdown chart
            st.write("")
            st.write("### Composition Breakdown")
            
            comp_data = pd.DataFrame({
                'Component': ['Fat Mass', 'Lean Mass'],
                'Weight (kg)': [fat_mass, lean_mass],
                'Percentage': [body_fat_pct, 100-body_fat_pct]
            })
            
            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(comp_data.set_index('Component')['Weight (kg)'])
            with col2:
                st.dataframe(comp_data, use_container_width=True)
            
            # Reference ranges
            st.write("")
            st.write("### 📊 Reference Ranges by Category")
            
            if gender == 'm':
                ref_data = {
                    'Category': ['Essential Fat', 'Athletes', 'Fitness', 'Average', 'Above Average'],
                    'Male (%)': ['2-5%', '6-13%', '14-17%', '18-24%', '25%+']
                }
            else:
                ref_data = {
                    'Category': ['Essential Fat', 'Athletes', 'Fitness', 'Average', 'Above Average'],
                    'Female (%)': ['10-13%', '14-20%', '21-24%', '25-31%', '32%+']
                }
            
            st.table(pd.DataFrame(ref_data))
            
            # Recommendations
            st.write("")
            st.write("### 💡 Personalized Recommendations")
            
            if body_fat_pct < (6 if gender == 'm' else 14):
                st.warning("""
                **⚠️ Body Fat Too Low**
                - Increase calorie intake
                - Focus on healthy fats (nuts, avocado, olive oil)
                - Reduce intense cardio, increase strength training
                - Consult with a healthcare provider
                """)
            elif body_fat_pct > (25 if gender == 'm' else 32):
                st.info("""
                **🎯 Body Fat Reduction Tips**
                - Create moderate calorie deficit (300-500 cal/day)
                - Increase protein intake (1.6-2.0g per kg)
                - Combine cardio (3-4x/week) with strength training (3x/week)
                - Focus on NAPFA training for functional fitness
                - Track food intake for 2 weeks to identify patterns
                """)
            else:
                st.success("""
                **✅ Healthy Range - Maintenance Tips**
                - Continue current training routine
                - Maintain balanced diet
                - Focus on NAPFA performance improvements
                - Build muscle through strength training
                - Monitor every 4-6 weeks for changes
                """)
            
            # NAPFA correlation
            st.write("")
            st.write("### 🏃 Impact on NAPFA Performance")
            
            st.info("""
            **Body composition affects NAPFA scores:**
            
            - **Lower body fat** generally improves:
              - 2.4km run time (less weight to carry)
              - Pull-ups (better strength-to-weight ratio)
              - Shuttle run speed
            
            - **Higher lean mass** generally improves:
              - Standing broad jump (more power)
              - Pull-ups (more muscle)
              - Sit-ups (stronger core)
            
            - **Balanced composition** is key:
              - Too low body fat can reduce energy/performance
              - Optimal is athletic/fitness range for your gender
            """)
            
            # Save to history
            if 'body_comp_history' not in user_data:
                user_data['body_comp_history'] = []
            
            user_data['body_comp_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'body_fat_pct': round(body_fat_pct, 1),
                'fat_mass': round(fat_mass, 1),
                'lean_mass': round(lean_mass, 1),
                'weight': weight,
                'neck': neck,
                'waist': waist,
                'hip': hip if gender == 'f' else None
            })
            update_user_data(user_data)
            
            st.success("✅ Body composition data saved to your history!")
        
        # Show history if available
        if user_data.get('body_comp_history') and len(user_data['body_comp_history']) > 1:
            st.write("")
            st.write("### 📈 Progress Tracking")
            
            df_comp = pd.DataFrame(user_data['body_comp_history'])
            df_comp['date'] = pd.to_datetime(df_comp['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Body Fat % Trend**")
                st.line_chart(df_comp.set_index('date')['body_fat_pct'])
            
            with col2:
                st.write("**Lean Mass Trend**")
                st.line_chart(df_comp.set_index('date')['lean_mass'])
        
        # Method explanation
        st.write("")
        with st.expander("ℹ️ About the Navy Method"):
            st.write("""
            **The U.S. Navy Body Composition Method:**
            
            This is a validated method used by the U.S. military that estimates body fat percentage 
            using circumference measurements. It's considered one of the most accurate non-clinical methods.
            
            **Advantages:**
            - No special equipment needed (just a measuring tape)
            - Good accuracy (within 3-4% of DEXA scans)
            - Easy to do at home
            - Tracks changes over time
            
            **Tips for Accurate Measurements:**
            1. Measure in the morning before eating
            2. Stand relaxed, don't suck in or flex
            3. Keep tape horizontal and snug (not tight)
            4. Take 2-3 measurements and use the average
            5. Same person should measure each time if possible
            
            **Note:** This is an estimate. For most accurate results, consider professional body composition 
            testing (DEXA scan, hydrostatic weighing, or BodPod) if available.
            """)

# API Integrations
def api_integrations():
    st.header("🌐 API Integrations")
    st.write("Connect with external services for enhanced features")
    
    user_data = get_user_data()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "🌤️ Weather API",
        "🍔 Nutrition API",
        "🎥 YouTube API"
    ])
    
    with tab1:
        st.subheader("🌤️ Weather-Based Workout Recommendations")
        st.write("Get outdoor workout suggestions based on current weather")
        
        # Show API status
        if OPENWEATHER_API_KEY:
            st.success("✅ Real Weather API Active")
        else:
            st.info("📝 Using simulated weather data. Add API key to enable real-time weather.")
        
        location = st.text_input("Your Location", value="Singapore", placeholder="Enter city name")
        
        if st.button("Get Weather & Recommendations", type="primary"):
            
            if OPENWEATHER_API_KEY and API_MODE == 'real':
                # REAL API CALL
                try:
                    import requests
                    
                    # OpenWeatherMap API endpoint
                    url = f"http://api.openweathermap.org/data/2.5/weather"
                    params = {
                        'q': location,
                        'appid': OPENWEATHER_API_KEY,
                        'units': 'metric'  # Get temperature in Celsius
                    }
                    
                    response = requests.get(url, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Extract weather data
                        temp = round(data['main']['temp'])
                        humidity = data['main']['humidity']
                        conditions = data['weather'][0]['main']
                        description = data['weather'][0]['description']
                        
                        st.success(f"✅ Real-time weather data from OpenWeatherMap")
                    else:
                        st.error(f"Error fetching weather: {response.status_code}")
                        # Fallback to mock data
                        temp, humidity, conditions = 30, 75, "Clear"
                
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
                    st.info("Falling back to simulated data")
                    # Fallback to mock data
                    import random
                    temp = random.randint(25, 35)
                    humidity = random.randint(60, 90)
                    conditions = random.choice(["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Rainy"])
            
            else:
                # MOCK DATA (when no API key)
                import random
                temp = random.randint(25, 35)
                humidity = random.randint(60, 90)
                conditions = random.choice(["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Rainy"])
                
                if not OPENWEATHER_API_KEY:
                    st.warning("⚠️ Simulated weather data (no API key configured)")
            
            # Display weather (same for both real and mock)
            st.write("### Current Weather")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌡️ Temperature", f"{temp}°C")
            with col2:
                st.metric("💧 Humidity", f"{humidity}%")
            with col3:
                st.metric("☁️ Conditions", conditions)
            
            # Generate recommendations (same logic for both)
            st.write("")
            st.write("### 🏃 Workout Recommendations")
            
            if temp < 28 and "Rain" not in conditions:
                recommendation = "✅ Perfect for outdoor running!"
                workout = "2.4km NAPFA practice run"
                color = "#4caf50"
            elif temp < 32 and "Rain" not in conditions:
                recommendation = "⚠️ Good for outdoor, stay hydrated"
                workout = "Morning or evening run (avoid midday)"
                color = "#ff9800"
            elif "Rain" in conditions:
                recommendation = "🏠 Indoor workout recommended"
                workout = "Indoor circuit: push-ups, sit-ups, burpees"
                color = "#2196f3"
            else:
                recommendation = "🌡️ Too hot! Indoor training"
                workout = "Air-con gym or home workout"
                color = "#f44336"
            
            st.markdown(f"""
            <div class="stat-card" style="background: {color}; color: white;">
                <h3>{recommendation}</h3>
                <h4>Suggested: {workout}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Hydration advice
            hydration_need = "High" if temp > 30 or humidity > 80 else "Moderate"
            st.info(f"💧 **Hydration Need:** {hydration_need} - Drink {500 if hydration_need == 'High' else 300}ml before workout")
        
        # Setup instructions
        if not OPENWEATHER_API_KEY:
            st.write("")
            st.write("---")
            st.write("### 🔗 Enable Real-Time Weather")
            
            with st.expander("📝 Setup Instructions", expanded=False):
                st.markdown("""
                **Step 1: Get Free API Key**
                1. Go to: https://openweathermap.org/api
                2. Click "Sign Up" (it's FREE!)
                3. Verify your email
                4. Go to "API Keys" tab
                5. Copy your API key
                
                **Step 2: Add to Streamlit Cloud**
                1. Deploy your app to Streamlit Cloud
                2. Go to your app settings (⚙️)
                3. Click "Secrets"
                4. Add this:
                ```
                OPENWEATHER_API_KEY = "your_api_key_here"
                ```
                5. Save and restart app
                
                **Step 3: Run Locally (Optional)**
                Create a file called `.streamlit/secrets.toml`:
                ```
                OPENWEATHER_API_KEY = "your_api_key_here"
                ```
                
                **That's it!** The app will automatically use real weather data.
                
                **Free Tier Limits:**
                - 1,000 API calls per day
                - 60 calls per minute
                - More than enough for personal use!
                """)

    
    with tab2:
        st.subheader("🍔 Food & Nutrition Database")
        st.write("Search nutritional information for any food")
        
        # Show API status
        if USDA_API_KEY:
            st.success("✅ Real USDA Food Database Active (350,000+ foods)")
        else:
            st.info("📝 Using sample food database. Add USDA API key for 350,000+ foods.")
        
        # Food search
        food_query = st.text_input("Search for a food", placeholder="e.g., chicken rice, banana, salmon")
        
        # Advanced search options
        with st.expander("🔍 Advanced Search Options"):
            col1, col2 = st.columns(2)
            with col1:
                food_category = st.selectbox(
                    "Food Category (optional)",
                    ["All Categories", "Dairy", "Fruits", "Vegetables", "Proteins", 
                     "Grains", "Snacks", "Beverages", "Fast Foods"]
                )
            with col2:
                sort_by = st.selectbox(
                    "Sort by",
                    ["Relevance", "Protein (High to Low)", "Calories (Low to High)", "Calories (High to Low)"]
                )
        
        if st.button("Search Nutrition", type="primary"):
            
            if USDA_API_KEY and API_MODE == 'real':
                # REAL USDA API CALL
                try:
                    import requests
                    
                    # FoodData Central API endpoint
                    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
                    
                    params = {
                        'api_key': USDA_API_KEY,
                        'query': food_query,
                        'pageSize': 10,  # Get top 10 results
                    }
                    
                    # Note: Removed dataType filter as it can cause 400 errors
                    # The API will return the best matches automatically
                    
                    response = requests.get(url, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        foods = data.get('foods', [])
                        
                        if foods:
                            st.success(f"✅ Found {len(foods)} results from USDA database")
                            
                            # Sort results if needed
                            if sort_by == "Protein (High to Low)":
                                foods = sorted(foods, key=lambda x: get_nutrient_from_food(x, 'Protein'), reverse=True)
                            elif sort_by == "Calories (Low to High)":
                                foods = sorted(foods, key=lambda x: get_nutrient_from_food(x, 'Energy'))
                            elif sort_by == "Calories (High to Low)":
                                foods = sorted(foods, key=lambda x: get_nutrient_from_food(x, 'Energy'), reverse=True)
                            
                            # Display results
                            for food in foods[:5]:  # Show top 5
                                food_name = food.get('description', 'Unknown Food')
                                brand = food.get('brandOwner', '')
                                
                                # Extract nutrients
                                nutrients = food.get('foodNutrients', [])
                                
                                calories = get_nutrient_value(nutrients, 'Energy')
                                protein = get_nutrient_value(nutrients, 'Protein')
                                carbs = get_nutrient_value(nutrients, 'Carbohydrate, by difference')
                                fat = get_nutrient_value(nutrients, 'Total lipid (fat)')
                                fiber = get_nutrient_value(nutrients, 'Fiber, total dietary')
                                sugar = get_nutrient_value(nutrients, 'Sugars, total including NLEA')
                                
                                # Handle alternative nutrient names
                                if calories is None:
                                    calories = get_nutrient_value(nutrients, 'Energy (Atwater General Factors)')
                                if carbs is None:
                                    carbs = get_nutrient_value(nutrients, 'Carbohydrate')
                                if fat is None:
                                    fat = get_nutrient_value(nutrients, 'Fat')
                                
                                # Serving size
                                serving = food.get('servingSize', 100)
                                serving_unit = food.get('servingUnit', 'g')
                                
                                with st.expander(f"🍽️ {food_name}" + (f" ({brand})" if brand else ""), expanded=True):
                                    col1, col2 = st.columns([2, 1])
                                    
                                    with col1:
                                        st.write(f"**Serving Size:** {serving} {serving_unit}")
                                        
                                        col_a, col_b, col_c, col_d = st.columns(4)
                                        col_a.metric("Calories", f"{calories:.0f}" if calories else "N/A")
                                        col_b.metric("Protein", f"{protein:.1f}g" if protein else "N/A")
                                        col_c.metric("Carbs", f"{carbs:.1f}g" if carbs else "N/A")
                                        col_d.metric("Fat", f"{fat:.1f}g" if fat else "N/A")
                                        
                                        if fiber or sugar:
                                            st.write("")
                                            col_e, col_f = st.columns(2)
                                            if fiber:
                                                col_e.write(f"**Fiber:** {fiber:.1f}g")
                                            if sugar:
                                                col_f.write(f"**Sugars:** {sugar:.1f}g")
                                    
                                    with col2:
                                        # Macro ratio
                                        if calories and calories > 0:
                                            st.write("**Macro Ratio:**")
                                            p_cals = (protein or 0) * 4
                                            c_cals = (carbs or 0) * 4
                                            f_cals = (fat or 0) * 9
                                            total = p_cals + c_cals + f_cals
                                            
                                            if total > 0:
                                                st.write(f"Protein: {(p_cals/total*100):.0f}%")
                                                st.write(f"Carbs: {(c_cals/total*100):.0f}%")
                                                st.write(f"Fat: {(f_cals/total*100):.0f}%")
                                        
                                        # Health score (simple)
                                        health_score = calculate_health_score(protein, carbs, fat, fiber, sugar)
                                        if health_score:
                                            st.write("")
                                            st.metric("Health Score", f"{health_score}/10")
                        else:
                            st.warning(f"No results found for '{food_query}'. Try a different search term.")
                    
                    elif response.status_code == 400:
                        st.error("API Error 400: Invalid request format")
                        st.write("**Debug Info:**")
                        st.write(f"Query: {food_query}")
                        try:
                            error_detail = response.json()
                            st.write(f"Error details: {error_detail}")
                        except:
                            st.write(f"Response: {response.text}")
                        st.info("Falling back to sample database")
                        show_mock_nutrition_data(food_query)
                    
                    elif response.status_code == 403:
                        st.error("API Error 403: Invalid API key")
                        st.write("Please check your USDA_API_KEY in Streamlit Secrets")
                        st.info("Falling back to sample database")
                        show_mock_nutrition_data(food_query)
                    
                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.info("Falling back to sample database")
                        show_mock_nutrition_data(food_query)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Falling back to sample database")
                    show_mock_nutrition_data(food_query)
            
            else:
                # MOCK DATA (when no API key)
                show_mock_nutrition_data(food_query)
        
        # Setup instructions
        if not USDA_API_KEY:
            st.write("")
            st.write("---")
            st.write("### 🔗 Enable Full Food Database")
            
            with st.expander("📝 Setup Instructions (2 minutes)", expanded=False):
                st.markdown("""
                **Step 1: Get FREE API Key**
                1. Go to: https://fdc.nal.usda.gov/api-key-signup.html
                2. Fill in:
                   - First Name
                   - Last Name
                   - Email Address
                   - Organization: "School of Science and Technology" (or "Personal")
                3. Click "Sign Up"
                4. Check your email for API key
                5. Copy the key (long string of letters/numbers)
                
                **Step 2: Add to Streamlit Cloud**
                1. Go to your deployed app
                2. Click ⚙️ Settings → Secrets
                3. Add this line:
                ```
                USDA_API_KEY = "your_api_key_here"
                ```
                4. Save and restart
                
                **Step 3: Test**
                1. Come back to this page
                2. Should see "✅ Real USDA Food Database Active"
                3. Search any food - get instant results!
                
                **What You Get:**
                - ✅ 350,000+ foods (vs. 5 sample foods)
                - ✅ Brand name foods
                - ✅ Restaurant foods
                - ✅ Complete nutrient data (vitamins, minerals, etc.)
                - ✅ Serving size info
                - ✅ Unlimited searches (FREE forever!)
                
                **Free Tier:**
                - 1,000 requests per hour
                - No daily limit
                - No credit card needed
                - FREE forever!
                """)
    
    with tab3:
        st.subheader("🎥 Exercise Tutorial Videos")
        st.write("Curated YouTube videos for NAPFA components and exercises")
        
        st.info("💡 We use curated video links for best quality tutorials!")
        
        # NAPFA Component Videos
        st.write("### NAPFA Component Tutorials")
        
        napfa_videos = {
            "Sit-Ups": "https://www.youtube.com/results?search_query=proper+sit+ups+form",
            "Standing Broad Jump": "https://www.youtube.com/results?search_query=standing+broad+jump+technique",
            "Sit and Reach": "https://www.youtube.com/results?search_query=sit+and+reach+flexibility",
            "Pull-Ups": "https://www.youtube.com/results?search_query=pull+ups+tutorial",
            "Shuttle Run": "https://www.youtube.com/results?search_query=shuttle+run+technique",
            "2.4km Run": "https://www.youtube.com/results?search_query=running+form+tips"
        }
        
        for component, url in napfa_videos.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{component}**")
            with col2:
                st.link_button("Watch Videos", url, type="secondary")
        
        st.write("")
        st.write("### General Workout Videos")
        
        workout_videos = {
            "Strength Training": "https://www.youtube.com/results?search_query=strength+training+beginners",
            "Cardio Workouts": "https://www.youtube.com/results?search_query=cardio+workout+home",
            "Flexibility & Stretching": "https://www.youtube.com/results?search_query=flexibility+stretching+routine",
            "HIIT Training": "https://www.youtube.com/results?search_query=HIIT+workout",
            "Warm Up Exercises": "https://www.youtube.com/results?search_query=dynamic+warm+up",
            "Cool Down Stretches": "https://www.youtube.com/results?search_query=cool+down+stretches"
        }
        
        for workout, url in workout_videos.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{workout}**")
            with col2:
                st.link_button("Watch Videos", url, type="secondary")
        
        st.write("")
        st.success("✅ All video links lead to curated YouTube search results for best tutorials!")

# Helper functions for USDA API
def get_nutrient_from_food(food, nutrient_name):
    """Extract nutrient value from food object for sorting"""
    nutrients = food.get('foodNutrients', [])
    value = get_nutrient_value(nutrients, nutrient_name)
    return value if value is not None else 0

def get_nutrient_value(nutrients, nutrient_name):
    """Extract nutrient value from USDA food data"""
    for nutrient in nutrients:
        # Check nutrient name
        name = nutrient.get('nutrientName', '')
        if nutrient_name.lower() in name.lower():
            return nutrient.get('value', 0)
    return None

def calculate_health_score(protein, carbs, fat, fiber, sugar):
    """Simple health score calculation (1-10)"""
    if not all([protein is not None, carbs is not None, fat is not None]):
        return None
    
    score = 5.0  # Start at neutral
    
    # High protein is good
    if protein and protein > 10:
        score += 1.5
    elif protein and protein > 5:
        score += 0.5
    
    # High fiber is good
    if fiber and fiber > 5:
        score += 1.5
    elif fiber and fiber > 2:
        score += 0.5
    
    # High sugar is bad
    if sugar and sugar > 20:
        score -= 2.0
    elif sugar and sugar > 10:
        score -= 1.0
    
    # Balance of macros
    total = protein + carbs + fat
    if total > 0:
        protein_ratio = protein / total
        if 0.2 <= protein_ratio <= 0.4:  # Good protein ratio
            score += 1.0
    
    return max(1, min(10, round(score, 1)))

def show_mock_nutrition_data(food_query):
    """Display mock nutrition data when API not available"""
    # Simulated nutrition database
    nutrition_db = {
        "chicken rice": {
            "calories": 607,
            "protein": 25,
            "carbs": 86,
            "fat": 15,
            "fiber": 2,
            "sugar": 3,
            "serving": "1 plate (350g)"
        },
        "banana": {
            "calories": 105,
            "protein": 1.3,
            "carbs": 27,
            "fat": 0.4,
            "fiber": 3.1,
            "sugar": 14,
            "serving": "1 medium (118g)"
        },
        "apple": {
            "calories": 95,
            "protein": 0.5,
            "carbs": 25,
            "fat": 0.3,
            "fiber": 4.4,
            "sugar": 19,
            "serving": "1 medium (182g)"
        },
        "white rice": {
            "calories": 204,
            "protein": 4.2,
            "carbs": 45,
            "fat": 0.4,
            "fiber": 0.6,
            "sugar": 0.1,
            "serving": "1 cup cooked (158g)"
        },
        "grilled chicken breast": {
            "calories": 165,
            "protein": 31,
            "carbs": 0,
            "fat": 3.6,
            "fiber": 0,
            "sugar": 0,
            "serving": "100g"
        },
        "salmon": {
            "calories": 206,
            "protein": 22,
            "carbs": 0,
            "fat": 13,
            "fiber": 0,
            "sugar": 0,
            "serving": "100g"
        },
        "broccoli": {
            "calories": 55,
            "protein": 3.7,
            "carbs": 11,
            "fat": 0.6,
            "fiber": 5.1,
            "sugar": 2.2,
            "serving": "1 cup chopped (156g)"
        },
        "egg": {
            "calories": 72,
            "protein": 6,
            "carbs": 0.4,
            "fat": 5,
            "fiber": 0,
            "sugar": 0.2,
            "serving": "1 large (50g)"
        }
    }
    
    # Search (case-insensitive, partial match)
    results = {k: v for k, v in nutrition_db.items() if food_query.lower() in k.lower()}
    
    if results:
        st.success(f"Found {len(results)} result(s) in sample database")
        
        for food_name, nutrition in results.items():
            with st.expander(f"🍽️ {food_name.title()}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Serving Size:** {nutrition['serving']}")
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("Calories", f"{nutrition['calories']} kcal")
                    col_b.metric("Protein", f"{nutrition['protein']}g")
                    col_c.metric("Carbs", f"{nutrition['carbs']}g")
                    col_d.metric("Fat", f"{nutrition['fat']}g")
                    
                    st.write("")
                    col_e, col_f = st.columns(2)
                    col_e.write(f"**Fiber:** {nutrition['fiber']}g")
                    col_f.write(f"**Sugars:** {nutrition['sugar']}g")
                
                with col2:
                    # Macro ratio
                    total_cals = (nutrition['protein'] * 4 + nutrition['carbs'] * 4 + nutrition['fat'] * 9)
                    if total_cals > 0:
                        st.write("**Macro Ratio:**")
                        st.write(f"Protein: {(nutrition['protein']*4/total_cals*100):.0f}%")
                        st.write(f"Carbs: {(nutrition['carbs']*4/total_cals*100):.0f}%")
                        st.write(f"Fat: {(nutrition['fat']*9/total_cals*100):.0f}%")
                    
                    # Health score
                    health_score = calculate_health_score(
                        nutrition['protein'], 
                        nutrition['carbs'], 
                        nutrition['fat'],
                        nutrition['fiber'],
                        nutrition['sugar']
                    )
                    if health_score:
                        st.write("")
                        st.metric("Health Score", f"{health_score}/10")
        
        st.info("💡 **Limited to 8 sample foods.** Add USDA API key for 350,000+ foods!")
    else:
        st.warning(f"No results for '{food_query}' in sample database.")
        st.write("**Try searching:** chicken rice, banana, apple, white rice, grilled chicken breast, salmon, broccoli, egg")
        st.info("💡 Add USDA API key to search any food!")

# Workout Timer with Audio
        st.subheader("🎥 Exercise Tutorial Videos")
        st.write("Get exercise demonstrations from YouTube")
        
        # NAPFA component selector
        exercise = st.selectbox(
            "Select Exercise",
            ["Sit-Ups", "Standing Broad Jump", "Sit and Reach", 
             "Pull-Ups", "Shuttle Run", "2.4km Running Tips"]
        )
        
        if st.button("Find Tutorials", type="primary"):
            # Simulated YouTube recommendations (in production, use YouTube Data API)
            videos = {
                "Sit-Ups": [
                    {"title": "Perfect Sit-Up Form for NAPFA", "channel": "FitnessBlender", "duration": "5:23"},
                    {"title": "How to Do More Sit-Ups", "channel": "PE Coach", "duration": "8:15"},
                    {"title": "NAPFA Sit-Up Training", "channel": "SG Fitness", "duration": "6:40"}
                ],
                "Pull-Ups": [
                    {"title": "Pull-Up Progression Guide", "channel": "Calisthenicmovement", "duration": "12:30"},
                    {"title": "Get Your First Pull-Up", "channel": "Athlean-X", "duration": "10:15"},
                    {"title": "NAPFA Pull-Up Technique", "channel": "PE Singapore", "duration": "7:20"}
                ],
                "Standing Broad Jump": [
                    {"title": "Standing Broad Jump Technique", "channel": "Track Coach", "duration": "6:45"},
                    {"title": "How to Jump Further", "channel": "Sprint Master", "duration": "9:10"}
                ],
                "2.4km Running Tips": [
                    {"title": "2.4km NAPFA Strategy", "channel": "Running Coach SG", "duration": "11:20"},
                    {"title": "How to Run Faster 2.4km", "channel": "TrackStar", "duration": "8:50"}
                ]
            }
            
            if exercise in videos:
                st.write(f"### 📹 Top Tutorials for {exercise}")
                
                for video in videos[exercise]:
                    with st.expander(f"▶️ {video['title']} - {video['duration']}", expanded=True):
                        st.write(f"**Channel:** {video['channel']}")
                        st.write(f"**Duration:** {video['duration']}")
                        
                        # In production, embed actual video
                        st.info("🎥 Video would be embedded here with real YouTube API")
                        
                        st.write("**🔗 Search on YouTube:** ")
                        search_url = f"https://www.youtube.com/results?search_query={exercise.replace(' ', '+')}+NAPFA+tutorial"
                        st.markdown(f"[Open YouTube Search]({search_url})")
            
            st.write("")
            st.info("""
            **🔗 To enable video embedding:**
            
            Use YouTube Data API v3 (free quota):
            1. Get API key: https://console.cloud.google.com/
            2. Enable YouTube Data API
            3. Embed videos directly in app
            """)

# Workout Timer with Audio
def workout_timer():
    st.header("⏱️ Workout Timer & Logger")
    st.write("Time your workout in real-time and automatically log it")
    
    user_data = get_user_data()
    
    # Initialize session state for timer
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_seconds' not in st.session_state:
        st.session_state.timer_seconds = 0
    if 'timer_start_time' not in st.session_state:
        st.session_state.timer_start_time = None
    if 'workout_name' not in st.session_state:
        st.session_state.workout_name = ""
    if 'workout_intensity' not in st.session_state:
        st.session_state.workout_intensity = "Medium"
    if 'workout_notes' not in st.session_state:
        st.session_state.workout_notes = ""
    
    # Workout details (enter before starting timer)
    if not st.session_state.timer_running:
        st.write("### 📝 Workout Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            workout_name = st.text_input(
                "Exercise Name", 
                value=st.session_state.workout_name,
                placeholder="e.g., Running, Swimming, Gym"
            )
            st.session_state.workout_name = workout_name
        
        with col2:
            intensity = st.selectbox(
                "Intensity", 
                ["Low", "Medium", "High"],
                index=["Low", "Medium", "High"].index(st.session_state.workout_intensity)
            )
            st.session_state.workout_intensity = intensity
        
        notes = st.text_area(
            "Notes (optional)", 
            value=st.session_state.workout_notes,
            placeholder="Any additional notes about your workout..."
        )
        st.session_state.workout_notes = notes
        
        st.write("")
    
    # Timer display
    if st.session_state.timer_running:
        elapsed = st.session_state.timer_seconds
        
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        
        # Large timer display
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, {SST_COLORS['red']} 0%, #b71c1c 100%); color: white; text-align: center;">
            <h2 style="color: white; margin-bottom: 10px;">🏃 Workout in Progress</h2>
            <h3 style="color: white; margin-bottom: 5px;">{st.session_state.workout_name or 'Workout'}</h3>
            <h1 style="font-size: 96px; margin: 30px 0; font-family: monospace; color: white; font-weight: bold;">
                {hours:02d}:{minutes:02d}:{seconds:02d}
            </h1>
            <p style="color: white; font-size: 18px;">Intensity: {st.session_state.workout_intensity}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Stop button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("⏹️ Stop & Log Workout", type="primary", use_container_width=True):
                # Calculate duration in minutes
                duration_mins = st.session_state.timer_seconds // 60
                
                if duration_mins > 0:
                    # Log the workout
                    user_data['exercises'].insert(0, {
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'name': st.session_state.workout_name or 'Timed Workout',
                        'duration': duration_mins,
                        'intensity': st.session_state.workout_intensity,
                        'notes': st.session_state.workout_notes
                    })
                    
                    # Calculate house points (1 hour = 1 point)
                    house_points_msg = ""
                    if user_data.get('role') == 'student' and user_data.get('house'):
                        hours_earned = duration_mins / 60.0
                        user_data['total_workout_hours'] = user_data.get('total_workout_hours', 0) + hours_earned
                        user_data['house_points_contributed'] = user_data.get('house_points_contributed', 0) + hours_earned
                        house_points_msg = f"🏠 +{hours_earned:.1f} points for {user_data['house'].title()} House!"
                    
                    update_user_data(user_data)
                    
                    # Reset timer
                    st.session_state.timer_running = False
                    st.session_state.timer_seconds = 0
                    st.session_state.workout_name = ""
                    st.session_state.workout_notes = ""
                    
                    st.success(f"✅ Workout logged! Duration: {duration_mins} minutes")
                    if house_points_msg:
                        st.info(house_points_msg)
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Workout must be at least 1 minute to log")
        
        # Auto-increment timer
        st.session_state.timer_seconds += 1
        time.sleep(1)
        st.rerun()
    
    else:
        # Show ready state
        st.markdown(f"""
        <div class="stat-card" style="text-align: center;">
            <h1 style="font-size: 72px; margin: 20px 0;">⏱️</h1>
            <h2>Ready to start your workout</h2>
            <p>Fill in the details above and click Start</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Start button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("▶️ Start Timer", type="primary", use_container_width=True, disabled=not st.session_state.workout_name):
                st.session_state.timer_running = True
                st.session_state.timer_seconds = 0
                st.session_state.timer_start_time = datetime.now()
                st.rerun()
        
        if not st.session_state.workout_name:
            st.warning("⚠️ Please enter an exercise name to start the timer")
    
    # Display recent exercises below
    st.write("")
    st.write("---")
    
    if user_data['exercises']:
        st.subheader("📋 Recent Workouts")
        
        # Show last 5 exercises
        recent = user_data['exercises'][:5]
        for ex in recent:
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            with col1:
                st.write(f"**{ex['name']}**")
            with col2:
                st.write(f"📅 {ex['date']}")
            with col3:
                st.write(f"⏱️ {ex['duration']} min")
            with col4:
                intensity_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                st.write(f"{intensity_emoji.get(ex['intensity'], '⚪')} {ex['intensity']}")
        
        # Link to full exercise log
        st.write("")
        st.info("💡 View all workouts in the Exercise Log page")
    else:
        st.info("No workouts logged yet. Start your first workout above!")

# Teacher Dashboard
# Teacher Dashboard
def teacher_dashboard():
    st.header("👨‍🏫 Teacher Dashboard")
    
    user_data = get_user_data()
    all_users = st.session_state.users_data
    
    # Display class code
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, {SST_COLORS['blue']} 0%, #1565c0 100%); color: white;">
        <h2>📝 Your Class Code: {user_data['class_code']}</h2>
        <p>Share this code with your students to join your class</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Get student list
    student_usernames = user_data.get('students', [])
    students_data = {username: all_users[username] for username in student_usernames if username in all_users}
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💪 My Fitness",
        "🏠 Houses",
        "📊 Class Overview",
        "👥 Student List", 
        "📈 Performance Analysis",
        "📄 Export Reports"
    ])
    
    with tab1:
        st.subheader("💪 My Personal Fitness")
        st.write("Track your own fitness alongside your students!")
        
        # Allow teachers to access all student features
        teacher_feature = st.selectbox(
            "Select Feature",
            ["Dashboard", "BMI Calculator", "NAPFA Test", "Sleep Tracker", 
             "Exercise Log", "Training Schedule", "AI Insights", "Community"]
        )
        
        if teacher_feature == "Dashboard":
            st.write("### 📊 Your Fitness Overview")
            
            # Teacher's personal stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if user_data.get('bmi_history'):
                    latest_bmi = user_data['bmi_history'][-1]['bmi']
                    st.metric("Latest BMI", f"{latest_bmi:.1f}")
                else:
                    st.metric("Latest BMI", "No data")
            
            with col2:
                if user_data.get('napfa_history'):
                    latest_napfa = user_data['napfa_history'][-1]['total']
                    st.metric("NAPFA Score", f"{latest_napfa}/30")
                else:
                    st.metric("NAPFA Score", "No data")
            
            with col3:
                total_workouts = len(user_data.get('exercises', []))
                st.metric("Total Workouts", total_workouts)
            
            with col4:
                if user_data.get('house'):
                    house_display = {'yellow': '🟡 Yellow', 'red': '🔴 Red', 'blue': '🔵 Blue', 
                                   'green': '🟢 Green', 'black': '⚫ Black'}.get(user_data['house'], 'None')
                    st.metric("Your House", house_display)
                else:
                    st.metric("Your House", "Not assigned")
            
            # Quick actions
            st.write("")
            st.write("### 🚀 Quick Actions")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 Log Workout", key="teacher_log"):
                    st.session_state.teacher_feature_nav = "Exercise Log"
                    st.rerun()
            with col2:
                if st.button("🏃 Take NAPFA", key="teacher_napfa"):
                    st.session_state.teacher_feature_nav = "NAPFA Test"
                    st.rerun()
            with col3:
                if st.button("🤖 AI Insights", key="teacher_ai"):
                    st.session_state.teacher_feature_nav = "AI Insights"
                    st.rerun()
            
            # Recent activity
            if user_data.get('exercises'):
                st.write("")
                st.write("### 📋 Recent Workouts")
                recent = user_data['exercises'][:5]
                for ex in recent:
                    st.write(f"• **{ex['name']}** - {ex['duration']} min ({ex['date']})")
        
        elif teacher_feature == "BMI Calculator":
            bmi_calculator()
        
        elif teacher_feature == "NAPFA Test":
            napfa_calculator()
        
        elif teacher_feature == "Sleep Tracker":
            sleep_tracker()
        
        elif teacher_feature == "Exercise Log":
            exercise_logger()
        
        elif teacher_feature == "Training Schedule":
            schedule_manager()
        
        elif teacher_feature == "AI Insights":
            ai_insights()
        
        elif teacher_feature == "Community":
            st.write("### 🏆 Community Features")
            st.info("💡 As a teacher, you can join houses, compete on leaderboards, and connect with colleagues!")
            
            community_sub = st.selectbox("Select", ["Leaderboards", "My Achievements", "Friends"])
            
            if community_sub == "Leaderboards":
                st.write("Access leaderboards from the main Community section")
                st.write("You can compete with students and other teachers!")
            
            elif community_sub == "My Achievements":
                st.write("### 🎖️ Your Badges & Achievements")
                badges = user_data.get('badges', [])
                if badges:
                    for badge in badges:
                        st.success(f"{badge['name']} - {badge['description']} (+{badge['points']} pts)")
                else:
                    st.info("Complete workouts and NAPFA tests to earn badges!")
            
            elif community_sub == "Friends":
                st.write("### 👥 Connect with Colleagues")
                st.write("Add other teachers as friends to compare fitness progress!")
    
    with tab2:
        st.subheader("🏠 House System - Your Class")
        
        # Calculate house stats for THIS teacher's students only
        house_stats = {
            'yellow': {'points': 0, 'members': [], 'workouts': 0, 'display': '🟡 Yellow House', 'color': '#FFD700'},
            'red': {'points': 0, 'members': [], 'workouts': 0, 'display': '🔴 Red House', 'color': '#DC143C'},
            'blue': {'points': 0, 'members': [], 'workouts': 0, 'display': '🔵 Blue House', 'color': '#1E90FF'},
            'green': {'points': 0, 'members': [], 'workouts': 0, 'display': '🟢 Green House', 'color': '#32CD32'},
            'black': {'points': 0, 'members': [], 'workouts': 0, 'display': '⚫ Black House', 'color': '#2F4F4F'}
        }
        
        # Calculate points for teacher's students only
        for username, student in students_data.items():
            if student.get('house'):
                house = student['house']
                if house in house_stats:
                    house_stats[house]['points'] += student.get('house_points_contributed', 0)
                    house_stats[house]['members'].append(username)
                    house_stats[house]['workouts'] += len(student.get('exercises', []))
        
        # Sort houses
        sorted_houses = sorted(house_stats.items(), key=lambda x: x[1]['points'], reverse=True)
        
        # Display house standings
        st.write("### 🏆 House Standings (Your Class)")
        
        for rank, (house_name, stats) in enumerate(sorted_houses, 1):
            if stats['members']:  # Only show houses with members
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
                
                st.markdown(f"""
                <div class="stat-card" style="background: linear-gradient(135deg, {stats['color']} 0%, {stats['color']}dd 100%); color: white;">
                    <h3>{medal} {stats['display']}</h3>
                    <h2>{stats['points']:.1f} Points</h2>
                    <p>👥 {len(stats['members'])} members | 💪 {stats['workouts']} workouts</p>
                </div>
                """, unsafe_allow_html=True)
        
        # House distribution
        st.write("")
        st.write("### 📊 House Distribution")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        
        for idx, (house_name, stats) in enumerate(sorted_houses):
            with cols[idx]:
                st.metric(stats['display'], len(stats['members']))
        
        # Students not assigned to house
        unassigned = [username for username, student in students_data.items() if not student.get('house')]
        if unassigned:
            st.write("")
            st.warning(f"⚠️ {len(unassigned)} student(s) not assigned to a house")
            st.write("Go to 'Student List' tab to assign houses.")
    
    with tab3:
        st.subheader("Class Overview")
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", f"{len(students_data)}/30")
        
        with col2:
            # Calculate average NAPFA
            napfa_scores = []
            for student in students_data.values():
                if student.get('napfa_history'):
                    napfa_scores.append(student['napfa_history'][-1]['total'])
            
            if napfa_scores:
                avg_napfa = sum(napfa_scores) / len(napfa_scores)
                st.metric("Avg NAPFA Score", f"{avg_napfa:.1f}/30")
            else:
                st.metric("Avg NAPFA Score", "No data")
        
        with col3:
            # Active this week
            week_ago = datetime.now() - timedelta(days=7)
            active_count = 0
            for student in students_data.values():
                if student.get('exercises'):
                    for exercise in student['exercises']:
                        if datetime.strptime(exercise['date'], '%Y-%m-%d') >= week_ago:
                            active_count += 1
                            break
            
            st.metric("Active This Week", f"{active_count}/{len(students_data)}")
        
        with col4:
            # Total workouts this week
            total_workouts = 0
            for student in students_data.values():
                if student.get('exercises'):
                    weekly = [e for e in student['exercises'] 
                            if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                    total_workouts += len(weekly)
            
            st.metric("Class Workouts", total_workouts)
        
        # Performance distribution
        if napfa_scores:
            st.write("")
            st.write("### 📊 NAPFA Score Distribution")
            
            # Create distribution chart
            df = pd.DataFrame({'Score': napfa_scores})
            st.bar_chart(df['Score'].value_counts().sort_index())
            
            # Medal counts
            st.write("")
            st.write("### 🏅 Medal Distribution")
            
            medal_counts = {'🥇 Gold': 0, '🥈 Silver': 0, '🥉 Bronze': 0, 'No Medal': 0}
            for student in students_data.values():
                if student.get('napfa_history'):
                    medal = student['napfa_history'][-1]['medal']
                    if '🥇' in medal:
                        medal_counts['🥇 Gold'] += 1
                    elif '🥈' in medal:
                        medal_counts['🥈 Silver'] += 1
                    elif '🥉' in medal:
                        medal_counts['🥉 Bronze'] += 1
                    else:
                        medal_counts['No Medal'] += 1
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🥇 Gold", medal_counts['🥇 Gold'])
            col2.metric("🥈 Silver", medal_counts['🥈 Silver'])
            col3.metric("🥉 Bronze", medal_counts['🥉 Bronze'])
            col4.metric("No Medal", medal_counts['No Medal'])
        
        # Top performers
        if napfa_scores:
            st.write("")
            st.write("### ⭐ Top Performers")
            
            student_scores = []
            for username, student in students_data.items():
                if student.get('napfa_history'):
                    student_scores.append({
                        'name': student['name'],
                        'username': username,
                        'score': student['napfa_history'][-1]['total'],
                        'medal': student['napfa_history'][-1]['medal']
                    })
            
            student_scores.sort(key=lambda x: x['score'], reverse=True)
            
            for idx, student in enumerate(student_scores[:5], 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
                st.write(f"{medal} **{student['name']}** - {student['score']}/30 ({student['medal']})")
        
        # Students needing attention
        st.write("")
        st.write("### ⚠️ Students Needing Attention")
        
        needs_attention = []
        for username, student in students_data.items():
            # Check if inactive
            if not student.get('exercises') or len(student.get('exercises', [])) == 0:
                needs_attention.append(f"📝 **{student['name']}** - No workouts logged")
            elif student.get('napfa_history'):
                latest_napfa = student['napfa_history'][-1]
                if latest_napfa['total'] < 9:
                    needs_attention.append(f"📉 **{student['name']}** - Low NAPFA score ({latest_napfa['total']}/30)")
        
        if needs_attention:
            for msg in needs_attention[:5]:
                st.warning(msg)
        else:
            st.success("✅ All students doing well!")
    
    with tab4:
        st.subheader("Student List")
        
        if not students_data:
            st.info("No students in your class yet. Share your class code: " + user_data['class_code'])
        else:
            # Search and filter
            search = st.text_input("🔍 Search students", placeholder="Enter name or username")
            
            # Display students
            for username, student in students_data.items():
                if search.lower() in student['name'].lower() or search.lower() in username.lower() or not search:
                    with st.expander(f"👤 {student['name']} (@{username})"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Email:** {student.get('email', 'N/A')}")
                            st.write(f"**Age:** {student.get('age', 'N/A')}")
                            st.write(f"**Gender:** {'Male' if student.get('gender') == 'm' else 'Female'}")
                        
                        with col2:
                            if student.get('napfa_history'):
                                latest = student['napfa_history'][-1]
                                st.write(f"**NAPFA:** {latest['total']}/30")
                                st.write(f"**Medal:** {latest['medal']}")
                            else:
                                st.write("**NAPFA:** Not tested")
                            
                            st.write(f"**Workouts:** {len(student.get('exercises', []))}")
                        
                        with col3:
                            st.write(f"**Level:** {student.get('level', 'Novice')}")
                            st.write(f"**Points:** {student.get('total_points', 0)}")
                            st.write(f"**Login Streak:** {student.get('login_streak', 0)} days")
                        
                        # House info and assignment
                        st.write("")
                        current_house = student.get('house', 'Not assigned')
                        if current_house != 'Not assigned':
                            house_display = {
                                'yellow': '🟡 Yellow',
                                'red': '🔴 Red',
                                'blue': '🔵 Blue',
                                'green': '🟢 Green',
                                'black': '⚫ Black'
                            }
                            st.write(f"**🏠 House:** {house_display.get(current_house, current_house.title())}")
                            st.write(f"**House Points:** {student.get('house_points_contributed', 0):.1f}")
                        else:
                            st.write("**🏠 House:** Not assigned")
                        
                        # House assignment
                        st.write("")
                        house_options = ['yellow', 'red', 'blue', 'green', 'black']
                        new_house = st.selectbox(
                            "Assign to House",
                            house_options,
                            index=house_options.index(current_house) if current_house in house_options else 0,
                            key=f"house_{username}",
                            format_func=lambda x: {'yellow': '🟡 Yellow', 'red': '🔴 Red', 'blue': '🔵 Blue', 
                                                  'green': '🟢 Green', 'black': '⚫ Black'}[x]
                        )
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button(f"Update House", key=f"update_house_{username}"):
                                student['house'] = new_house
                                save_users(all_users)
                                st.success(f"Updated {student['name']}'s house to {new_house.title()}!")
                                st.rerun()
                        
                        with col_b:
                            if st.button(f"Remove from class", key=f"remove_{username}"):
                                user_data['students'].remove(username)
                                student['teacher_class'] = None
                                update_user_data(user_data)
                                save_users(all_users)
                                st.success(f"Removed {student['name']} from class")
                                st.rerun()
    
    with tab5:
        st.subheader("Performance Analysis")
        
        if not students_data:
            st.info("No students to analyze yet")
        else:
            # NAPFA component analysis
            st.write("### 📊 NAPFA Component Breakdown")
            
            component_scores = {
                'Sit-Ups': [],
                'Broad Jump': [],
                'Sit & Reach': [],
                'Pull-Ups': [],
                'Shuttle Run': [],
                '2.4km Run': []
            }
            
            component_map = {
                'SU': 'Sit-Ups',
                'SBJ': 'Broad Jump',
                'SAR': 'Sit & Reach',
                'PU': 'Pull-Ups',
                'SR': 'Shuttle Run',
                'RUN': '2.4km Run'
            }
            
            for student in students_data.values():
                if student.get('napfa_history'):
                    grades = student['napfa_history'][-1]['grades']
                    for code, name in component_map.items():
                        if code in grades:
                            component_scores[name].append(grades[code])
            
            if any(component_scores.values()):
                # Calculate averages
                avg_scores = {name: sum(scores)/len(scores) if scores else 0 
                            for name, scores in component_scores.items()}
                
                df = pd.DataFrame({
                    'Component': list(avg_scores.keys()),
                    'Average Grade': list(avg_scores.values())
                })
                
                st.bar_chart(df.set_index('Component'))
                
                # Identify weak areas
                weak_components = [name for name, avg in avg_scores.items() if avg < 3]
                if weak_components:
                    st.warning(f"⚠️ **Class weak areas:** {', '.join(weak_components)}")
                    st.info("💡 Consider focusing class training on these components")
            
            # Participation trends
            st.write("")
            st.write("### 📈 Weekly Participation Trend")
            
            # Last 4 weeks
            weeks_data = []
            for week in range(4):
                week_start = datetime.now() - timedelta(days=7 * (week + 1))
                week_end = datetime.now() - timedelta(days=7 * week)
                
                active_count = 0
                for student in students_data.values():
                    if student.get('exercises'):
                        for exercise in student['exercises']:
                            ex_date = datetime.strptime(exercise['date'], '%Y-%m-%d')
                            if week_start <= ex_date < week_end:
                                active_count += 1
                                break
                
                weeks_data.append({
                    'Week': f"Week {4-week}",
                    'Active Students': active_count
                })
            
            df_weeks = pd.DataFrame(weeks_data)
            st.line_chart(df_weeks.set_index('Week'))
    
    with tab6:
        st.subheader("Export Class Reports")
        
        st.write("### 📊 Google Sheets Export")
        st.info("Generate a comprehensive class report and export to Google Sheets")
        
        # Report options
        include_napfa = st.checkbox("Include NAPFA scores", value=True)
        include_workouts = st.checkbox("Include workout logs", value=True)
        include_attendance = st.checkbox("Include attendance/participation", value=True)
        
        if st.button("📄 Generate Report (Download CSV)", type="primary"):
            if not students_data:
                st.error("No students to export")
            else:
                # Generate report data
                report_data = []
                
                for username, student in students_data.items():
                    row = {
                        'Name': student['name'],
                        'Email': student.get('email', ''),
                        'Age': student.get('age', ''),
                        'Gender': 'Male' if student.get('gender') == 'm' else 'Female'
                    }
                    
                    if include_napfa and student.get('napfa_history'):
                        latest = student['napfa_history'][-1]
                        row['NAPFA Total'] = latest['total']
                        row['Medal'] = latest['medal']
                        row['Sit-Ups'] = latest['grades'].get('SU', 0)
                        row['Broad Jump'] = latest['grades'].get('SBJ', 0)
                        row['Sit & Reach'] = latest['grades'].get('SAR', 0)
                        row['Pull-Ups'] = latest['grades'].get('PU', 0)
                        row['Shuttle Run'] = latest['grades'].get('SR', 0)
                        row['2.4km Run'] = latest['grades'].get('RUN', 0)
                    
                    if include_workouts:
                        row['Total Workouts'] = len(student.get('exercises', []))
                        
                        # This week
                        week_ago = datetime.now() - timedelta(days=7)
                        weekly = [e for e in student.get('exercises', []) 
                                if datetime.strptime(e['date'], '%Y-%m-%d') >= week_ago]
                        row['Workouts This Week'] = len(weekly)
                    
                    if include_attendance:
                        row['Login Streak'] = student.get('login_streak', 0)
                        row['Level'] = student.get('level', 'Novice')
                        row['Total Points'] = student.get('total_points', 0)
                    
                    report_data.append(row)
                
                # Create DataFrame
                df_report = pd.DataFrame(report_data)
                
                # Convert to CSV
                csv = df_report.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv,
                    file_name=f"class_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
                st.success("✅ Report generated! Click to download.")
                
                # Preview
                st.write("### Preview")
                st.dataframe(df_report, use_container_width=True)
        
        st.write("")
        st.write("### 📧 Share Instructions")
        st.info("""
        **To share this report with others:**
        1. Download the CSV file
        2. Upload to Google Sheets
        3. Click Share → Add people (enter emails)
        4. Set permissions (Viewer = read-only, Editor = can edit)
        5. Send the link!
        
        **For automatic Google Sheets export, this feature will be available after deployment.**
        """)

# AI Workout Verification
def ai_workout_verification():
    st.header("📸 AI Workout Verification")
    st.write("Use OpenAI Vision AI to verify your exercise form and get detailed feedback!")
    
    user_data = get_user_data()
    
    # Check API availability
    has_openai = bool(OPENAI_API_KEY)
    
    if has_openai:
        st.success("✅ OpenAI Vision API connected - AI verification active!")
    else:
        st.warning("""
        ⚠️ **Setup Required**: This feature needs an OpenAI API key.
        
        **Quick Setup:**
        1. Get API key from https://platform.openai.com ($5 credit for new accounts)
        2. Add to Streamlit: Settings → Secrets → `OPENAI_API_KEY = "sk-..."`
        3. Cost: ~$0.01 per verification (affordable!)
        
        **Benefits:**
        - 85-95% accuracy in form verification
        - Detailed feedback on your technique
        - Verifies NAPFA exercise standards
        """)
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs([
        "📸 Verify Exercise",
        "📊 Verification History", 
        "ℹ️ Setup Guide"
    ])
    
    with tab1:
        st.subheader("Verify Your Workout")
        
        col1, col2 = st.columns(2)
        
        with col1:
            exercise_type = st.selectbox(
                "Exercise Type",
                ["Pull-Up", "Sit-Up", "Push-Up", "Squat", "Plank", "Jumping Jack", "Other"],
                help="Select the exercise you want to verify"
            )
        
        with col2:
            rep_count = st.number_input(
                "Number of Reps/Duration",
                min_value=1,
                max_value=1000,
                value=10,
                help="How many reps did you do?"
            )
        
        st.write("---")
        st.write("### Upload Exercise Photo/Video Frame")
        st.info("""
        **📷 Photo Tips for Best Results:**
        - Show full body in frame
        - Good lighting (not too dark)
        - Capture at the peak of movement (e.g., top of pull-up, bottom of sit-up)
        - Side view often works best
        - Make sure exercise is clearly visible
        """)
        
        uploaded_file = st.file_uploader(
            "Upload exercise image",
            type=['jpg', 'jpeg', 'png'],
            help="Take a photo during your exercise"
        )
        
        if uploaded_file is not None:
            # Import PIL only when needed
            try:
                from PIL import Image
            except ImportError:
                st.error("PIL (Pillow) library not installed. Please add 'Pillow' to requirements.txt")
                st.stop()
            
            # Display uploaded image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(image, caption="Uploaded Exercise Photo", use_container_width=True)
            
            with col2:
                st.write("**Image Details:**")
                st.write(f"Size: {image.size[0]}x{image.size[1]}")
                st.write(f"Format: {image.format}")
                st.write(f"Exercise: {exercise_type}")
                st.write(f"Reps: {rep_count}")
            
            st.write("---")
            
            # Verification button
            if st.button("🔍 Verify Exercise Form", type="primary"):
                if not has_openai:
                    st.error("""
                    ⚠️ **OpenAI API Key Required**
                    
                    To use AI workout verification, you need to:
                    1. Get an API key from https://platform.openai.com
                    2. Add it to Streamlit secrets as `OPENAI_API_KEY`
                    3. Restart the app
                    
                    Cost: ~$0.01 per verification (very affordable!)
                    """)
                else:
                    with st.spinner("🤖 AI analyzing exercise form..."):
                        is_valid, feedback, confidence = verify_workout_with_openai(image, exercise_type)
                    
                    st.write("### Verification Results")
                    
                    if is_valid is None:
                        st.error(f"⚠️ Verification failed: {feedback}")
                    elif is_valid:
                        st.success(f"✅ **VALID {exercise_type.upper()}**")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Status", "VERIFIED ✓")
                        with col2:
                            st.metric("Reps Counted", rep_count)
                        with col3:
                            st.metric("Confidence", f"{confidence}%")
                        
                        st.write("**AI Feedback:**")
                        st.info(feedback)
                        
                        # Save verification to history
                        if 'workout_verifications' not in user_data:
                            user_data['workout_verifications'] = []
                        
                        user_data['workout_verifications'].append({
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'time': datetime.now().strftime('%H:%M:%S'),
                            'exercise': exercise_type,
                            'reps': rep_count,
                            'valid': True,
                            'confidence': confidence,
                            'feedback': feedback
                        })
                        
                        # Also add to exercise log
                        user_data['exercises'].append({
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'type': exercise_type,
                            'duration': rep_count,  # Using duration field for reps
                            'notes': f'AI Verified ({confidence}% confidence)',
                            'verified': True
                        })
                        
                        update_user_data(user_data)
                        
                        st.success("💾 Exercise saved to your log!")
                        
                        # Award points for verified workout
                        points_earned = min(rep_count * 2, 50)  # Cap at 50 points
                        st.balloons()
                        st.success(f"🎉 +{points_earned} points earned!")
                        
                    else:
                        st.warning(f"⚠️ **FORM ISSUES DETECTED**")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Status", "NEEDS IMPROVEMENT")
                        with col2:
                            st.metric("Attempted Reps", rep_count)
                        with col3:
                            st.metric("Confidence", f"{confidence}%")
                        
                        st.write("**AI Feedback:**")
                        st.warning(feedback)
                        
                        st.info("""
                        **💡 Tips to Improve:**
                        - Review the form guide below
                        - Try the exercise again with corrections
                        - Take a clearer photo showing full range of motion
                        - Consider recording a video for better analysis
                        """)
                        
                        # Save verification to history (even invalid ones for learning)
                        if 'workout_verifications' not in user_data:
                            user_data['workout_verifications'] = []
                        
                        user_data['workout_verifications'].append({
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'time': datetime.now().strftime('%H:%M:%S'),
                            'exercise': exercise_type,
                            'reps': rep_count,
                            'valid': False,
                            'confidence': confidence,
                            'feedback': feedback
                        })
                        update_user_data(user_data)
        
        # Exercise form guides
        st.write("---")
        st.write("### 📖 Exercise Form Guides")
        
        with st.expander(f"✓ {exercise_type} - Proper Form Guide"):
            if exercise_type == "Pull-Up":
                st.write("""
                **Proper Pull-Up Form:**
                1. **Starting Position:** Hang from bar with arms fully extended, palms facing away
                2. **Grip:** Slightly wider than shoulder-width
                3. **Movement:** Pull yourself up until chin is above the bar
                4. **Control:** Lower yourself back down with control (no dropping)
                5. **Body:** Keep core tight, no swinging or kipping
                6. **Breathing:** Exhale going up, inhale going down
                
                **Common Mistakes:**
                - ❌ Not going to full extension at bottom
                - ❌ Chin not clearing the bar
                - ❌ Excessive swinging/kipping
                - ❌ Jerky movements
                """)
            elif exercise_type == "Sit-Up":
                st.write("""
                **Proper Sit-Up Form:**
                1. **Starting Position:** Lie flat on back, knees bent, feet flat on floor
                2. **Hand Position:** Behind head or crossed on chest (don't pull on neck)
                3. **Movement:** Lift shoulders and upper back off ground, curl toward knees
                4. **Peak:** Torso should reach vertical or near-vertical position
                5. **Return:** Lower back down with control
                6. **Breathing:** Exhale going up, inhale going down
                
                **Common Mistakes:**
                - ❌ Pulling on neck with hands
                - ❌ Using momentum instead of core strength
                - ❌ Not lifting shoulders completely off ground
                - ❌ Feet coming off ground
                """)
            elif exercise_type == "Push-Up":
                st.write("""
                **Proper Push-Up Form:**
                1. **Starting Position:** Plank position, hands shoulder-width apart
                2. **Body Alignment:** Straight line from head to heels
                3. **Movement:** Lower body until chest nearly touches ground (elbows at 90°)
                4. **Push:** Press back up to starting position
                5. **Core:** Keep abs tight, don't let hips sag or pike up
                6. **Breathing:** Inhale going down, exhale pushing up
                
                **Common Mistakes:**
                - ❌ Hips sagging (banana back)
                - ❌ Hips too high (pike position)
                - ❌ Not going deep enough
                - ❌ Flaring elbows too wide
                """)
            else:
                st.write(f"Form guide for {exercise_type} - Maintain proper posture and control throughout the movement.")
    
    with tab2:
        st.subheader("📊 Verification History")
        
        if user_data.get('workout_verifications'):
            verifications = user_data['workout_verifications']
            
            # Summary stats
            total_verifications = len(verifications)
            valid_count = sum(1 for v in verifications if v['valid'])
            invalid_count = total_verifications - valid_count
            success_rate = (valid_count / total_verifications * 100) if total_verifications > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Verified", total_verifications)
            with col2:
                st.metric("Valid ✓", valid_count)
            with col3:
                st.metric("Needs Work", invalid_count)
            with col4:
                st.metric("Success Rate", f"{success_rate:.0f}%")
            
            # Recent verifications
            st.write("")
            st.write("### Recent Verifications")
            
            df_verify = pd.DataFrame(verifications)
            df_verify = df_verify.sort_values('date', ascending=False)
            
            # Display with color coding
            for idx, row in df_verify.head(10).iterrows():
                status_color = "#4caf50" if row['valid'] else "#ff9800"
                status_text = "✓ VALID" if row['valid'] else "⚠ NEEDS WORK"
                
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: {status_color};">
                    <strong>{row['date']} {row['time']}</strong> - {row['exercise']}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">{status_text}</span><br>
                    <strong>Reps:</strong> {row['reps']} | <strong>Confidence:</strong> {row['confidence']}%<br>
                    <em>{row['feedback'][:100]}...</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No verifications yet. Upload your first workout photo to get started!")
    
    with tab3:
        st.subheader("📖 Setup Guide")
        
        st.write("### 🚀 Quick Setup (5 minutes)")
        
        st.write("**Step 1: Get OpenAI API Key**")
        st.code("""
1. Go to https://platform.openai.com
2. Sign up or log in
3. Click "API Keys" in left menu
4. Click "Create new secret key"
5. Copy the key (starts with sk-...)
        """)
        
        st.write("**Step 2: Add to Streamlit**")
        if has_openai:
            st.success("✅ Already configured!")
        else:
            st.code("""
In Streamlit Cloud:
1. Go to your app dashboard
2. Click "Settings" → "Secrets"
3. Add this line:
   OPENAI_API_KEY = "sk-your-key-here"
4. Click "Save"
5. App will restart automatically
            """)
        
        st.write("**Step 3: Test It**")
        st.info("""
        1. Take a photo of yourself doing an exercise
        2. Upload it in the "Verify Exercise" tab
        3. Click "Verify Exercise Form"
        4. Get instant AI feedback!
        """)
        
        st.write("---")
        st.write("### 💰 Pricing")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Per Verification", "~$0.01")
            st.write("Very affordable!")
        
        with col2:
            st.metric("30 Students/Week", "~$1.50")
            st.write("5 verifications each")
        
        st.info("""
        **New users get $5 free credit** - that's ~500 verifications to test!
        
        Monthly cost for a class of 30:
        - 5 verifications/student/week
        - 30 students × 5 = 150 verifications/week
        - 150 × $0.01 = $1.50/week
        - **Monthly: ~$6-7**
        """)
        
        st.write("---")
        st.write("### 📸 Photo Tips for Best Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**✅ DO:**")
            st.write("""
            - Show full body in frame
            - Good lighting (natural light best)
            - Capture at peak of movement
            - Simple background
            - Side view for most exercises
            - Wear contrasting colors
            """)
        
        with col2:
            st.write("**❌ DON'T:**")
            st.write("""
            - Dim lighting
            - Cut off limbs
            - Multiple people
            - Blurry images
            - Too far away
            - Cluttered background
            """)
        
        st.write("---")
        st.write("### 🎯 Expected Accuracy")
        
        accuracy_data = pd.DataFrame({
            'Exercise': ['Pull-ups', 'Sit-ups', 'Push-ups', 'Squats'],
            'Accuracy': [90, 85, 90, 85]
        })
        
        st.bar_chart(accuracy_data.set_index('Exercise'))
        
        st.info("""
        **What AI Checks:**
        - Pull-ups: Full arm extension, chin above bar, no kipping
        - Sit-ups: Back flat, shoulders lifting, controlled movement
        - Push-ups: Body alignment, elbow angle, full range
        - Squats: Depth, knee position, back straight
        """)
        
        st.write("---")
        st.write("### 🔒 Privacy & Security")
        st.success("""
        **Your data is safe:**
        - Images processed in real-time only
        - Not stored by OpenAI (per API terms)
        - Only verification results saved
        - No image sharing between users
        - Students see only their own data
        - Teachers see aggregated stats only
        """)
        
        st.write("---")
        st.write("### 🐛 Troubleshooting")
        
        with st.expander("❓ API key not working"):
            st.write("""
            - Check key starts with `sk-`
            - Verify copied correctly (no spaces)
            - Make sure you added to Streamlit Secrets, not local file
            - Restart app after adding
            - Check API quota at platform.openai.com
            """)
        
        with st.expander("❓ Low confidence scores"):
            st.write("""
            - Retake with better lighting
            - Show full body in frame
            - Use side angle
            - Ensure good contrast
            - Take at peak of movement
            """)
        
        with st.expander("❓ 'No person detected' error"):
            st.write("""
            - Full body must be visible
            - Check lighting
            - Try different angle
            - Center person in frame
            - Reduce background clutter
            """)

# Schedule Manager
def schedule_manager():
    st.header("📅 Training Schedule")
    
    with st.form("schedule_form"):
        day = st.selectbox("Day of Week", 
                          ["Monday", "Tuesday", "Wednesday", "Thursday", 
                           "Friday", "Saturday", "Sunday"])
        activity = st.text_input("Activity", placeholder="e.g., Morning run")
        
        col1, col2 = st.columns(2)
        with col1:
            time = st.time_input("Time")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=30)
        
        submitted = st.form_submit_button("Add to Schedule")
        
        if submitted:
            if activity:
                user_data = get_user_data()
                user_data['schedule'].append({
                    'day': day,
                    'activity': activity,
                    'time': str(time),
                    'duration': duration
                })
                update_user_data(user_data)
                st.success("Activity added to schedule!")
                st.rerun()
            else:
                st.error("Please enter activity name")
    
    # Display schedule
    user_data = get_user_data()
    if user_data['schedule']:
        st.subheader("Weekly Schedule")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in days:
            day_activities = [s for s in user_data['schedule'] if s['day'] == day]
            if day_activities:
                st.markdown(f"### {day}")
                for activity in day_activities:
                    st.markdown(f'<div class="stat-card"><strong>{activity["activity"]}</strong><br>{activity["time"]} - {activity["duration"]} minutes</div>', 
                              unsafe_allow_html=True)
    else:
        st.info("No activities scheduled yet.")

# Main App
def main_app():
    user_data = get_user_data()
    
    # Check if teacher or student
    is_teacher = user_data.get('role') == 'teacher'
    
    # Header with logout
    col1, col2 = st.columns([4, 1])
    with col1:
        if is_teacher:
            st.markdown(f'<div class="main-header"><h1>🏋️ FitTrack - Teacher Portal</h1><p>Welcome, {user_data["name"]}!</p></div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="main-header"><h1>🏋️ FitTrack</h1><p>Welcome back, {user_data["name"]}!</p></div>', 
                       unsafe_allow_html=True)
    with col2:
        st.write("")
        st.write("")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    # Different interface for teachers vs students
    if is_teacher:
        teacher_dashboard()
    else:
        # Update login streak for students
        user_data = update_login_streak(user_data)
        update_user_data(user_data)
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Choose a feature:", 
                               ["📊 Weekly Progress", "🏆 Community", "🤖 AI Insights", 
                                "🏥 Advanced Metrics", "🌐 Integrations",
                                "💪 Log Workout", 
                                "BMI Calculator", "NAPFA Test", "Sleep Tracker", 
                                "Training Schedule"])
        
        # Display selected page
        if page == "📊 Weekly Progress":
            reminders_and_progress()
        elif page == "🏆 Community":
            community_features()
        elif page == "🤖 AI Insights":
            ai_insights()
        elif page == "🏥 Advanced Metrics":
            advanced_metrics()
        elif page == "🌐 Integrations":
            api_integrations()
        elif page == "💪 Log Workout":
            exercise_logger()  # This now has Timer + AI Verification + Steps Tracker + History
        elif page == "BMI Calculator":
            bmi_calculator()
        elif page == "NAPFA Test":
            napfa_calculator()
        elif page == "Sleep Tracker":
            sleep_tracker()
        elif page == "Training Schedule":
            schedule_manager()

# Main execution
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
