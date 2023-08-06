from PyQt5 import QtWidgets

from boxjelly.ui.MediaSelectionBox import MediaSelectionBox
from boxjelly.ui.TrackSelectionBox import TrackSelectionBox


class DataSelectionBox(QtWidgets.QGroupBox):
    """Data selection group box"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Set the title
        self.setTitle('Data')
        
        # Create the selection boxes
        self.media_selection_box = MediaSelectionBox()
        self.track_selection_box = TrackSelectionBox()
        
        self.arrange()

    def arrange(self):
        """Arrange the data form"""
        # Set form layout
        self.setLayout(QtWidgets.QVBoxLayout())
        
        # Arrange the selection boxes
        self.layout().addWidget(self.media_selection_box)
        self.layout().addWidget(self.track_selection_box)

    @property
    def media_content(self):
        return self.media_selection_box.media_content
    
    @property
    def track_io(self):
        return self.track_selection_box.io
