from pathlib import Path
from typing import Any

from openpyxl import load_workbook

class TemplateAnalyzer:
    
    def analyze_workbook(
        self,
        file_path: str,
    ) -> dict[str, Any]:
        
        path = Path(file_path)
        
        workbook = load_workbook(
            path,
            data_only=False,
        )
        
        sheets = []
        
        for worksheet in workbook.worksheets:
            
            cells = []
            
            for row in worksheet.iter_rows():
                for cell in row:
                    
                    cells.append({
                        "coordinate": cell.coordinate,
                        "value": cell.value,
                        "data_type": cell.data_type,
                        "number_format": cell.number_format, 
                    })
                    
            sheets.append({
                "name": worksheet.title,
                "max_row": worksheet.max_row,
                "max_column": worksheet.max_column,
                "merged_cells": [
                    str(cell_range)
                    for cell_range
                    in worksheet.merged_cells.ranges
                ],
                "cells": cells,
            })
            
        return {
            "file_name": path.name,
            "sheets": sheets,
        }