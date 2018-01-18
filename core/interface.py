# -*- coding: utf-8 -*-
import sys
import re
import math
import sys
import textwrap
from functools import reduce


def len(iterable):
    if not isinstance(iterable, str):
        return iterable.__len__()
    try:
        return len(str(iterable, 'utf'))
    except:
        return iterable.__len__()


class ArraySizeError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg, '')

    def __str__(self):
        return self.msg


class ColorTemplates:
    PURPLE = '\x1b[95m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    ENDC = '\x1b[0m'
    WHITE = ''
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


def get_string_color(type, string):
    end = ColorTemplates.ENDC
    if type == ColorTemplates.WHITE:
        end = ''
    return '%s%s%s' % (type, string, end)


class ASCIITable:

    BORDER = 1
    HEADER = 1 << 1
    HLINES = 1 << 2
    VLINES = 1 << 3

    def __init__(self, max_width=80):
        if max_width <= 0:
            max_width = False
        self._maxWidth = max_width
        self._precision = 3
        self._decoration = ASCIITable.VLINES | \
                           ASCIITable.HLINES | \
                           ASCIITable.BORDER | \
                           ASCIITable.HEADER
        self.set_characters(['-', '|', '+', '='])
        self.reset()

    def reset(self):
        self._horizontal_line_string = None
        self._row_size = None
        self._header = []
        self._rows = []

    def set_characters(self, array):
        """
        [horizontal, vertical, corner, header]
        default is set to: ['-', '|', '+', '=']
        """
        if len(array) != 4:
            raise ArraySizeError("Array should contain 4 characters.")
        array = [x[:1] for x in [str(s) for s in array]]
        (self._horizontalCharacter,
         self._verticalCharacter,
         self._cornerCharacter,
         self._headerCharacter) = array

    def set_table_decoration(self, deco):
        """
        -deco:
        Texttable.BORDER: Border around the table
        Texttable.HEADER: Horizontal line below the header
        Texttable.HLINES: Horizontal lines between rows
        Texttable.VLINES: Vertical lines between columns
        - example:
        Texttable.BORDER | Texttable.HEADER
        """

        self._decoration = deco

    def set_column_alignment(self, array):
        """
        -array: should be either "l", "c" or "r":
        * "l": column flushed left
        * "c": column centered
        * "r": column flushed right
        """
        self._check_row_size(array)
        self._align = array

    def set_column_vertical_alignment(self, array):
        """
        -array should be either "t", "m" or "b":
        * "t": column aligned on the top of the cell
        * "m": column aligned on the middle of the cell
        * "b": column aligned on the bottom of the cell
        """
        self._check_row_size(array)
        self._verticalAlignment = array

    def set_columns_data_type(self, array):
        """
        -array should be either "a", "t", "f", "e" or "i":
        * "a": automatic (try to use the most appropriate datatype)
        * "t": treat as text
        * "f": treat as float in decimal format
        * "e": treat as float in exponential format
        * "i": treat as int
        """
        self._check_row_size(array)
        self._dataType = array

    def set_columns_width(self, array):
        """S
        -array should be integers, specifying the
        -example: [10, 20, 5]
        """
        self._check_row_size(array)
        try:
            array = list(map(int, array))
            if reduce(min, array) <= 0:
                raise ValueError
        except ValueError:
            sys.stderr.write("Wrong argument in column width specification\n")
            raise
        self._width = array

    def set_precision(self, width):
        """
            - width must be an integer >= 0
            - default value: 3
        """
        if not type(width) is int or width < 0:
            raise ValueError('width must be an integer greater then 0')
        self._precision = width

    def header(self, array):
        self._check_row_size(array)
        self._header = list(map(str, array))

    def addRow(self, array):
        self._check_row_size(array)
        if not hasattr(self, "_dtype"):
            self._dataType = ["a"] * self._row_size
        cells = []
        for i,x in enumerate(array):
            cells.append(self._str(i,x))
        self._rows.append(cells)

    def addRows(self, rows, header=True):
        """
            -rows: iterator returning arrays or a by-dimensional array
            -header: specifies if the first row should be used as the header of the table
        """
        if header:
            if hasattr(rows, '__iter__') and hasattr(rows, 'next'):
                self.header(next(rows))
            else:
                self.header(rows[0])
                rows = rows[1:]
        for row in rows:
            self.addRow(row)

    def draw(self):
        if not self._header and not self._rows:
            return
        self._computeColumnsWidth()
        self._checkAlignment()
        out = ""
        if self._hasBorder():
            out += self._horizontalLine()
        if self._header:
            out += self._drawLine(self._header, isheader=True)
            if self._hasHeader():
                out += self._horizontalLineHeader()
        length = 0
        for row in self._rows:
            length += 1
            out += self._drawLine(row)
            if self._hasHorizontalLines() and length < len(self._rows):
                out += self._horizontalLine()
        if self._hasBorder():
            out += self._horizontalLine()
        return out[:-1]

    def _str(self, i, x):
        """
            -i: index of the cell datatype in self._dtype
            -x: cell data to format
        """
        try:
            f = float(x)
            n = str(f)
            if n == "nan" or n=="inf" or n=="-inf" :
                raise ValueError('Infinity or NaN considered as string')
        except:
            if type(x) is str:
                return x
            else:
                if x is None:
                    return str(x)
                else:
                    return str(x.encode('utf-8'))

        n = self._precision
        dtype = self._dataType[i]

        if dtype == 'i':
            return str(int(round(f)))
        elif dtype == 'f':
            return '%.*f' % (n, f)
        elif dtype == 'e':
            return '%.*e' % (n, f)
        elif dtype == 't':
            if type(x) is str:
                return x
            else:
                if x is None:
                    return str(x)
                else:
                    return str(x.encode('utf-8'))
        else:
            if f - round(f) == 0:
                if abs(f) > 1e8:
                    return '%.*e' % (n, f)
                else:
                    return str(int(round(f)))
            else:
                if abs(f) > 1e8:
                    return '%.*e' % (n, f)
                else:
                    return '%.*f' % (n, f)

    def _check_row_size(self, array):
        if not self._row_size:
            self._row_size = len(array)
        elif self._row_size != len(array):
            raise ArraySizeError(
                "array should contain %d elements" % self._row_size)

    def _hasVerticalLines(self):
        return self._decoration & ASCIITable.VLINES > 0

    def _hasHorizontalLines(self):
        return self._decoration & ASCIITable.HLINES > 0

    def _hasBorder(self):
        return self._decoration & ASCIITable.BORDER > 0

    def _hasHeader(self):
        return self._decoration & ASCIITable.HEADER > 0

    def _horizontalLineHeader(self):
        return self._buildHorizontalLine(True)

    def _horizontalLine(self):
        if not self._horizontal_line_string:
            self._horizontal_line_string = self._buildHorizontalLine()
        return self._horizontal_line_string

    def _buildHorizontalLine(self, is_header=False):
        horiz = self._horizontalCharacter
        if (is_header):
            horiz = self._headerCharacter
        s = "%s%s%s" % (horiz, [horiz, self._cornerCharacter][self._hasVerticalLines()],
                        horiz)
        l = s.join([horiz * n for n in self._width])
        if self._hasBorder():
            l = "%s%s%s%s%s\n" % (self._cornerCharacter, horiz, l, horiz,
                                  self._cornerCharacter)
        else:
            l += "\n"
        return l

    def _widthOfCell(self, cell):
        cell = re.compile(r'\x1b[^m]*m').sub('', cell)
        cellLines = cell.split('\n')
        maxi = 0
        for line in cellLines:
            length = 0
            parts = line.split('\t')
            for part, i in zip(parts, list(range(1, len(parts) + 1))):
                length = length + len(part)
                if i < len(parts):
                    length = (length//8 + 1) * 8
            maxi = max(maxi, length)
        return maxi

    def _computeColumnsWidth(self):
        if hasattr(self, "_width"):
            return
        maxi = []
        if self._header:
            maxi = [self._widthOfCell(x) for x in self._header]
        for row in self._rows:
            for cell, i in zip(row, list(range(len(row)))):
                try:
                    maxi[i] = max(maxi[i], self._widthOfCell(cell))
                except (TypeError, IndexError):
                    maxi.append(self._widthOfCell(cell))
        items = len(maxi)
        length = reduce(lambda x,y: x+y, maxi)
        if self._maxWidth and length + items * 3 + 1 > self._maxWidth:
            max_lengths = maxi
            maxi = [(self._maxWidth - items * 3 - 1) // items for n in range(items)]
            free = 0
            oversized = 0

            for col, max_len in enumerate(max_lengths):
                current_length = maxi[col]
                if current_length > max_len:
                    free += current_length - max_len
                    maxi[col] = max_len
                elif max_len > current_length:
                    oversized += 1

            while free > 0:
                freePart = int(math.ceil(float(free) / float(oversized)))

                for col, max_len in enumerate(max_lengths):
                    current_length = maxi[col]
                    if current_length < max_len:
                        needed = max_len - current_length
                        if needed <= freePart:
                            maxi[col] = max_len
                            free -= needed
                            oversized -= 1
                        else:
                            maxi[col] = maxi[col] + freePart
                            free -= freePart
        self._width = maxi

    def _checkAlignment(self):
        if not hasattr(self, "_align"):
            self._align = ["l"] * self._row_size
        if not hasattr(self, "_valign"):
            self._verticalAlignment = ["t"] * self._row_size

    def _drawLine(self, line, isheader=False):
        line = self._splitEachElementOfLine(line, isheader)
        space = " "
        out  = ""
        for i in range(len(line[0])):
            if self._hasBorder():
                out += "%s " % self._verticalCharacter
            length = 0
            for cell, width, align in zip(line, self._width, self._align):
                length += 1
                cell_line = cell[i]

                fill = width - len(re.compile(r'\x1b[^m]*m').sub('', cell_line))
                if isheader:
                    align = "c"
                if align == "r":
                    out += "%s " % (fill * space + cell_line)
                elif align == "c":
                    out += "%s " % (fill//2 * space + cell_line + (fill//2 + fill%2) * space)
                else:
                    out += "%s " % (cell_line + fill * space)
                if length < len(line):
                    out += "%s " % [space, self._verticalCharacter][self._hasVerticalLines()]
            out += "%s\n" % ['', self._verticalCharacter][self._hasBorder()]
        return out

    def _splitEachElementOfLine(self, line, isheader):
        line_wrapped = []
        for cell, width in zip(line, self._width):
            array = []
            ANSIKeep = []
            for c in cell.split('\n'):
                c = "".join(ANSIKeep) + c
                ANSIKeep = []
                extraWidth = 0
                for a in re.findall(r'\x1b[^m]*m', c):
                    extraWidth += len(a)
                    if a == '\x1b[0m':
                        if len(ANSIKeep) > 0:
                            ANSIKeep.pop()
                    else:
                        ANSIKeep.append(a)
                c = c + '\x1b[0m' * len(ANSIKeep)
                extraWidth += len('\x1b[0m' * len(ANSIKeep))
                if type(c) is not str:
                    try:
                        c = str(c, 'utf')
                    except UnicodeDecodeError as strerror:
                        sys.stderr.write("UnicodeDecodeError exception for string '%s': %s\n" % (c, strerror))
                        c = str(c, 'utf', 'replace')
                array.extend(textwrap.wrap(c, width + extraWidth))
            line_wrapped.append(array)
        max_cell_lines = reduce(max, list(map(len, line_wrapped)))
        for cell, valign in zip(line_wrapped, self._verticalAlignment):
            if isheader:
                valign = "t"
            if valign == "m":
                missing = max_cell_lines - len(cell)
                cell[:0] = [""] * (missing // 2)
                cell.extend([""] * (missing // 2 + missing % 2))
            elif valign == "b":
                cell[:0] = [""] * (max_cell_lines - len(cell))
            else:
                cell.extend([""] * (max_cell_lines - len(cell)))
        return line_wrapped

def printLogo():
    import colorama
    print('\n')
    print('+----------------------------------------------------------------------------------------+')
    text = """
                 #####                       ######                             
                #     # #    # #####  ###### #     #   ##   #####  ####  #    # 
                #       #    # #    # #      #     #  #  #    #   #    # #    # 
                 #####  #    # #    # #####  ######  #    #   #   #      ###### 
                      # #    # #####  #      #       ######   #   #      #    # 
                #     # #    # #   #  #      #       #    #   #   #    # #    # 
                 #####   ####  #    # ###### #       #    #   #    ####  #    # 
                (c) WebSailors, 2017
     """
    print(colorama.Fore.RED + text)
    print(colorama.Fore.WHITE + '+----------------------------------------------------------------------------------------+')


def print_line(message: str) -> None:
    print(message)


def print_components(components: list) -> None:
    print('Components: \n')
    table = ASCIITable()
    table.set_columns_width([5, 60, 15])
    table.set_column_alignment(['c', 'l', 'l'])
    table.set_column_vertical_alignment(['c', 'c', 'c'])
    table.addRows([
        [get_string_color(ColorTemplates.GREEN, "#"),
         get_string_color(ColorTemplates.RED, "Component Name"),
         get_string_color(ColorTemplates.BLUE, "Component Version")]])
    if isinstance(components, list):
        cnt = 1
        for component in components:
            table.addRow(
                [get_string_color(ColorTemplates.GREEN, cnt),
                 get_string_color(ColorTemplates.RED, component['name']),
                 get_string_color(ColorTemplates.BLUE, component['version'])]
            )
            cnt += 1
    print(table.draw() + '\n')


def print_platforms(platforms: list) -> None:
    print('Platforms:')
    for index, platform in enumerate(platforms):
        print('# {0}: name: {1} description: {2}'.format(index, platform['name'], platform['description']))


def print_projects(projects: list) -> None:
    print('Projects:')
    for index, project in enumerate(projects):
        print('# {0}: name: {1} description: {2}'.format(index, project['name'], project['description']))


def print_issues(issues: list) -> None:
    print('Issues:')
    for index, issue in enumerate(issues):
        print('# {0}: name: {1} description: {2}'.format(index, issue['name'], issue['description']))

def main():

    print_line('123')


if __name__ == '__main__':
    main()
