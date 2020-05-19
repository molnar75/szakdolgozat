class Region(object):
    """
    Region of Interest (ROI)
    """
    
    def __init__(self, row, column, n_rows, n_columns):
        """
        Initialize the region.
        """
        self._row = row
        self._column = column
        self._n_rows = n_rows
        self._n_columns = n_columns

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def n_rows(self):
        return self._n_rows

    @property
    def n_columns(self):
        return self._n_columns

    def __str__(self):
        return f'Region at ({self._row}, {self._column}) with size ({self._n_rows}, {self._n_columns})'
