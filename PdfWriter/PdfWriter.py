from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

class PdfWriter:
    @staticmethod
    def writePdf(plots, path, filename="report.pdf"):
        filepath = path + filename
        with PdfPages(filepath) as pdf:
            for plot in plots:
                pdf.savefig(plot)
                plt.close()