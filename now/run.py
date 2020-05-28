import sys
import os
import PyQt5.QtWidgets as QtWidgets
d = os.path.dirname(__file__)
print(d)
sys.path.append(d)
from codes.gui import neo4j



qapp = QtWidgets.QApplication(sys.argv)
app = neo4j.neo4j()
app.show()
sys.exit(qapp.exec_())