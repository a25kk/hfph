import sys
import traceback

class ArcheCSVBase:

    def formatExceptionInfo(self, maxTBlevel=5):
        # Code taken from http://www.linuxjournal.com/article/5821
        cla, exc, trbk = sys.exc_info()
        
        if str(cla):
            excName = str(cla)
        else:
            excName = "no exception name"
        try:
            excName = cla.__name__
        except:
            pass

        excArgs = ()
        try:
            excArgs = exc.__dict__.get("args")
        except:
            pass
            
        excTb = ("no traceback",)
        try:          
            excTb = traceback.format_tb(trbk, maxTBlevel)
        except:
            pass
        return (excName, excArgs, excTb)

    def HTMLFormatExceptionInfo(self, maxTBlevel=5):
        excName, excArgs, excTb = self.formatExceptionInfo(maxTBlevel=5)
        html = "<br />"
        html += "<strong>"
        html += excName
        html += "</strong>"
        html += "<br />"
        try:
            for a in excArgs:
                if a.strip():
                    html += "&nbsp;"
                    html += "<strong>"
                    html += a
                    html += "</strong>"
                    html += "<br />"
        except:
                    html += "&nbsp;"
                    html += "<strong>"
                    html += str(excArgs)
                    html += "</strong>"
                    html += "<br />"
            
        html += "<code>"
        try:
            for t in excTb:
                if t.strip():
                    html += "&nbsp;"
                    html += t
                    html += "<br />"
        except:
            html += "&nbsp;"
            html += str(excTb)
            html += "<br />"
        html += "</code>"
            
        return html

