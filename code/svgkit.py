"""给课程配图用的极简 SVG 画布（只用标准库，不需要 matplotlib）。

配图脚本（`code/fig*.py`）是**作者出图用的工具**，不是课程练习：
读者只要打开 `assets/` 里已经生成好的图就够了。想自己重新出图：

    python3 code/fig07_standard_error.py     # 重新生成 assets/fig07_standard_error.svg

画布坐标：原点左上，x 向右、y 向下；`fig.plot(...)` 一类方法收的是"数据坐标"，
内部按 `set_view()` 设好的范围换算到像素。
"""

import math
import os
import unicodedata


class Canvas:
    def __init__(self, width=760, height=460, title="", sub=""):
        self.w = width
        self.h = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" font-family="system-ui, -apple-system, '
            "'PingFang SC', 'Microsoft YaHei', sans-serif\">",
            f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        ]
        if title:
            self.parts.append(
                f'<text x="26" y="30" font-size="19" font-weight="600" fill="#1a1a1a">{esc(title)}</text>')
        if sub:
            self.parts.append(
                f'<text x="26" y="50" font-size="12.5" fill="#7a7a7a">{esc(sub)}</text>')

    # ---- 坐标换算：由 set_view 记录数据范围与绘图区像素框 ----
    def set_view(self, x0, x1, y0, y1, left=64, right=None, top=72, bottom=None):
        self.vx0, self.vx1 = x0, x1
        self.vy0, self.vy1 = y0, y1
        self.pl = left
        self.pr = right if right is not None else self.w - 26
        self.pt = top
        self.pb = bottom if bottom is not None else self.h - 46

    def X(self, x):
        return self.pl + (x - self.vx0) / (self.vx1 - self.vx0) * (self.pr - self.pl)

    def Y(self, y):
        return self.pb - (y - self.vy0) / (self.vy1 - self.vy0) * (self.pb - self.pt)

    # ---- 图元 ----
    def frame(self):
        self.parts.append(
            f'<rect x="{self.pl:.1f}" y="{self.pt:.1f}" width="{self.pr - self.pl:.1f}" '
            f'height="{self.pb - self.pt:.1f}" fill="none" stroke="#d8d8d8"/>')

    def grid_x(self, ticks, label_fmt="{:.0f}", rotate=False):
        for t in ticks:
            px = self.X(t)
            self.parts.append(
                f'<line x1="{px:.1f}" y1="{self.pt:.1f}" x2="{px:.1f}" y2="{self.pb:.1f}" '
                f'stroke="#ededed"/>')
            lab = label_fmt.format(t)
            if rotate:
                self.parts.append(
                    f'<text x="{px:.1f}" y="{self.pb + 14:.1f}" font-size="11" fill="#5a5a5a" '
                    f'text-anchor="end" transform="rotate(-40 {px:.1f} {self.pb + 14:.1f})">{esc(lab)}</text>')
            else:
                self.parts.append(
                    f'<text x="{px:.1f}" y="{self.pb + 18:.1f}" font-size="11" fill="#5a5a5a" '
                    f'text-anchor="middle">{esc(lab)}</text>')

    def grid_y(self, ticks, label_fmt="{:.1f}"):
        for t in ticks:
            py = self.Y(t)
            self.parts.append(
                f'<line x1="{self.pl:.1f}" y1="{py:.1f}" x2="{self.pr:.1f}" y2="{py:.1f}" '
                f'stroke="#ededed"/>')
            self.parts.append(
                f'<text x="{self.pl - 8:.1f}" y="{py + 4:.1f}" font-size="11" fill="#5a5a5a" '
                f'text-anchor="end">{esc(label_fmt.format(t))}</text>')

    def zero_line(self, y=0.0, color="#9a9a9a"):
        py = self.Y(y)
        self.parts.append(
            f'<line x1="{self.pl:.1f}" y1="{py:.1f}" x2="{self.pr:.1f}" y2="{py:.1f}" '
            f'stroke="{color}" stroke-width="1.2" stroke-dasharray="4 3"/>')

    def plot(self, xs, ys, color="#2f6fb0", width=2.2, dash=None, opacity=1.0):
        pts = " ".join(f"{self.X(a):.1f},{self.Y(b):.1f}" for a, b in zip(xs, ys))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"'
            f'{d} opacity="{opacity}" stroke-linejoin="round"/>')

    def dots(self, xs, ys, color="#c2410c", r=3.6, opacity=1.0):
        for a, b in zip(xs, ys):
            self.parts.append(
                f'<circle cx="{self.X(a):.1f}" cy="{self.Y(b):.1f}" r="{r}" fill="{color}" '
                f'opacity="{opacity}"/>')

    def vbars(self, xs, ys, color="#2f6fb0", gap=0.18, opacity=0.9):
        """柱状：xs 是柱中心，ys 是柱高（从数据下界起）。"""
        for x, y in zip(xs, ys):
            px = self.X(x)
            w = abs(self.X(x + 1) - self.X(x)) * (1 - gap)
            y0 = self.Y(max(self.vy0, 0))
            y1 = self.Y(y)
            self.parts.append(
                f'<rect x="{px - w / 2:.1f}" y="{y1:.1f}" width="{w:.1f}" '
                f'height="{max(0.0, y0 - y1):.1f}" fill="{color}" opacity="{opacity}"/>')

    def hline(self, y, color="#8a8a8a", width=1.4, dash="5 4"):
        py = self.Y(y)
        self.parts.append(
            f'<line x1="{self.pl:.1f}" y1="{py:.1f}" x2="{self.pr:.1f}" y2="{py:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>')

    def vline(self, x, color="#8a8a8a", width=1.2, dash=None, y0=None, y1=None):
        px = self.X(x)
        top = self.Y(y1) if y1 is not None else self.pt
        bot = self.Y(y0) if y0 is not None else self.pb
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{px:.1f}" y1="{top:.1f}" x2="{px:.1f}" y2="{bot:.1f}" '
            f'stroke="{color}" stroke-width="{width}"{d}/>')

    def rug(self, values, color="#c2410c", frac=0.07, width=2.0):
        """底部短竖线：把原始记录一条一条钉在横轴上。"""
        h = (self.pb - self.pt) * frac
        for v in values:
            px = self.X(v)
            self.parts.append(
                f'<line x1="{px:.1f}" y1="{self.pb:.1f}" x2="{px:.1f}" y2="{self.pb - h:.1f}" '
                f'stroke="{color}" stroke-width="{width}" opacity="0.85"/>')

    def band(self, x0, x1, color="#c2410c", opacity=0.08):
        """整高的一条竖向底色，用来圈出"这一段占几成"。"""
        self.parts.append(
            f'<rect x="{self.X(x0):.1f}" y="{self.pt:.1f}" width="{self.X(x1) - self.X(x0):.1f}" '
            f'height="{self.pb - self.pt:.1f}" fill="{color}" opacity="{opacity}"/>')

    def xlabel(self, text):
        self.parts.append(
            f'<text x="{(self.pl + self.pr) / 2:.1f}" y="{self.h - 10}" font-size="12.5" '
            f'fill="#454545" text-anchor="middle">{esc(text)}</text>')

    def ylabel(self, text):
        self.parts.append(
            f'<text x="16" y="{(self.pt + self.pb) / 2:.1f}" font-size="12.5" fill="#454545" '
            f'text-anchor="middle" transform="rotate(-90 16 {(self.pt + self.pb) / 2:.1f})">{esc(text)}</text>')

    def label(self, x, y, text, color="#3a3a3a", size=12.5, anchor="start", dx=0, dy=0):
        self.parts.append(
            f'<text x="{self.X(x) + dx:.1f}" y="{self.Y(y) + dy:.1f}" font-size="{size}" '
            f'fill="{color}" text-anchor="{anchor}">{esc(text)}</text>')

    def note_at(self, px, py, text, color="#7a7a7a", size=12, anchor="start"):
        self.parts.append(
            f'<text x="{px:.1f}" y="{py:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{esc(text)}</text>')

    def legend(self, items, px, py, anchor="start"):
        """items = [(颜色, 线型dash或None, 文字), ...]；anchor=end 时整块右对齐到 px。"""
        width = sum(22 + 5 + text_width(text) + 26 for _, _, text in items) - 26
        x = px - width if anchor == "end" else px
        for color, dash, text in items:
            if dash == "dot":
                self.parts.append(
                    f'<circle cx="{x + 11:.1f}" cy="{py:.1f}" r="3.4" fill="{color}"/>')
            else:
                d = f' stroke-dasharray="{dash}"' if dash else ""
                self.parts.append(
                    f'<line x1="{x:.1f}" y1="{py:.1f}" x2="{x + 22:.1f}" y2="{py:.1f}" '
                    f'stroke="{color}" stroke-width="2.4"{d}/>')
            self.parts.append(
                f'<text x="{x + 27:.1f}" y="{py + 4:.1f}" font-size="12" fill="#454545">{esc(text)}</text>')
            x += 22 + 5 + text_width(text) + 26

    def save(self, path):
        self.parts.append("</svg>")
        path = os.path.normpath(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.parts))
        return path


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text_width(text, size=12):
    """估一行字的像素宽度：汉字/全角按一个 em，其余按 0.55 em。"""
    em = sum(1.0 if unicodedata.east_asian_width(c) in ("W", "F") else 0.55 for c in text)
    return size * em


def spread(vals):
    n = len(vals)
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))
