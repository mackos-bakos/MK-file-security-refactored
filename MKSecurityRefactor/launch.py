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
        return render_template('menu.html', purge_output_colour="red", purge_output_message=f"command execution failed with params {file_types}")

    purge_directory(selected_directory, file_types, True)
    return render_template('menu.html', purge_output_colour="white", purge_output_message=f"command executed with params {file_types}")

@app.route("/decrypt", methods=["POST"])
def decrypt():
    decryption_key = request.form.get("decryptionKey")
    keep_original = request.form.get("keepOriginal")
    seperate = request.form.get("keepDecrypted")
    should_hash_decrypt = request.form.get("HashKeyDecrypt")
    if should_hash_decrypt:
        decryption_key = hash_md5(decryption_key)
    if decryption_key == "":
        return render_template('menu.html', decrypt_output_colour="red", decrypt_output_message=f"command execution failed with params {decryption_key}, {keep_original}, {seperate}")
    decrypt_directory(selected_directory,not keep_original,True,seperate,decryption_key)
    return render_template('menu.html', decrypt_output_colour="white", decrypt_output_message=f"command executed with params {decryption_key}, {keep_original}, {seperate}")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    backup = request.form.get("backup")
    keep_decrypted = request.form.get("keepDecrypted")
    encryption_key = request.form.get("encryptionKey")
    should_hash_encrypt = request.form.get("HashKeyEncrypt")
    if should_hash_encrypt:
        encryption_key = hash_md5(encryption_key)
    if encryption_key == "":
        return render_template('menu.html', encrypt_output_colour="red", encrypt_output_message=f"command execution failed with params {encryption_key}, {backup}, {keep_decrypted}")
    encrypt_directory(selected_directory,not keep_decrypted,True,backup,encryption_key)
    return render_template('menu.html', encrypt_output_colour="white", encrypt_output_message=f"command executed with params {encryption_key}, {backup}, {keep_decrypted}")

@app.route("/obscure", methods=["POST"])
def obscure():
    obscure_directory(selected_directory)
    return render_template('menu.html', obscure_output_colour="white", obscure_output_message=f"command executed")

@app.route("/swap", methods=["POST"])
def swap():
    swap_from = request.form.get("swapFrom")
    swap_to = request.form.get("swapTo")
    if "." not in swap_from or "." not in swap_to:
        return render_template('menu.html', swap_output_colour="red", swap_output_message=f"command execution failed with params {swap_from}, {swap_to}")
    swap_file_extensions(selected_directory,swap_from,swap_to)
    return render_template('menu.html', swap_output_colour="white", swap_output_message=f"command executed with params {swap_from}, {swap_to}")

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
