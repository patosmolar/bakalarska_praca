"""This is the run module.

Startup file.
"""
from bakalarka import app

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
    
    