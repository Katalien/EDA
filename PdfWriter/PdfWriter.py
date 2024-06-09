from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

class PdfWriter:
    @staticmethod
    def writePdf(plots, filename="report2.pdf"):
        with PdfPages(filename) as pdf:
            for plot in plots:
                pdf.savefig(plot)
                plt.close()