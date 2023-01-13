# -*- coding: utf-8 -*-

import os
import subprocess

from albert import *

__doc__ = """
Find files with fd
Synopsis: `<trigger> <expression>`
"""

md_iid = "0.5"
md_version = "0.1"
md_name = "Find Files"
md_description = "Find files with fd"
md_license = "MIT"
md_url = "https://github.com/hankliao87/albert-fd"
md_maintainers = "@hankliao87"
md_bin_dependencies = ["fd"]

trigger = "f "

SEARCH_LIMIT = 20


class Plugin(QueryHandler):
    iconPath = ["xdg:preferences-system-search", "xdg:system-search", "xdg:search", "xdg:text-x-generic"]

    def id(self):
        return __name__

    def name(self):
        return md_name

    def description(self):
        return md_description

    def synopsis(self) -> str:
        return "<name>"

    def defaultTrigger(self) -> str:
        return trigger

    def handleQuery(self, query):

        query_string = query.string.strip()

        if len(query_string) < 1:
            item = Item(id=__name__, icon=self.iconPath)
            item.text = "Enter more than one characters to search"
            item.subtext = ""
            query.add(item)
        else:
            try:
                proc_result = subprocess.run(['fd', '-L', query_string, '--max-results', str(SEARCH_LIMIT), '/home'], stdout=subprocess.PIPE, text=True, timeout=10)

                results = proc_result.stdout
                results = results.splitlines()
                if len(results) == 0:
                    item = Item(id=__name__, icon=self.iconPath)
                    item.text = "Not Found"
                    item.subtext = query_string
                    query.add(item)
                    return

                for result in results:
                    result = result[:-1] if result.endswith('/') else result
                    item = Item(
                        id=__name__,
                        text=os.path.basename(result),
                        subtext=result,
                        icon=self.iconPath,
                        actions=[
                            Action(
                                id="open",
                                text="Open",
                                callable=lambda u=f"file://{result}": openUrl(u)),
                        ],
                    )
                    query.add(item)

            except subprocess.TimeoutExpired as ex:
                item = Item(id=__name__, icon=self.iconPath)
                item.text = "Timeout"
                item.subtext = "Error: " + str(ex)
                query.add(item)

            except Exception as ex:
                item = Item(
                    id=__name__,
                    icon=self.iconPath,
                    actions=[
                        Action(
                            id="copy-clipboard",
                            text="Copy error message to clipboard",
                            callable=lambda u=str(ex): setClipboardText(u)),
                        Action(
                            id="copy-repo-url",
                            text="Copy repo url to clipboard",
                            callable=lambda: setClipboardText(md_url)),
                    ]
                )
                item.text = "Error: " + str(ex)
                item.subtext = f"Please create an issue in {md_url}"
                query.add(item)

