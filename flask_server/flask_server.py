import os

from flask import Flask, render_template

app = Flask(__name__)


def _find_latest_log(path_to_logs_dir):
    max_mtime = 0
    max_file = None
    for dirname, subdirs, files in os.walk(path_to_logs_dir):
        for fname in files:
            full_path = os.path.join(dirname, fname)
            mtime = os.stat(full_path).st_mtime
            if mtime > max_mtime:
                max_mtime = mtime
                max_file = full_path
    return max_file


@app.route("/")
def main():
    latest_log_path = _find_latest_log("/home/pi/PycharmProjects/sensor_testing/logs")
    with open(latest_log_path) as f:
        last_line = f.readlines()[-1]
    date, temp, probe_temp, pressure, light = last_line.split(',')
    return render_template('index.html', date=date, temp=temp, probe_temp=probe_temp, pressure=pressure, light=light)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)