html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Chatbot - Testing Page</title>
    <!-- Dialogflow Messenger -->
        <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
        <df-messenger
            chat-icon="https://mariuskalder.io/images/weather_chatbot/weather_chatbot.png"
            intent="WELCOME"
            chat-title="Weather Chatbot"
            agent-id="ff8cce25-9114-4589-97f7-5c0d64b1dd5d"
            language-code="en">
    </df-messenger>
</head>
<style>
    /* General Styles */
    body {
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #eef5ff; /* Light blue background */
        color: #333;
    }

    /* Container for main content */
    .container {
        max-width: 800px;
        margin: 50px auto;
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0px 4px 20px rgba(0, 123, 255, 0.2);
    }

    h1 {
        color: #007bff;
        font-size: 26px;
        margin-bottom: 20px;
    }

    h2 {
        color: #0056b3;
        font-size: 22px;
    }

    p {
        font-size: 16px;
        color: #555;
    }

    /* Table Styling */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0px 4px 12px rgba(0, 123, 255, 0.15);
    }

    th, td {
        padding: 12px;
        text-align: left;
    }

    th {
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }

    td {
        background-color: #f8f9fa;
    }

    tr:nth-child(even) td {
        background-color: #e9f1ff;
    }

    /* Link Styling */
    a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }

    a:hover {
        text-decoration: underline;
    }

    /* Chatbot Floating Button */
    df-messenger {
        --df-messenger-bot-message: #eef5ff;
        --df-messenger-font-color: #000;
        --df-messenger-chat-background: #ffffff;
        --df-messenger-button-titlebar-color: #007bff;
        --df-messenger-send-icon: #007bff;
        position: fixed;
        bottom: 30px;
        right: 30px;
    }

    /* Webhook Status Section */
    .status-container {
        text-align: center;
        margin-top: 20px;
    }

    /* Footer */
    .footer {
        margin-top: 20px;
        font-size: 14px;
        color: #555;
        text-align: center;
    }
</style>
<body>
    <div class="container">
        <h1>Weather Chatbot Testing Page</h1>
        <p>This chatbot provides weather data updates and answers waether related queries. Below are some example questions and expected responses.</p>
        <h2>Test Questions</h2>
        <table>
            <tr>
                <th>Test Question</th>
                <th>Expected Outcome</th>
            </tr>
            <td>Hello how are you?</td>
            <td><b>Example answer:</b><br> 
            I’m always feeling bright and ready to deliver forecasts! How about you?
            </td>
              <tr>
                <td>I need help!</td>
                <td><b>Example answer:</b> <br>
                Whether it’s heavy rain, strong winds, or perfect beach weather, let me know what you’re looking for!
                </td>
            </tr>
            <tr>
                <td>What's the weather like in Bangkok?</td>
                <td>📍Bangkok:<br>
                📅 {day name}, {month} {day}, {year}<br>
                ⛅ Weather: {weather condtion}<br>
                🌡️ Temperature: 🔽 {min temp} → 🔼 {max temp}<br>
                💨 Wind Speed: {wind speed} in m/s
                </td>
            </tr>
            <tr>
                <td>Will it rain tomorrow in Phuket?</td>
                <td>📍Phuket:<br>
                📅 {day name}, {month} {day}, {year}<br>
                {weahter icon - condtion} Weather: If yes: {weather condtion} Else: No {weather condtion}<br>
                </td>
            </tr>
            <tr>
                <td>Will it be warm in Munich?</td>
                <td>📍Munich:<br>
                📅 {day name}, {month} {day}, {year}<br>
                🌡️🔽 Temperature: {min temp}<br>
                🌡️🔼 Temperature: {max temp}
                </td>
            </tr>
            <tr>
                <td>What’s the UV index today?</td>
                <td><b>Example answer:</b><br>
                Sorry, I can only help with weather updates. Try asking something like: ‘What’s the temperature in Bangkok?’ ☀️
                </td>
            </tr>
            <tr>
                <td>How was the weather last week in New York?</td>
                <td><b>Example answer:</b><br>
                Past weather is history! Let’s talk about what’s ahead. Ask me about future forecasts.🌍⏳
                </td>
            </tr>
        </table>

        <div class="status-container">
            <h2>Webhook Status</h2>
            <p><strong>Status:</strong> ✅ Online</p>
            <p>Powered by: <strong>Marius Kalder</strong></p>
            <p>GitHub: <a href="https://github.com/MKalder/ai_weather_chatbot" target="_blank">GitHub Repository</a></p>
            <p>Email: <a href="mailto:aiweatherchatbot@mariuskalder.io">aiweatherchatbot@mariuskalder.io</a></p>
            <p>Website: <a href="https://mariuskalder.io" target="_blank">www.mariuskalder.io</a></p>
            <p>LikedIn: <a href="https://www.linkedin.com/in/marius-kalder/" target="_blank">Marius Kalder</a></p>
        </div>
    </div>
    <div class="footer">
        © 2025 Weather Chatbot by Marius Kalder
    </div>
    <div style="margin-bottom: 50px;"></div>
</body>
</html>'''