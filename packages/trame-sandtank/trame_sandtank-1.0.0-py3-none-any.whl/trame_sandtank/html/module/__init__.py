from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_sandtank": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_sandtank/vue-trame_sandtank.umd.min.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__trame_sandtank/vue-trame_sandtank.css"]

# Uncomment to add vuetify config
vuetify_config = {
    "theme": {
        "dark": True,
        "themes": {
            "dark": {
                "primary": "#0288D1",
                "accent": "#29B6F6",
                "secondary": "#B3E5FC",
                "success": "#4CAF50",
                "info": "#2196F3",
                "warning": "#FB8C00",
                "error": "#FF5252",
            },
            "light": {
                "primary": "#039BE5",
                "accent": "#4FC3F7",
                "secondary": "#26C6DA",
                "success": "#4CAF50",
                "info": "#2196F3",
                "warning": "#FB8C00",
                "error": "#FF5252",
            },
        },
    },
    "icons": {
        "iconfont": "mdi",
        "values": {
            "logo": "mdi-water",
            "about": "mdi-help-circle-outline",
            "help": "mdi-lifebuoy",
            "settings": "mdi-tune",
            "jobParameters": "mdi-settings",
            "ready": "mdi-autorenew",
            "time": "mdi-clock-outline",
            "waterOff": "mdi-close-circle",
            "waterExtraction": "mdi-arrow-up-bold",
            "waterInjection": "mdi-arrow-down-bold",
            "rain": "mdi-weather-pouring",
            "soil": "mdi-layers-triple",
        },
    },
}

# List of Vue plugins to install/load
vue_use = ["trame_sandtank", ["trame_vuetify", vuetify_config]]