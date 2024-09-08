import subprocess

def other_media_playing():
    result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE, text=True)
    
    output = result.stdout
    inputs = []
    current_input = {}
    
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Sink Input #"):
            if current_input:
                inputs.append(current_input)
            current_input = {'id': line.split('#')[1].strip(), 'corked': False, 'muted': False}
        elif 'media.name' in line:
            current_input['media_name'] = line.split('=')[1].strip().strip('"')
        elif 'application.name' in line:
            current_input['application_name'] = line.split('=')[1].strip().strip('"')
        elif 'application.process.binary' in line:
            current_input['process_binary'] = line.split('=')[1].strip().strip('"')
        elif 'Corked: yes' in line:
            current_input['corked'] = True
        elif 'Mute: yes' in line:
            current_input['muted'] = True

    if current_input:
        inputs.append(current_input)
    
    for input in inputs:
        if 'python' in input.get('process_binary', '') and 'VLC' in input.get('application_name', ''):
            continue
        if not (input.get('corked') or input.get('muted')):
            return True
    
    return False


