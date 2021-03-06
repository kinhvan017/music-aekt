from flask import (abort, Blueprint, current_app, jsonify, render_template,
                   request)

from music_aekt.player import moc
from music_aekt.tasks import download


main = Blueprint('main', __name__)


@main.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('music_link')
        print(url)
        download.delay(url)
    return render_template('index.html')

@main.route('/play', methods=['GET'])
def play():
    _, status = moc.play()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/playit', methods=['GET', 'POST'])
def playit():
    if request.method == 'GET':
        mp3_file = request.args.get('file')
    elif request.method == 'POST':
        mp3_file = request.form.get('file')
    _, status =  moc.playit(mp3_file)
    if status != 0:
        abort(500)
    return "OK"

@main.route('/stop', methods=['GET'])
def stop():
    _, status = moc.stop()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/next', methods=['GET'])
def next():
    _, status = moc.next_()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/prev', methods=['GET'])
def prev():
    _, status = moc.prev()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/pause', methods=['GET'])
def pause():
    _, status = moc.pause()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/togglePause', methods=['GET'])
def togglePause():
    _, status = moc.togglePause()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/unpause', methods=['GET'])
def unpause():
    _, status = moc.pause()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/clear', methods=['GET'])
def clear():
    _, status = moc.clear()
    if status != 0:
        abort(500)
    return "OK"

@main.route('/info', methods=['GET'])
def info():
    output, exit_code = moc.show_current_song()
    if exit_code == 0:
        payload = _create_info_dict(output)
        return jsonify(payload)
    return '{}', 500

@main.route('/playlist', methods=['GET'])
def playlist():
    playlist = moc.show_play_list()
    payload = _create_playlist_dict(playlist)
    return jsonify(payload)

@main.route('/volume_up', methods=['GET'])
def volume_up():
    _, status = moc.volume(level='up')
    if status != 0:
        abort(500)
    return 'OK'

@main.route('/volume_down', methods=['GET'])
def volume_down():
    _, status = moc.volume(level='down')
    if status != 0:
        abort(500)
    return 'OK'

def _create_info_dict(info):
    info = info.decode('utf-8')
    d = {}
    for item in info.splitlines():
        key = item.split(":")[0]
        val = item.split(":")[1].strip()
        d[key] = val
    return d

def _create_playlist_dict(playlist):
    d = {'playlist': []}
    for length, title, path in playlist:
        info = {}
        info['length'] = int(length)
        info['title'] = title.split('/')[-1].split('.mp3')[0]
        info['path'] = path
        d['playlist'].append(info)
    return d
