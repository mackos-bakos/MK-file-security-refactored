import os
from tkinter import filedialog
from flask import Flask, render_template, request, session, redirect, url_for

from utilities.funcs import *
from utilities.utils import *

root = tk.Tk()
root.withdraw()
    
path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "ReplaceMeIfNeeded"
selected_directory = ""

while not selected_directory:
    selected_directory = filedialog.askdirectory()

print(f"directory selection: {selected_directory}")
@app.route('/')
def render_ui():
    return render_template('menu.html')

@app.route("/purge", methods=["POST"])
def purge():
    file_types = request.form.get("purge")
    if ',' not in file_types and len(file_types) > 1:
        file_types = [file_types]
    else:
        file_types = file_types.split(",")

    if file_types == ['']:
        return redirect(url_for('render_ui'))

    purge_directory(selected_directory, file_types, True)
    return redirect(url_for('render_ui'))

@app.route("/decrypt", methods=["POST"])
def decrypt():
    decryption_key = request.form.get("decryptionKey")
    keep_original = request.form.get("keepOriginal")
    seperate = request.form.get("keepDecrypted")
    should_hash_decrypt = request.form.get("HashKeyDecrypt")
    if should_hash_decrypt:
        decryption_key = hash_md5(decryption_key)
    if decryption_key == "":
        return redirect(url_for('render_ui'))
    decrypt_directory(selected_directory,not keep_original,True,seperate,decryption_key)
    return redirect(url_for('render_ui'))

@app.route("/encrypt", methods=["POST"])
def encrypt():
    backup = request.form.get("backup")
    keep_decrypted = request.form.get("keepDecrypted")
    encryption_key = request.form.get("encryptionKey")
    should_hash_encrypt = request.form.get("HashKeyEncrypt")
    if should_hash_encrypt:
        encryption_key = hash_md5(encryption_key)
    if encryption_key == "":
        return redirect(url_for('render_ui'))
    encrypt_directory(selected_directory,not keep_decrypted,True,backup,encryption_key)
    return redirect(url_for('render_ui'))

@app.route("/obscure", methods=["POST"])
def obscure():
    obscure_directory(selected_directory)
    return redirect(url_for('render_ui'))

@app.route("/swap", methods=["POST"])
def swap():
    swap_from = request.form.get("swapFrom")
    swap_to = request.form.get("swapTo")
    if "." not in swap_from or "." not in swap_to:
        return redirect(url_for('render_ui'))
    swap_file_extensions(selected_directory,swap_from,swap_to)
    return redirect(url_for('render_ui'))

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
