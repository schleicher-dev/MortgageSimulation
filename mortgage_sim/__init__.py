import numpy as np
import pandas as pd
import re
import typing as ty


from babel.numbers import format_currency
from decimal import Decimal
from enum import Flag
from IPython.core.display import HTML


class ReferenceDisplayMode(Flag):
    NONE = 0
    MONTHLY = 2 ** 0
    ANNUAL = 2 ** 1
    TOTAL = 2 ** 2
    FULL = MONTHLY | ANNUAL | TOTAL


def display_payment_plan(payment_plan: pd.DataFrame, reference_payment_plan: ty.Optional[pd.DataFrame] = None, reference_display_mode: ty.Optional[ReferenceDisplayMode] = None):
    exclude = {'Date', 'Month', 'Delta', 'Wallet', 'Mortgage Sum', '.* Amount'}
    highlight = {'.* Unscheduled'}
    reference_display_mode = (reference_display_mode or ReferenceDisplayMode.FULL) if reference_payment_plan is not None else ReferenceDisplayMode.NONE
    columns = payment_plan.columns if reference_payment_plan is None or len(payment_plan.columns) <= len(reference_payment_plan.columns) else reference_payment_plan.columns
    
    def _format_value(value: ty.Any) -> str:
        if isinstance(value, Decimal):
            return format_currency(value, 'EUR', locale='de_DE') if value != Decimal(0) else "&#8212;"
        return str(value)
    
    def write_header(_markup: str):
        _cell_style = "background-color: #00B6B2; color: #FFF; font-weight: 700;"
        _markup + '= <tr>'
        _markup += f'<th style="{_cell_style}" />'
        for column in columns:
            _markup += f'<th style="{_cell_style}">{column}</th>'
        _markup += "</tr>"
        return _markup
    
    
    markup = ''
        
    for row_index in range(payment_plan.shape[0]):      
        if payment_plan['Date'][row_index].month == 1 or row_index == 0:
            markup = write_header(markup)
          
        # Show row
        _cell_style = 'background-color: #FFF;'
        _normal_style = _cell_style + 'color: #000;'
        _highlight_style = _cell_style + 'color: #018A8D;'
        _reference_style = _cell_style + 'color: #666;'
        
        markup += f'<tr><td style="{_normal_style}" />'
        for column in columns:
            value = payment_plan[column][row_index]
            
            style = _normal_style
            if any(re.match(h, column) is not None for h in highlight) and value > Decimal(0):
                style = _highlight_style
            elif column == 'Wallet' and payment_plan['Mortgage Sum'][row_index] < value:
                style = _highlight_style
            markup += f'<td style="{style}">{_format_value(value)}</td>'
        markup += "</tr>"
        
        if reference_display_mode & ReferenceDisplayMode.MONTHLY == ReferenceDisplayMode.MONTHLY:
            # Reference
            markup += f'<tr><td style="{_reference_style}">Reference:</td>'
            for column in columns:
                value = reference_payment_plan[column][row_index]
                
                markup += f'<td style="{_reference_style}">{_format_value(value)}</td>'
            markup += "</tr>"
        
        # Create annual summary
        if payment_plan['Date'][row_index].month == 12 or row_index == payment_plan.shape[0] - 1:
            markup += "<tr style=\"background-color: #FF9658; color: #000\">"
            markup += "<th>Annual Summary</th>"
            for column in columns:
                start_row_index = max(0, row_index - 12 + 1)
                value = np.sum(payment_plan[column][start_row_index:row_index + 1]) if all(re.match(ex, column) is None for ex in exclude) else None
                formatted_value = _format_value(value) if value is not None else "&#8212;"
                markup += f"<th style=\"font-weight: 600\">{formatted_value}</th>"
            markup += "</tr>"
            
            if reference_display_mode & ReferenceDisplayMode.ANNUAL == ReferenceDisplayMode.ANNUAL:
                markup += "<tr style=\"background-color: #F1F1F1; color: #999\">"
                markup += "<th>Reference Annual Summary</th>"
                for column in columns:
                    start_row_index = max(0, row_index - 12 + 1)
                    value = np.sum(reference_payment_plan[column][start_row_index:row_index + 1]) if all(re.match(ex, column) is None for ex in exclude) else None
                    formatted_value = _format_value(value) if value is not None else "&#8212;"
                    markup += f"<th style=\"font-weight: 600\">{formatted_value}</th>"
                markup += "</tr>"     
            
                markup += "<tr style=\"background-color: #F1F1F1; color: #999\">"
                markup += "<th>Δ Annual Summary</th>"
                for column in columns:
                    start_row_index = max(0, row_index - 12 + 1)
                    value = np.sum(payment_plan[column][start_row_index:row_index + 1]) if all(re.match(ex, column) is None for ex in exclude) else None
                    ref_value = np.sum(reference_payment_plan[column][start_row_index:row_index + 1]) if all(re.match(ex, column) is None for ex in exclude) else None
                    formatted_value = _format_value(value - ref_value) if value is not None and ref_value is not None else "&#8212;"
                    markup += f"<th style=\"font-weight: 600\">{formatted_value}</th>"
                markup += "</tr>"            
    
    # Create grand summary
    markup += "<tr style=\"background-color: #FD5A19; color: #000;\">"
    markup += "<th><b>Grand Summary</b></th>"
    for column in columns:
        if any(re.match(ex, column) is not None for ex in exclude):
            formatted_value = "&#8212;"
        else:
            formatted_value = _format_value(np.sum(payment_plan[column]))
        markup += "<th style=\"font-weight: 600\">" + formatted_value + "</th>"
    markup += "</tr>"
    
    if reference_display_mode & ReferenceDisplayMode.TOTAL == ReferenceDisplayMode.TOTAL:
        markup += "<tr style=\"background-color: #FFF; color: #000\">"
        markup += "<th>Reference Grand Summary</th>"
        for column in columns:
            if any(re.match(ex, column) is not None for ex in exclude):
                formatted_value = "&#8212;"
            else:
                formatted_value = _format_value(np.sum(reference_payment_plan[column]))
            markup += "<th style=\"font-weight: 600\">" + formatted_value + "</th>"
        markup += "</tr>"
        
        markup += "<tr style=\"background-color: #FFF; color: #000\">"
        markup += "<th>Δ Grand Summary</th>"
        for column in columns:
            if any(re.match(ex, column) is not None for ex in exclude):
                formatted_value = "&#8212;"
            else:
                formatted_value = _format_value(np.sum(payment_plan[column]) - np.sum(reference_payment_plan[column]))
            markup += "<th style=\"font-weight: 600\">" + formatted_value + "</th>"
        markup += "</tr>"
    
    display(HTML("<table>" + markup + "</table>"))
