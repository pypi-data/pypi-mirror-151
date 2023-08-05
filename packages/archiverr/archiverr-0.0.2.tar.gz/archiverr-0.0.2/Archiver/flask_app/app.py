from curses import reset_shell_mode
import os, sys
from flask import Flask, render_template, request

sys.path.insert(1, os.path.abspath('.'))
from Archiver.Archive import Archive
from Archiver.Utilities import Utilities
import Archiver.Constants  as Constants
from Archiver import myConfig
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    resources = []
    if request.method == 'POST':
        filters = dict()
        Utilities.checkCurrentArchive()
        search = request.form['search']
        if search != "":
            filters = dict(x.split(':') for x in search.split(' ')) 
                            
        myArchive = Archive(myConfig.getOption(Constants.NAME_OF_SECTION_ARCHIVE, Constants.NAME_OF_CURRENT_ARCHIVE_NAME))
        resources = myArchive.search(filters)
        myArchive.saveToExtract(resources)
    return render_template('search.html', resources=resources)
