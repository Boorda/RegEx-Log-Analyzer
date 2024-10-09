from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import re

class RegexHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Metacharacters
        meta_format = QTextCharFormat()
        meta_format.setForeground(QColor("blue"))
        meta_format.setFontWeight(QFont.Bold)
        meta_chars = ['\\.', '\\^', '\\$', '\\*', '\\+', '\\?', '\\(', '\\)', '\\[', '\\]', '\\{', '\\}', '\\|']
        for pattern in meta_chars:
            self.highlighting_rules.append((re.compile(pattern), meta_format))

        # Character classes
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("green"))
        self.highlighting_rules.append((re.compile('\\\\[dDwWsS]'), class_format))

        # Quantifiers
        quant_format = QTextCharFormat()
        quant_format.setForeground(QColor("red"))
        self.highlighting_rules.append((re.compile('\\{[^}]+\\}'), quant_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)