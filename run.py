import os
from notifier import app

def run():
    port = int(os.environ.get('PORT', 8088))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    run()

