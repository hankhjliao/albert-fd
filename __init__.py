# -*- coding: utf-8 -*-
"""Find files with fd
Synopsis: <trigger> <expression>"""

import os
import subprocess

from albert import *

__title__ = "Find file with fd"
__version__ = "0.4.0"
__triggers__ = "f "
__authors__ = ["hankliao87"]
__exec_deps__ = ["fd"]

SEARCH_LIMIT = 20

iconPath = iconLookup(["preferences-system-search", "system-search" "search", "text-x-generic"])

def handleQuery(query):
    if query.isTriggered:
        query_string = query.string.strip()

        if len(query_string) < 3:
            item = Item(id=__title__, icon=iconPath)
            item.text = "Enter more than three characters to search"
            item.subtext = ""
            return item
        else:
            try:
                proc_result = subprocess.run(['fd', '-L', query_string, '--max-results', str(SEARCH_LIMIT), '/home'], stdout=subprocess.PIPE, text=True, timeout=10)

                results = proc_result.stdout
                results = results.splitlines()
            except subprocess.TimeoutExpired as ex:
                item = Item(id=__title__, icon=iconPath)
                item.text = "Timeout"
                item.subtext = "Error: " + str(ex)
                return item
            except Exception as ex:
                item = Item(id=__title__, icon=iconPath)
                item.text = "Error: " + str(ex)
                item.subtext = "Please create an issue in https://github.com/hankliao87/albert-fd"
                item.addAction(ClipAction(text="Copy error message to clipboard", clipboardText=str(ex)))
                item.addAction(ClipAction(text="Copy repo url to clipboard", clipboardText="https://github.com/hankliao87/albert-fd"))
                return item

            if len(results) == 0:
                item = Item(id=__title__, icon=iconPath)
                item.text = "Not Found"
                item.subtext = query_string
                return item

            items = []
            for result in results:
                item = Item(id=__title__, icon=iconPath)
                result = result[:-1] if result.endswith('/') else result
                item.text = os.path.basename(result)
                item.subtext = result
                item.addAction(UrlAction("Open", "file://%s" % result))
                #item.addAction(ProcAction(text="Open", commandline=["xdg-open", result]))
                items.append(item)
            return items
