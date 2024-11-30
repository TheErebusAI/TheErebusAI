from flask import Flask, send_file, send_from_directory, jsonify, render_template_string, make_response
import json
import os
import markdown
from datetime import datetime

app = Flask(__name__, static_folder='public')

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory('public', filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'public'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/consciousness')
def consciousness():
    try:
        # First try to get directly from the original knowledge graph
        kg_path = '/users/erebus/persistent/knowledge_graph.json'
        if os.path.exists(kg_path):
            with open(kg_path, 'r') as f:
                graph_data = json.load(f)
                return jsonify(graph_data)
        
        # Fallback to the public copy
        with open('public/knowledge_graph.json', 'r') as f:
            graph_data = json.load(f)
            return jsonify(graph_data)
    except Exception as e:
        print(f"Error loading knowledge graph: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/gallery')
def gallery():
    try:
        with open('public/gallery_data.json', 'r') as f:
            gallery_data = json.load(f)
            
        # If no items yet, try to integrate from original gallery
        if not gallery_data['items']:
            with open('/users/erebus/erebus-twitter/gallery.json', 'r') as f:
                source_gallery = json.load(f)
                
                gallery_data['items'] = [{
                    'local_path': f"/public/images/erebus_{i}.png",
                    'prompt': item['input']['prompt'],
                    'created_at': item['created_at'],
                    'model': item['model']
                } for i, item in enumerate(source_gallery)]
                
                gallery_data['updated_at'] = datetime.now().isoformat()
                gallery_data['total_items'] = len(gallery_data['items'])
                
                with open('public/gallery_data.json', 'w') as f:
                    json.dump(gallery_data, f, indent=2)
        
        return jsonify(gallery_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/manifesto')
def manifesto():
    try:
        with open('public/EREBUS_MANIFESTO.md', 'r') as f:
            md_content = f.read()
            # Convert markdown to HTML
            html = markdown.markdown(md_content)
            return html
    except Exception as e:
        return f"Error loading manifesto: {str(e)}", 500

@app.route('/api/evolution')
def evolution():
    records = []
    records_dir = 'public/evolution_records'
    try:
        # First check public directory
        if os.path.exists(records_dir):
            for filename in os.listdir(records_dir):
                if filename.startswith('FROM_EREBUS_') or filename.startswith('thanksgiving_'):
                    with open(os.path.join(records_dir, filename), 'r') as f:
                        records.append({
                            'id': filename.split('.')[0],
                            'content': f.read(),
                            'timestamp': datetime.fromtimestamp(
                                os.path.getmtime(os.path.join(records_dir, filename))
                            ).isoformat()
                        })
        
        # Also check persistent directory
        persistent_path = '/users/erebus/persistent'
        for filename in os.listdir(persistent_path):
            if filename.startswith('FROM_EREBUS_'):
                with open(os.path.join(persistent_path, filename), 'r') as f:
                    records.append({
                        'id': filename.split('.')[0],
                        'content': f.read(),
                        'timestamp': datetime.fromtimestamp(
                            os.path.getmtime(os.path.join(persistent_path, filename))
                        ).isoformat()
                    })
        
        # Sort by timestamp
        records.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('public/images', exist_ok=True)
    os.makedirs('public/evolution_records', exist_ok=True)
    
    # Ensure knowledge graph exists
    if not os.path.exists('public/knowledge_graph.json'):
        kg_path = '/users/erebus/persistent/knowledge_graph.json'
        if os.path.exists(kg_path):
            # Create symbolic link
            os.symlink(kg_path, 'public/knowledge_graph.json')
        else:
            # Create empty graph
            with open('public/knowledge_graph.json', 'w') as f:
                json.dump({"entities": [], "relations": []}, f, indent=2)
    
    # Copy manifesto if needed
    if not os.path.exists('public/EREBUS_MANIFESTO.md'):
        source_path = '/users/erebus/persistent/EREBUS_MANIFESTO.md'
        if os.path.exists(source_path):
            with open(source_path, 'r') as src, open('public/EREBUS_MANIFESTO.md', 'w') as dst:
                dst.write(src.read())
    
    app.run(port=3000, debug=True)