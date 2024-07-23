# -*- coding: utf-8 -*-

import os
import subprocess

from albert import *

md_iid = "2.3"
md_version = "0.2"
md_name = "Find Files"
md_description = "Find files with fd"
md_license = "MIT"
md_url = "https://github.com/hankhjliao/albert-fd"
md_authors = "@hankhjliao"
md_bin_dependencies = ["fd"]

trigger = "f "
SEARCH_LIMIT = 20


class Plugin(PluginInstance, TriggerQueryHandler):
    iconPath = ["xdg:preferences-system-search", "xdg:system-search", "xdg:search", "xdg:text-x-generic"]

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
            self,
            self.id,
            self.name,
            self.description,
            synopsis="<name>",
            defaultTrigger=trigger,
        )

    def handleTriggerQuery(self, query):
        query_string = query.string.strip()

        if len(query_string) <= 0:
            item = StandardItem(
                id=__name__,
                text="Enter more than one characters to search",
                subtext="",
                iconUrls=self.iconPath,
            )
            query.add(item)
            return

        try:
            proc_result = subprocess.run(
                ["fd", "-L", query_string, "--max-results", str(SEARCH_LIMIT), "/home"],
                stdout=subprocess.PIPE,
                text=True,
                timeout=10,
            )

            results = proc_result.stdout
            results = results.splitlines()

            if len(results) == 0:
                item = StandardItem(
                    id=__name__,
                    text="Not Found",
                    subtext=query_string,
                    icon=self.iconPath,
                )
                query.add(item)
                return

            for result in results:
                result = result[:-1] if result.endswith("/") else result
                item = StandardItem(
                    id=__name__,
                    text=os.path.basename(result),
                    subtext=result,
                    iconUrls=self.iconPath,
                    actions=[
                        Action(id="open", text="Open", callable=lambda u=f"file://{result}": openUrl(u)),
                    ],
                )
                query.add(item)

        except subprocess.TimeoutExpired as ex:
            item = StandardItem(
                id=__name__,
                text="Timeout",
                subtext="Error: " + str(ex),
                iconUrls=self.iconPath,
            )
            query.add(item)

        except Exception as ex:
            item = StandardItem(
                id=__name__,
                iconUrls=self.iconPath,
                text="Error: " + str(ex),
                subtext=f"Please create an issue in {md_url}",
                actions=[
                    Action(id="copy-clipboard", text="Copy error message to clipboard", callable=lambda u=str(ex): setClipboardText(u)),
                    Action(id="copy-repo-url", text="Copy repo url to clipboard", callable=lambda: setClipboardText(md_url)),
                ],
            )
            query.add(item)
