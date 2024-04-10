import pdfminer
from PyPDF2 import PdfFileReader, pdf
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from amspApp.FileServer.views.FileUploadView import FileUploadViewSet
from amspApp.QC.models import QCDocumentsDetails, QCDocumentsOulines


class pdfPositionHandling:
    indexT = -6
    filename = ""

    def parse_obj(self, qcDoc, lt_objs, indexOf, pageid):

        # loop over the object list
        for obj in lt_objs:

            if isinstance(obj, pdfminer.layout.LTTextLine):
                # print("width:     %6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))
                newPath = ""
                if self.indexT != indexOf:
                    tmpPath = FileUploadViewSet().convertWithIndex(qcDoc.fileAddr, indexOf)
                    newPath = FileUploadViewSet().saveImgToDB(-1, qcDoc.title, tmpPath)
                    self.indexT = indexOf
                    self.filename = newPath


                dt = {
                    "positionID": qcDoc.positionID,
                    "companyID": qcDoc.companyID,
                    "QCDocumentLink": qcDoc.id,
                    "dateOfPost": qcDoc.dateOfPost,
                    "pageIndex": indexOf,
                    "pageID": pageid,
                    "width": obj.width,
                    "height": obj.height,
                    "word_margin": obj.word_margin,
                    "x0": obj.x0,
                    "y0": obj.y0,
                    "x1": obj.x1,
                    "y1": obj.y1,
                    "fileAddr": self.filename,
                    "word": obj.get_text().replace('\n', '...'),
                }

                QCDD = QCDocumentsDetails(
                    **dt
                )
                QCDD.save()

                # path = os.path.join(STATIC_ROOT, 'manuals', qcDoc.title.replace(" ", "_").replace(".", "_"))
                # os.makedirs(path, exist_ok=True)
                # filepath_org = os.path.join(path, "org_"+str(indexOf) + ".jpg")
                # filepath = os.path.join(path, str(indexOf) + ".jpg")
                # copyfile(fuv, filepath_org)

                # with Image(filename=filepath_org) as background:
                #     with Image(filename='d:/water.jpg') as watermark:
                #         background.watermark(image=watermark, transparency=0.75)
                #     background.save(filename=filepath)
                #




                print("pageIndex:%d pageID:%d width:%d height:%d word_margin:%d x0:%d y0:%d x1:%d y1:%d     %s" %
                      (
                          indexOf, pageid, obj.width, obj.height, obj.width,
                          obj.x0, obj.y0, obj.x1, obj.y1,
                          obj.get_text().replace('\n', '_'),))

            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(qcDoc, obj._objs, indexOf, pageid)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(qcDoc, obj._objs, indexOf, pageid)

    def parsepdf(self, qcDoc, filename, startpage, endpage):

        # Open a PDF file.
        fp = open(filename, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        i = 0
        # loop over all pages in the document
        indexOf = 0
        for page in PDFPage.create_pages(document):
            if i >= startpage and i <= endpage:
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()

                # extract text from this object
                self.parse_obj(qcDoc, layout._objs, indexOf, page.pageid)
                indexOf += 1
            i += 1

    def _setup_page_id_to_num(self, pdf, pages=None, _result=None, _num_pages=None):
        if _result is None:
            _result = {}
        if pages is None:
            _num_pages = []
            pages = pdf.trailer["/Root"].getObject()["/Pages"].getObject()
        t = pages["/Type"]
        if t == "/Pages":
            for page in pages["/Kids"]:
                _result[page.idnum] = len(_num_pages)
                self._setup_page_id_to_num(pdf, page.getObject(), _result, _num_pages)
        elif t == "/Page":
            _num_pages.append(1)
        return _result

    def outlines_pg_zoom_info(self, outlines, pg_id_num_map, result=None):
        if result is None:
            result = dict()
        if type(outlines) == list:
            for outline in outlines:
                result = self.outlines_pg_zoom_info(outline, pg_id_num_map, result)
        elif type(outlines) == pdf.Destination:
            title = outlines['/Title']
            result[title.split()[0]] = dict(title=outlines['/Title'],
                                            top=outlines['/Top'],
                                            pageid=outlines.page.idnum,
                                            left=outlines['/Left'], page=(pg_id_num_map[outlines.page.idnum] + 1))
        return result

    def getBookmarks(self, qcDoc, fileaddr):
        # main
        pdf_name = fileaddr
        f = open(pdf_name, 'rb')
        pdf = PdfFileReader(f)
        # map page ids to page numbers
        pg_id_num_map = self._setup_page_id_to_num(pdf)
        outlines = pdf.getOutlines()
        bookmarks_info = self.outlines_pg_zoom_info(outlines, pg_id_num_map)
        lst = list(bookmarks_info.keys())
        list(map(str, lst)).sort()
        for l in lst:
            current = bookmarks_info[l]
            dt = dict(
                positionID=qcDoc.positionID,
                companyID=qcDoc.companyID,
                QCDocumentLink=qcDoc.id,
                title=l,
                desc=current["title"],
                left=current["left"],
                page=current["page"],
                pageid=current["pageid"],
                top=int(current["top"]),
            )

            cc = QCDocumentsOulines(**dt)
            cc.save()
            print(l)

        return bookmarks_info
