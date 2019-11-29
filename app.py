import os
import pickle
from helper import Index
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index_doc.html')


@app.route('/index', methods=['GET', 'POST'])
def index_documents():
    message = "Please enter the document content.."
    if request.method == 'POST':
        if not request.form['document']:
            return render_template("index_doc.html", message=message)
        else:
            data = request.form['document']
            with open('./database/documents.txt', 'w') as f:
                f.write(data)
            obj = Index('./database/documents.txt')
            obj.index_doc()
            return render_template("index_acknowledgment.html")
    else:
        return render_template("index_doc.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    index_path = './database/index.pickle'
    docid_path = './database/doc_id.pickle'
    if request.method == 'POST' and request.form['word']:
        word = request.form['word'].lower().strip()
        if os.path.exists(index_path) and os.path.exists(docid_path):
            with open(index_path, 'rb') as fp0:
                index = pickle.load(fp0)
            with open(docid_path, 'rb') as fp1:
                doc_id = pickle.load(fp1)
            if index.get(word) is None:
                return render_template('search_results.html', ptype='nfound', message='No match found!!')
            else:
                output = [doc_id.get(_id, None) for _id in index.get(word)]
                if len(output) > 10:
                    output = output[:10]
                return render_template('search_results.html', output=output, ptype='found')
        else:
            return render_template('search_results.html', message='No index found!!', ptype='nexists')
    else:
        return render_template('search_form.html')


@app.route('/clear')
def clear_indexed_data():
    index_path = './database/index.pickle'
    docid_path = './database/doc_id.pickle'
    if os.path.exists(index_path) and os.path.exists(docid_path):
        os.remove(index_path)
        os.remove(docid_path)
        return render_template('clear_index.html')


if __name__ == '__main__':
    app.run()
