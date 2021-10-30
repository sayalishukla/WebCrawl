from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys

class crwl:
    def __init__(self):
        self.url = []
        self.base_url = "http://commoncrawl.s3.amazonaws.com/"
        self.filenm = "/Users/sayali/Documents/Python/commoncrwl/warc.paths"
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
        matching_entries = 0
        hits = 0

        # file_name = "http://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-30/segments/1563195523840.34/warc/CC-MAIN-20190715175205-20190715200159-00000.warc.gz"
        #file_name_list = "http://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-24/warc.paths.gz"

        if len(sys.argv) > 1:
            file_name = sys.argv[1]

        stream = None
        if file_name.startswith("http://") or file_name.startswith(
                "https://"
        ):
            stream = requests.get(file_name, stream=True).raw
        else:
            stream = open(file_name, "rb")
        print("got stream")
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

c = crwl()
c.read_urls()
print(c.result)