from app import create_app

app = create_app()

# Vercel needs the 'app' object to be exposed directly
if __name__ == '__main__':
    app.run(debug=True)
