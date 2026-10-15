import sys
import re
import os
import json

def parse_srt(srt_path):
    """
    Parse an SRT file into a list of clean subtitle entries.
    Returns: list of dicts: [{'index': 1, 'start': '00:00:04', 'end': '00:00:09', 'text': '...'}]
    """
    if not os.path.exists(srt_path):
        print(f"Error: File not found {srt_path}", file=sys.stderr)
        return []

    with open(srt_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Normalize newlines
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split by double newline or block patterns
    blocks = re.split(r'\n\s*\n', content.strip())
    entries = []

    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if len(lines) < 2:
            continue
        
        # Check if first line is number
        idx = None
        time_line_idx = 1
        if re.match(r'^\d+$', lines[0]):
            idx = int(lines[0])
            time_line = lines[1]
            text_lines = lines[2:]
        elif '-->' in lines[0]:
            time_line = lines[0]
            text_lines = lines[1:]
        else:
            continue

        time_match = re.search(r'(\d{2}:\d{2}:\d{2})[,\.]\d{3}\s*-->\s*(\d{2}:\d{2}:\d{2})[,\.]\d{3}', time_line)
        if not time_match:
            continue
        
        start_time = time_match.group(1)
        end_time = time_match.group(2)
        
        text = ' '.join(text_lines)
        # Clean music / sound effect brackets
        text = re.sub(r'\[.*?\]', '', text).strip()
        text = re.sub(r'\(.*?\)', '', text).strip()
        text = re.sub(r'\s+', ' ', text)
        
        if text:
            entries.append({
                'index': idx if idx is not None else len(entries) + 1,
                'start': start_time,
                'end': end_time,
                'text': text
            })
            
    return entries

def group_subtitles_by_interval(entries, interval_minutes=2):
    """
    Groups subtitle entries into larger logical blocks by time interval.
    """
    groups = []
    current_group = []
    current_start = None
    
    def time_to_seconds(t_str):
        parts = list(map(int, t_str.split(':')))
        return parts[0] * 3600 + parts[1] * 60 + parts[2]

    interval_sec = interval_minutes * 60

    for entry in entries:
        t_sec = time_to_seconds(entry['start'])
        if current_start is None:
            current_start = t_sec
            
        if t_sec - current_start >= interval_sec and current_group:
            groups.append({
                'start': current_group[0]['start'],
                'end': current_group[-1]['end'],
                'text': ' '.join([e['text'] for e in current_group])
            })
            current_group = [entry]
            current_start = t_sec
        else:
            current_group.append(entry)

    if current_group:
        groups.append({
            'start': current_group[0]['start'],
            'end': current_group[-1]['end'],
            'text': ' '.join([e['text'] for e in current_group])
        })

    return groups

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse_srt.py <path_to_srt> [--grouped [minutes]]")
        sys.exit(1)
        
    srt_file = sys.argv[1]
    entries = parse_srt(srt_file)
    
    if '--grouped' in sys.argv:
        mins = 3
        try:
            g_idx = sys.argv.index('--grouped')
            if len(sys.argv) > g_idx + 1:
                mins = int(sys.argv[g_idx + 1])
        except:
            pass
        groups = group_subtitles_by_interval(entries, interval_minutes=mins)
        print(json.dumps(groups, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
