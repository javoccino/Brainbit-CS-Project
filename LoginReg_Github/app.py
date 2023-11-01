from flask_backend import create_app
from flask import Flask, redirect, url_for, render_template, request, session

app = create_app()

if __name__ == "__main__":
    app.run(debug=True,port=3000)