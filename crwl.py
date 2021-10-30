from warcio.archiveiterator import ArchiveIterator
import re
import os
import requests
import sys


class crwl:
    def __init__(self):
        self.url = []
        self.base_url = "http://commoncrawl.s3.amazonaws.com/"
        self.filenm = os.path.join(os.path.dirname(os.path.basename(__file__)),"warc.paths")
        self.result = []

    def read_urls(self):
        # read paths
        with open(self.filenm, "r") as f:
            for line in f:
                url = self.base_url + line.strip()
                self.process_url(url)

    def process_url(self,file_name):

        print(f"current file name {file_name}")

        regex = re.compile(
            '(covid19|covid-19|coronavirus|Covid19|Covid-19|Coronavirus|COVID19)'
        )
        regex1 = re.compile(
            '(economics|finance|business|Economics|Finance|Business|stockmarket|stock|wall street|economic|economy)'
        )


        entries = 0
        hits = 0

        if len(sys.argv) > 1:
            file_name = sys.argv[1]

        stream = None
        if file_name.startswith("http://") or file_name.startswith(
                "https://"
        ):
            stream = requests.get(file_name, stream=True).raw
        else:
            stream = open(file_name, "rb")

        for record in ArchiveIterator(stream):
            if record.rec_type == "warcinfo":
                continue

            if not ".com/" in record.rec_headers.get_header(
                    "WARC-Target-URI"
            ):
                continue

            entries = entries + 1
            contents = (
                record.content_stream()
                    .read()
                    .decode("utf-8", "replace")
            )

            m = regex.search(contents)
            if m:
                m1 = regex1.search(contents)
                hits = hits + 1
                if m1:
                    self.result.append(record.rec_headers.get_header("WARC-Target-URI"))
                if len(self.result)> 1000:
                    break

if __name__ == "__main__":
    c = crwl()
    c.read_urls()
    print(c.result)