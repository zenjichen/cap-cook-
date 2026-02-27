"""
CapCut Bypass Pro Tool
Tác giả gốc: zenjichen
GUI hiện đại được rebuild từ binary analysis
"""

import sys
import os
import json
import uuid
import shutil
import threading
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QLinearGradient
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QPlainTextEdit, QStatusBar,
    QFrame, QScrollArea, QCheckBox, QProgressBar, QSizePolicy,
    QGraphicsDropShadowEffect, QSpacerItem, QLineEdit, QFileDialog
)


# ─────────────────────────────────────────
#  DARK THEME stylesheet
# ─────────────────────────────────────────
DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #0f0f1a;
    color: #e0e0f0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QFrame#card {
    background-color: #1a1a2e;
    border-radius: 12px;
    border: 1px solid #2a2a4a;
}

QFrame#headerCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #16213e, stop:1 #0f3460);
    border-radius: 12px;
    border: 1px solid #2a4a8a;
}

QLabel#titleLabel {
    color: #00d4ff;
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 2px;
}

QLabel#subtitleLabel {
    color: #7a8ab8;
    font-size: 11px;
}

QLabel#sectionLabel {
    color: #a0b0e0;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase;
}

QLabel#linkLabel {
    color: #00d4ff;
    font-size: 11px;
}

QComboBox {
    background-color: #1e1e3a;
    color: #c0d0ff;
    border: 1px solid #3040a0;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #00d4ff;
    background-color: #252545;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
    color: #00d4ff;
}

QComboBox QAbstractItemView {
    background-color: #12122a;
    color: #a0b8e0;
    border: 1px solid #3040a0;
    border-radius: 6px;
    padding: 4px;
    outline: none;
    show-decoration-selected: 1;
}

QComboBox QAbstractItemView::item {
    padding: 7px 12px;
    border-radius: 4px;
    min-height: 22px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #1e2c5a;
    color: #c0d8ff;
}

QComboBox QAbstractItemView::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1e0060, stop:1 #003060);
    color: #ffffff;
    border-left: 3px solid #00d4ff;
    font-weight: bold;
    padding-left: 9px;
}

QPushButton#btnLoad {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a3a6a, stop:1 #1a5a9a);
    color: #a0d4ff;
    border: 1px solid #2060b0;
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 12px;
    font-weight: bold;
    min-width: 90px;
}

QPushButton#btnLoad:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2050a0, stop:1 #2070c0);
    border-color: #00d4ff;
    color: #00d4ff;
}

QPushButton#btnLoad:pressed {
    background-color: #0a264a;
}

QPushButton#btnBypass {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b00ff, stop:1 #00d4ff);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 12px 30px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 2px;
    min-width: 160px;
    min-height: 20px;
}

QPushButton#btnBypass:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #9b20ff, stop:1 #20e4ff);
}

QPushButton#btnBypass:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b00cc, stop:1 #00a0cc);
}

QPushButton#btnBypass:disabled {
    background: #2a2a4a;
    color: #555575;
}

QCheckBox {
    color: #a0b0d0;
    font-size: 12px;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border-radius: 4px;
    border: 1.5px solid #3a50b0;
    background-color: #12122a;
}

QCheckBox::indicator:hover {
    border-color: #00d4ff;
    background-color: #1a1a3e;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #5500cc, stop:1 #0099cc);
    border: 1.5px solid #00d4ff;
}

QCheckBox:checked {
    color: #e8f0ff;
    font-weight: bold;
}

QPlainTextEdit {
    background-color: #0d0d1f;
    color: #00ff88;
    border: 1px solid #1a2a5a;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Cascadia Code', 'Consolas', monospace;
    font-size: 11px;
    line-height: 1.5;
}

QPlainTextEdit:focus {
    border-color: #00d4ff;
}

QProgressBar {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b00ff, stop:1 #00d4ff);
    border-radius: 6px;
}

QScrollBar:vertical {
    background: #0f0f1a;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #2a2a5a;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #3a3a8a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QStatusBar {
    background-color: #0a0a15;
    color: #4a5a8a;
    font-size: 10px;
    border-top: 1px solid #1a1a3a;
}

QPushButton#btnHelp {
    background: transparent;
    color: #7b8ab8;
    border: 1px solid #2a3a6a;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton#btnHelp:hover {
    background-color: #1a2a4a;
    color: #00d4ff;
    border-color: #00d4ff;
}

QDialog {
    background-color: #0f0f1a;
}

QLabel#helpTitle {
    color: #00d4ff;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 1px;
}

QLabel#helpStep {
    color: #e0e0f0;
    font-size: 12px;
    padding: 2px 0px;
}

QLabel#helpNote {
    color: #ffaa00;
    font-size: 11px;
    font-style: italic;
}

QFrame#helpCard {
    background-color: #1a1a2e;
    border-radius: 10px;
    border: 1px solid #2a2a4a;
}

QFrame#stepLine {
    background-color: #2a2a4a;
    max-height: 1px;
}
"""


# ─────────────────────────────────────────
#  CUSTOM CHECKBOX (real checkmark via QPainter)
# ─────────────────────────────────────────
class CustomCheckBox(QCheckBox):
    """QCheckBox with a hand-drawn white checkmark indicator."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._box = 17   # indicator size px

    def paintEvent(self, event):
        """Draw the checkbox manually so the checkmark is always visible."""
        from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
        from PyQt5.QtCore import QRect, QPoint
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        sz = self._box
        top = (self.height() - sz) // 2
        box = QRect(0, top, sz, sz)

        checked = self.isChecked()
        hovered = self.underMouse()

        # ── Box background ──────────────────────────────────────────────
        if checked:
            grad = QtGui.QLinearGradient(box.topLeft(), box.bottomRight())
            grad.setColorAt(0, QColor("#5500cc"))
            grad.setColorAt(1, QColor("#0099cc"))
            p.setBrush(QBrush(grad))
            p.setPen(QPen(QColor("#00d4ff"), 1.5))
        else:
            p.setBrush(QBrush(QColor("#12122a")))
            border_color = QColor("#00d4ff") if hovered else QColor("#3a50b0")
            p.setPen(QPen(border_color, 1.5))

        p.drawRoundedRect(box, 4, 4)

        # ── Checkmark ✓ ─────────────────────────────────────────────────
        if checked:
            pen = QPen(QColor("white"), 2.2)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            p.setBrush(Qt.NoBrush)
            # points relative to box (sz=17)
            x0, y0 = box.x(), box.y()
            pts = [
                QPoint(x0 + 3,  y0 + 9),
                QPoint(x0 + 7,  y0 + 13),
                QPoint(x0 + 14, y0 + 4),
            ]
            p.drawPolyline(pts[0], pts[1], pts[2])

        # ── Label text ───────────────────────────────────────────────────
        text_x = sz + 8
        p.setPen(QPen(QColor("#e8f0ff" if checked else "#a0b0d0")))
        font = self.font()
        if checked:
            font.setBold(True)
        p.setFont(font)
        p.drawText(
            text_x, 0,
            self.width() - text_x, self.height(),
            Qt.AlignVCenter | Qt.AlignLeft,
            self.text()
        )
        p.end()

    def sizeHint(self):
        sh = super().sizeHint()
        return QSize(sh.width() + 4, max(sh.height(), self._box + 6))


# ─────────────────────────────────────────
#  BYPASS WORKER THREAD
# ─────────────────────────────────────────
class BypassWorker(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(bool)
    progress_signal = pyqtSignal(int)

    def __init__(self, draft_content_path: str, options: dict):
        super().__init__()
        self.draft_content_path = draft_content_path
        self.options = options

    def log(self, msg):
        self.log_signal.emit(msg)

    def run(self):
        try:
            with open(self.draft_content_path, encoding="utf-8") as f:
                draft = json.load(f)
        except Exception as e:
            self.log(f"❌ Không đọc được file draft: {e}")
            self.done_signal.emit(False)
            return

        steps = [
            ("subtitle",       "🔤 Bypass Subtitle...",        self.bypass_subtitle),
            ("audio",          "🔊 Bypass Audio (TTS)...",      self.bypass_audio),
            ("effect",         "✨ Bypass Video Effects...",    self.bypass_effect),
            ("music",          "🎵 Bypass Music...",            self.bypass_music),
            ("stickers",       "🎨 Bypass Stickers...",         self.bypass_stickers),
            ("text_effect",    "🖋️  Bypass Text Effects...",    self.bypass_text_effect),
            ("transitions",    "🔀 Bypass Transitions...",      self.bypass_transitions),
            ("text_templates", "📝 Bypass Text Templates...",   self.bypass_text_templates),
        ]

        enabled = [s for s in steps if self.options.get(s[0], True)]
        total = len(enabled)

        for i, (key, msg, func) in enumerate(enabled):
            self.log(msg)
            try:
                func(draft, self.draft_content_path)
            except Exception as e:
                self.log(f"  ⚠️  Lỗi {key}: {e}")
            self.progress_signal.emit(int((i + 1) / total * 100))

        self.log("✅ Bypass hoàn thành!")
        self.done_signal.emit(True)

    # ── helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def save(draft, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(draft, f, ensure_ascii=False, indent=2)

    def clean_ai_text(self, text_obj):
        for k in ["recognize_type","recognize_task_id","recognize_model","recognize_text",
                   "lyric_group_id","is_lyric_effect","subtitle_keywords",
                   "subtitle_keywords_config","tts_auto_update","bilingual_lan","translation_text"]:
            text_obj.pop(k, None)
        return text_obj

    def clean_ai_audio(self, audio_obj):
        for k in ["text_id","resource_id","aigc_history_id","aigc_item_id",
                  "extra_info","subtitle_fragment_info_list"]:
            audio_obj.pop(k, None)
        return audio_obj

    # ── bypass functions ───────────────────────────────────────────────────

    def bypass_subtitle(self, draft, path):
        materials = draft.get("materials", {})
        texts = materials.get("texts", [])
        tracks = draft.get("tracks", [])
        new_texts = []
        for track in tracks:
            if track.get("type") != "text":
                continue
            for seg in track.get("segments", []):
                cache_raw = seg.get("subtitle_cache_info", None)
                if not cache_raw:
                    continue
                try:
                    cache = json.loads(cache_raw) if isinstance(cache_raw, str) else cache_raw
                except Exception:
                    continue
                for sentence in cache.get("sentence_list", []):
                    text_id = sentence.get("text_id", "")
                    for t in texts:
                        if t.get("id", "") == text_id:
                            nt = dict(t)
                            nt["content"] = sentence.get("text", nt.get("content", ""))
                            nt.setdefault("font_path", "")
                            nt.setdefault("font_size", 8)
                            nt["material_id"] = str(uuid.uuid4()).upper()
                            nt.setdefault("source_timerange", {
                                "start": sentence.get("start_time", 0),
                                "duration": sentence.get("end_time", 0) - sentence.get("start_time", 0)
                            })
                            new_texts.append(nt)
                seg.pop("subtitle_cache_info", None)
        materials.setdefault("texts", []).extend(new_texts)
        config = draft.get("config", {})
        for k in ["subtitle_taskinfo","subtitle_recognition_id","lyrics_taskinfo",
                  "lyrics_recognition_id","multi_language_mode","multi_language_list","multi_language_current"]:
            config.pop(k, None)
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {len(new_texts)} subtitle segments")

    def bypass_audio(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for audio in materials.get("audios", []):
            if audio.get("type") != "text_to_audio":
                continue
            self.clean_ai_audio(audio)
            ap = audio.get("path", "")
            if ap and os.path.exists(ap):
                new_ap = ap.replace(".mp3", "_hunght1890.mp3")
                try:
                    os.rename(ap, new_ap)
                    audio["path"] = new_ap
                except Exception:
                    pass
            count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} audio TTS")

    def bypass_effect(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for effect in materials.get("video_effects", []):
            new_eid = str(uuid.uuid4()).upper()
            new_rid = str(uuid.uuid4()).upper()
            epath = effect.get("path", "")
            old_eid = effect.get("effect_id", "")
            if epath and old_eid:
                parts = epath.replace("\\", "/").split("/")
                new_dir = "/".join(parts[:-1]).replace(old_eid, new_eid)
                new_path = new_dir + "/" + parts[-1]
                try:
                    os.makedirs(new_dir, exist_ok=True)
                    if os.path.exists(os.path.dirname(epath)):
                        shutil.copytree(os.path.dirname(epath), new_dir, dirs_exist_ok=True)
                except Exception:
                    pass
                effect["effect_id"] = new_eid
                effect["path"] = new_path
                effect["resource_id"] = new_rid
                count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} video effects")

    def bypass_music(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for audio in materials.get("audios", []):
            if audio.get("type") == "text_to_audio":
                continue
            if audio.get("music_id"):
                audio["music_id"] = str(uuid.uuid4()).upper()
                count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} music items")

    def bypass_stickers(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for sticker in materials.get("stickers", []):
            old_id = sticker.get("id", "")
            if not old_id:
                continue
            new_id = str(uuid.uuid4()).upper()
            old_path = sticker.get("path", "")
            if old_path:
                sub = os.path.basename(os.path.dirname(old_path))
                new_path = old_path.replace(sub, new_id)
                try:
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    if os.path.exists(old_path):
                        shutil.copy2(old_path, new_path)
                except Exception:
                    pass
                sticker["id"] = new_id
                sticker["path"] = new_path
                sticker["sticker_id"] = new_id
                count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} stickers")

    def bypass_text_effect(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for effect in materials.get("effects", []):
            old_id = effect.get("id", "")
            if not old_id:
                continue
            new_id = str(uuid.uuid4()).upper()
            old_path = effect.get("path", "")
            if old_path:
                sub = os.path.basename(os.path.dirname(old_path))
                new_path = old_path.replace(sub, new_id)
                try:
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    if os.path.exists(old_path):
                        shutil.copytree(os.path.dirname(old_path), os.path.dirname(new_path), dirs_exist_ok=True)
                except Exception:
                    pass
                effect["id"] = new_id
                effect["path"] = new_path
                for text in effect.get("texts", []):
                    for style in text.get("styles", []):
                        es = style.get("effectStyle", {})
                        if es.get("path"):
                            style["effectStyle"]["path"] = es["path"].replace(old_id, new_id)
                count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} text effects")

    def bypass_transitions(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for tr in materials.get("transitions", []):
            old_id = tr.get("id", "")
            if not old_id:
                continue
            new_id = str(uuid.uuid4()).upper()
            old_path = tr.get("path", "")
            if old_path:
                sub = os.path.basename(os.path.dirname(old_path))
                new_path = old_path.replace(sub, new_id)
                try:
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    if os.path.exists(old_path):
                        shutil.copytree(os.path.dirname(old_path), os.path.dirname(new_path), dirs_exist_ok=True)
                except Exception:
                    pass
                tr["id"] = new_id
                tr["third_resource_id"] = new_id
                tr["path"] = new_path
                count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} transitions")

    def bypass_text_templates(self, draft, path):
        materials = draft.get("materials", {})
        count = 0
        for tmpl in materials.get("text_templates", []):
            old_id = tmpl.get("id", "")
            if not old_id:
                continue
            new_id = str(uuid.uuid4()).upper()
            old_path = tmpl.get("path", "")
            if old_path:
                sub = os.path.basename(os.path.dirname(old_path))
                new_path = old_path.replace(sub, new_id)
                try:
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    if os.path.exists(old_path):
                        shutil.copytree(os.path.dirname(old_path), os.path.dirname(new_path), dirs_exist_ok=True)
                except Exception:
                    pass
                tmpl["id"] = new_id
                tmpl["template_id"] = new_id
                tmpl["path"] = new_path
                count += 1
        self.save(draft, path)
        self.log(f"  ✓ Đã xử lý {count} text templates")


# ─────────────────────────────────────────
#  HELP DIALOG
# ─────────────────────────────────────────
class HelpDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hướng Dẫn Sử Dụng")
        self.setMinimumWidth(560)
        self.setModal(True)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # Title
        title = QLabel("📖  HƯỚNG DẪN SỬ DỤNG")
        title.setObjectName("helpTitle")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        # Divider
        div = QFrame(); div.setObjectName("stepLine")
        div.setFrameShape(QFrame.HLine)
        root.addWidget(div)

        steps = [
            ("1", "⚡", "Yêu cầu",
             "Đã cài CapCut và có ít nhất 1 project chứa tài nguyên Premium\n"
             "(subtitle, nhạc, sticker, hiệu ứng...) trước khi chạy tool."),

            ("2", "📂", "Chọn Project",
             "Nhấn 🔄 REFRESH để load danh sách project.\n"
             "Chọn đúng project bạn muốn bypass từ dropdown."),

            ("3", "☑️", "Chọn loại bypass",
             "Tick vào các loại tài nguyên cần bypass:\n"
             "  • Subtitle  — Xóa liên kết AI subtitle/lyrics\n"
             "  • Audio TTS  — Xóa metadata giọng đọc AI\n"
             "  • Video Effects  — Thay ID hiệu ứng video\n"
             "  • Music  — Thay ID nhạc nền\n"
             "  • Stickers  — Thay ID sticker\n"
             "  • Text Effects  — Thay ID hiệu ứng chữ\n"
             "  • Transitions  — Thay ID chuyển cảnh\n"
             "  • Text Templates  — Thay ID template chữ"),

            ("4", "⚡", "Thực hiện Bypass",
             "Nhấn nút BYPASS NGAY.\n"
             "Chờ thanh tiến trình chạy xong, theo dõi log bên dưới."),

            ("5", "🎬", "Kiểm tra kết quả",
             "Mở lại CapCut → vào project vừa bypass.\n"
             "Các tài nguyên premium sẽ không còn bị check bản quyền nữa."),
        ]

        for num, icon, step_title, desc in steps:
            card = QFrame(); card.setObjectName("helpCard")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(14, 12, 14, 12)
            card_layout.setSpacing(14)

            # Number badge
            badge = QLabel(num)
            badge.setFixedSize(28, 28)
            badge.setAlignment(Qt.AlignCenter)
            badge.setStyleSheet(
                "background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
                "stop:0 #7b00ff, stop:1 #00d4ff);"
                "border-radius: 14px; color: white; font-weight: bold; font-size: 12px;"
            )

            # Content
            content = QVBoxLayout()
            content.setSpacing(3)
            hdr = QLabel(f"{icon}  {step_title}")
            hdr.setStyleSheet("color: #a0d4ff; font-weight: bold; font-size: 12px;")
            body = QLabel(desc)
            body.setObjectName("helpStep")
            body.setWordWrap(True)
            content.addWidget(hdr)
            content.addWidget(body)

            card_layout.addWidget(badge)
            card_layout.addLayout(content, 1)
            root.addWidget(card)

        # Warning note
        note_card = QFrame(); note_card.setObjectName("helpCard")
        note_card.setStyleSheet("QFrame#helpCard { border: 1px solid #5a3a00; background-color: #1e1500; }")
        note_layout = QHBoxLayout(note_card)
        note_layout.setContentsMargins(14, 10, 14, 10)
        note = QLabel(
            "⚠️  LƯU Ý: Tool sửa trực tiếp file draft_content.json.\n"
            "Hãy backup project trước nếu cần. Chỉ dùng cho mục đích học tập & nghiên cứu."
        )
        note.setObjectName("helpNote")
        note.setWordWrap(True)
        note_layout.addWidget(note)
        root.addWidget(note_card)

        # Close button
        btn_close = QPushButton("✅  Đã hiểu, đóng lại")
        btn_close.setObjectName("btnBypass")
        btn_close.clicked.connect(self.accept)
        btn_close.setFixedHeight(38)
        root.addWidget(btn_close)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)


# ─────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────
class MainWindow(QMainWindow):
    CAPCUT_DRAFT_PATH = r"C:\Users\{user}\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"

    def __init__(self):
        super().__init__()
        self.username = os.getlogin()
        self.setWindowTitle("CapCut Bypass Pro")
        self.setMinimumSize(700, 600)
        self.resize(780, 680)
        self._setup_ui()
        self._load_projects()

    # ─── UI SETUP ─────────────────────────────────────────────────────────

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 12)
        root.setSpacing(12)

        # ── Header ──────────────────────────────────────────────────────
        header = QFrame(); header.setObjectName("headerCard")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 14, 20, 14)
        h_layout.setSpacing(12)

        # Icon area
        icon_lbl = QLabel("⚡")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 28))
        icon_lbl.setFixedWidth(50)
        icon_lbl.setAlignment(Qt.AlignCenter)

        # Title block
        title_block = QVBoxLayout()
        title_block.setSpacing(2)
        title = QLabel("CAPCUT BYPASS PRO"); title.setObjectName("titleLabel")
        subtitle = QLabel(f"👤  {self.username}  •  Loại bỏ watermark & tài nguyên Premium")
        subtitle.setObjectName("subtitleLabel")
        title_block.addWidget(title)
        title_block.addWidget(subtitle)

        # Social links
        links = QLabel(
            '<a href="https://www.facebook.com/NguyenManhHaOfficial" style="color:#00d4ff; text-decoration:none;">👤 Facebook</a>'
        )
        links.setObjectName("linkLabel")
        links.setOpenExternalLinks(True)
        links.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        h_layout.addWidget(icon_lbl)
        h_layout.addLayout(title_block, 1)
        h_layout.addWidget(links)
        root.addWidget(header)

        # ── Project Selector ────────────────────────────────────────────
        proj_card = QFrame(); proj_card.setObjectName("card")
        proj_layout = QVBoxLayout(proj_card)
        proj_layout.setContentsMargins(16, 14, 16, 14)
        proj_layout.setSpacing(10)

        lbl_sec1 = QLabel("📁  CHỌN PROJECT CAPCUT"); lbl_sec1.setObjectName("sectionLabel")
        proj_layout.addWidget(lbl_sec1)

        row1 = QHBoxLayout(); row1.setSpacing(10)
        self.combo_project = QComboBox()
        self.combo_project.setPlaceholderText("-- Chọn project --")
        self.combo_project.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.btn_load = QPushButton("🔄  REFRESH"); self.btn_load.setObjectName("btnLoad")
        self.btn_load.clicked.connect(self._load_projects)

        row1.addWidget(self.combo_project)
        row1.addWidget(self.btn_load)
        proj_layout.addLayout(row1)

        self.lbl_path = QLabel(""); self.lbl_path.setObjectName("subtitleLabel")
        self.lbl_path.setWordWrap(True)
        proj_layout.addWidget(self.lbl_path)
        self.combo_project.currentTextChanged.connect(self._update_path_label)

        # ── Manual path row ─────────────────────────────────────────────
        lbl_manual = QLabel("Hoặc chọn thủ công:")
        lbl_manual.setObjectName("subtitleLabel")
        proj_layout.addWidget(lbl_manual)

        row2 = QHBoxLayout(); row2.setSpacing(8)

        self.txt_manual_path = QLineEdit()
        self.txt_manual_path.setPlaceholderText("Paste đường dẫn tới draft_content.json hoặc nhấn 📂 Browse...")
        self.txt_manual_path.setStyleSheet(
            "QLineEdit {"
            "  background-color: #12122a;"
            "  color: #c0d0ff;"
            "  border: 1px solid #2a3a7a;"
            "  border-radius: 7px;"
            "  padding: 7px 10px;"
            "  font-size: 11px;"
            "}"
            "QLineEdit:focus { border-color: #00d4ff; }"
            "QLineEdit:hover { border-color: #4060c0; }"
        )
        self.txt_manual_path.textChanged.connect(self._on_manual_path_changed)

        btn_browse = QPushButton("📂  Browse")
        btn_browse.setObjectName("btnLoad")
        btn_browse.setFixedWidth(110)
        btn_browse.clicked.connect(self._browse_manual)

        btn_clear_path = QPushButton("✕")
        btn_clear_path.setObjectName("btnLoad")
        btn_clear_path.setFixedWidth(32)
        btn_clear_path.setToolTip("Xóa đường dẫn thủ công")
        btn_clear_path.clicked.connect(lambda: self.txt_manual_path.clear())

        row2.addWidget(self.txt_manual_path)
        row2.addWidget(btn_browse)
        row2.addWidget(btn_clear_path)
        proj_layout.addLayout(row2)

        root.addWidget(proj_card)

        # ── Options ─────────────────────────────────────────────────────
        opt_card = QFrame(); opt_card.setObjectName("card")
        opt_layout = QVBoxLayout(opt_card)
        opt_layout.setContentsMargins(16, 14, 16, 14)
        opt_layout.setSpacing(10)

        lbl_sec2 = QLabel("⚙️  TÙY CHỌN BYPASS"); lbl_sec2.setObjectName("sectionLabel")
        opt_layout.addWidget(lbl_sec2)

        opt_grid1 = QHBoxLayout(); opt_grid1.setSpacing(20)
        opt_grid2 = QHBoxLayout(); opt_grid2.setSpacing(20)

        self.checks = {}
        options = [
            ("subtitle",       "🔤 Subtitle"),
            ("audio",          "🔊 Audio TTS"),
            ("effect",         "✨ Video Effects"),
            ("music",          "🎵 Music"),
            ("stickers",       "🎨 Stickers"),
            ("text_effect",    "🖋️  Text Effects"),
            ("transitions",    "🔀 Transitions"),
            ("text_templates", "📝 Text Templates"),
        ]
        for i, (key, lbl) in enumerate(options):
            cb = CustomCheckBox(lbl); cb.setChecked(True)
            self.checks[key] = cb
            (opt_grid1 if i < 4 else opt_grid2).addWidget(cb)

        opt_grid1.addStretch()
        opt_grid2.addStretch()
        opt_layout.addLayout(opt_grid1)
        opt_layout.addLayout(opt_grid2)
        root.addWidget(opt_card)

        # ── Bypass Button + Progress ─────────────────────────────────────
        action_card = QFrame(); action_card.setObjectName("card")
        action_layout = QVBoxLayout(action_card)
        action_layout.setContentsMargins(16, 14, 16, 14)
        action_layout.setSpacing(10)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_bypass = QPushButton("⚡  BYPASS NGAY"); self.btn_bypass.setObjectName("btnBypass")
        self.btn_bypass.clicked.connect(self._start_bypass)
        btn_row.addWidget(self.btn_bypass)

        btn_help = QPushButton("❓  Hướng Dẫn"); btn_help.setObjectName("btnHelp")
        btn_help.clicked.connect(self._show_help)
        btn_help.setFixedHeight(42)
        btn_row.addWidget(btn_help)
        btn_row.addStretch()
        action_layout.addLayout(btn_row)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        action_layout.addWidget(self.progress)
        root.addWidget(action_card)

        # ── Log Output ───────────────────────────────────────────────────
        log_card = QFrame(); log_card.setObjectName("card")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(16, 14, 16, 14)
        log_layout.setSpacing(8)

        log_header = QHBoxLayout()
        lbl_sec3 = QLabel("🖥️  LOG OUTPUT"); lbl_sec3.setObjectName("sectionLabel")
        self.btn_clear = QPushButton("🗑 Xóa"); self.btn_clear.setObjectName("btnLoad")
        self.btn_clear.setFixedWidth(80)
        self.btn_clear.clicked.connect(lambda: self.log_area.clear())
        log_header.addWidget(lbl_sec3)
        log_header.addStretch()
        log_header.addWidget(self.btn_clear)
        log_layout.addLayout(log_header)

        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(160)
        self.log_area.setPlaceholderText("Output sẽ hiển thị ở đây...")
        log_layout.addWidget(self.log_area)
        root.addWidget(log_card)

        # ── Status Bar ───────────────────────────────────────────────────
        self.statusBar().showMessage("Sẵn sàng  •  Chọn project và nhấn BYPASS")

        # ── Drop shadow effect on cards ──────────────────────────────────
        for card in [header, proj_card, opt_card, action_card, log_card]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 120))
            card.setGraphicsEffect(shadow)

    # ─── PROJECT LOADING ──────────────────────────────────────────────────

    def _get_draft_dir(self):
        return self.CAPCUT_DRAFT_PATH.format(user=self.username)

    def _load_projects(self):
        draft_dir = self._get_draft_dir()
        self.combo_project.clear()
        try:
            projects = [
                p for p in os.listdir(draft_dir)
                if p != ".recycle_bin" and os.path.isdir(os.path.join(draft_dir, p))
            ]
            projects.sort(key=lambda p: os.path.getmtime(os.path.join(draft_dir, p)), reverse=True)
            if projects:
                self.combo_project.addItems(projects)
                self._log(f"📁 Tìm thấy {len(projects)} project(s)")
                self.statusBar().showMessage(f"{len(projects)} projects  •  Chọn project và nhấn BYPASS")
            else:
                self._log("⚠️  Không tìm thấy project nào.")
        except Exception as e:
            self._log(f"❌ Không tìm thấy thư mục CapCut: {e}")

    def _update_path_label(self, name):
        if name:
            path = os.path.join(self._get_draft_dir(), name, "draft_content.json")
            exists = "✅" if os.path.exists(path) else "❌"
            self.lbl_path.setText(f"{exists}  {path}")
        else:
            self.lbl_path.setText("")

    def _browse_manual(self):
        """Open file dialog to manually pick draft_content.json."""
        start_dir = self._get_draft_dir() if os.path.exists(self._get_draft_dir()) else os.path.expanduser("~")
        fpath, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file draft_content.json",
            start_dir,
            "CapCut Draft (draft_content.json);;JSON files (*.json);;All files (*.*)"
        )
        if fpath:
            self.txt_manual_path.setText(fpath)

    def _on_manual_path_changed(self, text):
        """Validate and show feedback on the manual path field."""
        text = text.strip()
        if not text:
            self.txt_manual_path.setStyleSheet(
                self.txt_manual_path.styleSheet()
                .replace("border: 1px solid #2a5a2a;", "")
                .replace("border: 1px solid #5a2a2a;", "")
            )
            return
        ok = os.path.isfile(text) and text.endswith(".json")
        color = "#2a5a2a" if ok else "#5a2a2a"
        self.txt_manual_path.setStyleSheet(
            f"QLineEdit {{"
            f"  background-color: #12122a;"
            f"  color: #c0d0ff;"
            f"  border: 1px solid {color};"
            f"  border-radius: 7px;"
            f"  padding: 7px 10px;"
            f"  font-size: 11px;"
            f"}}"
            f"QLineEdit:focus {{ border-color: {'#00ff88' if ok else '#ff4444'}; }}"
        )

    # ─── BYPASS ───────────────────────────────────────────────────────────

    def _start_bypass(self):
        # ── Xác định đường dẫn file draft ───────────────────────────────────
        manual = self.txt_manual_path.text().strip()

        if manual:
            # Ưu tiên path thủ công
            if not os.path.isfile(manual):
                self._log(f"❌ File thủ công không hợp lệ: {manual}")
                return
            draft_path = manual
            source_label = f"[Thủ công] {os.path.basename(os.path.dirname(draft_path))}"
        else:
            # Dùng combo dropdown
            project_name = self.combo_project.currentText()
            if not project_name:
                self._log("⚠️  Vui lòng chọn project hoặc nhập đường dẫn thủ công!")
                return
            draft_path = os.path.join(self._get_draft_dir(), project_name, "draft_content.json")
            source_label = project_name
            if not os.path.exists(draft_path):
                self._log(f"❌ Không tìm thấy file: {draft_path}")
                return

        options = {key: cb.isChecked() for key, cb in self.checks.items()}

        self._log(f"\n{'─'*50}")
        self._log(f"🚀 Bắt đầu bypass: {source_label}")
        self._log(f"📄 File: {draft_path}")
        self._log(f"{'─'*50}")

        self.btn_bypass.setEnabled(False)
        self.btn_bypass.setText("⏳  Đang xử lý...")
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.statusBar().showMessage("Đang bypass...")

        self.worker = BypassWorker(draft_path, options)
        self.worker.log_signal.connect(self._log)
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.done_signal.connect(self._on_done)
        self.worker.start()

    def _on_done(self, success):
        self.btn_bypass.setEnabled(True)
        self.btn_bypass.setText("⚡  BYPASS NGAY")
        self.progress.setValue(100 if success else 0)
        if success:
            self._log(f"\n🎉 Bypass thành công! Mở CapCut và kiểm tra project.")
            self.statusBar().showMessage("✅ Bypass hoàn thành!")
        else:
            self._log("\n❌ Bypass thất bại!")
            self.statusBar().showMessage("❌ Lỗi!")

    # ─── HELP ─────────────────────────────────────────────────────────────

    def _show_help(self):
        dlg = HelpDialog(self)
        dlg.exec_()

    # ─── LOG ──────────────────────────────────────────────────────────────

    def _log(self, msg: str):
        self.log_area.appendPlainText(msg)
        sb = self.log_area.verticalScrollBar()
        sb.setValue(sb.maximum())


# ─────────────────────────────────────────
#  ENTRY
# ─────────────────────────────────────────
if __name__ == "__main__":
    os.system("title CapCut Bypass Pro")
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    app.setStyle("Fusion")

    # Dark palette base
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0f0f1a"))
    palette.setColor(QPalette.WindowText, QColor("#e0e0f0"))
    palette.setColor(QPalette.Base, QColor("#0d0d1f"))
    palette.setColor(QPalette.Text, QColor("#c0d0ff"))
    palette.setColor(QPalette.Button, QColor("#1a1a2e"))
    palette.setColor(QPalette.ButtonText, QColor("#e0e0f0"))
    palette.setColor(QPalette.Highlight, QColor("#304090"))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

