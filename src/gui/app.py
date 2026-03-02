"""CustomTkinter application window — Microsoft To Do redesign."""

from datetime import date, datetime

import customtkinter as ctk
from tkcalendar import DateEntry

from src.models.task import VALID_CATEGORIES, VALID_PRIORITIES, VALID_RECURRENCES
from src.services.task_service import TaskService

# ── Color constants ──
ACCENT_BLUE = "#2564CF"
ACCENT_BLUE_HOVER = "#1B4EA3"
SIDEBAR_BG = ("#F5F5F5", "#2D2D2D")
CARD_BG = ("#FFFFFF", "#3B3B3B")
MAIN_BG = ("#EBEBEB", "#1E1E1E")
DETAIL_BG = ("#FAFAFA", "#2D2D2D")
COMPLETED_COLOR = "#A0A0A0"
STAR_ACTIVE = "#F2C94C"
STAR_INACTIVE = "#808080"
SIDEBAR_SELECTED = ("#E0E8F5", "#1A3A5C")
SIDEBAR_WIDTH = 220
DETAIL_PANEL_WIDTH = 320

CATEGORY_LABELS = ("None", *VALID_CATEGORIES)
PRIORITY_LABELS = ("None", *VALID_PRIORITIES)
RECURRENCE_LABELS = ("None", *VALID_RECURRENCES)
SORT_OPTIONS = {
    "Created Date": "created_at",
    "Due Date": "due_date",
    "Priority": "priority",
    "Alphabetical": "title",
}

# Smart list definitions: (key, icon, label)
SMART_LISTS = [
    ("my_day", "☀", "My Day"),
    ("important", "⭐", "Important"),
    ("planned", "📅", "Planned"),
    ("all", "📋", "All Tasks"),
]


class CalendarDialog(ctk.CTkToplevel):
    """Popup calendar for picking a date."""

    def __init__(self, parent, on_select, initial_date=None):
        super().__init__(parent)
        self.title("Select Date")
        self.geometry("300x300")
        self.resizable(False, False)
        self._on_select = on_select
        self._initial_date = initial_date
        self.after(200, self._build_widgets)

    def _build_widgets(self):
        self.grab_set()
        self.lift()
        self.focus_force()

        init = self._initial_date or date.today()
        self._cal = DateEntry(
            self, selectmode="day", year=init.year, month=init.month, day=init.day,
            date_pattern="yyyy-mm-dd",
        )
        self._cal.pack(padx=20, pady=20, fill="x")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Select", command=self._select, width=80).pack(
            side="left", padx=10
        )
        ctk.CTkButton(btn_frame, text="Clear", command=self._clear, width=80, fg_color="gray").pack(
            side="left", padx=10
        )
        ctk.CTkButton(
            btn_frame, text="Cancel", command=self.destroy, width=80, fg_color="gray",
        ).pack(side="left", padx=10)

    def _select(self):
        self._on_select(self._cal.get_date())
        self.destroy()

    def _clear(self):
        self._on_select(None)
        self.destroy()


class TodoApp(ctk.CTk):
    """Main application window — Microsoft To Do style 3-pane layout."""

    def __init__(self, service: TaskService):
        super().__init__()
        self._service = service

        self.title("To Do")
        self.geometry("1100x700")
        self.minsize(900, 600)

        ctk.set_appearance_mode("system")

        self._active_view = "my_day"
        self._detail_task = None
        self._sidebar_items = {}  # key -> (frame, count_label)

        self._build_ui()
        self._refresh_tasks()

    # ── UI Construction ──────────────────────────────────────────────

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main
        self.grid_columnconfigure(2, weight=0)  # detail

        self._build_sidebar()
        self._build_main_panel()
        self._build_detail_panel()

    # ── Sidebar ──────────────────────────────────────────────────────

    def _build_sidebar(self):
        self._sidebar = ctk.CTkFrame(
            self, width=SIDEBAR_WIDTH, fg_color=SIDEBAR_BG, corner_radius=0,
        )
        self._sidebar.grid(row=0, column=0, sticky="ns")
        self._sidebar.grid_propagate(False)

        # App title
        ctk.CTkLabel(
            self._sidebar, text="To Do",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ACCENT_BLUE,
        ).pack(padx=15, pady=(20, 15), anchor="w")

        # Smart lists
        for key, icon, label in SMART_LISTS:
            self._create_sidebar_item(key, icon, label)

        # Separator
        sep = ctk.CTkFrame(self._sidebar, height=1, fg_color="gray")
        sep.pack(fill="x", padx=15, pady=10)

        # Category lists
        for cat in VALID_CATEGORIES:
            self._create_sidebar_item(cat, "📁", cat.capitalize())

    def _create_sidebar_item(self, key, icon, label):
        frame = ctk.CTkFrame(self._sidebar, fg_color="transparent", cursor="hand2")
        frame.pack(fill="x", padx=8, pady=1)

        icon_lbl = ctk.CTkLabel(frame, text=icon, width=25)
        icon_lbl.pack(side="left", padx=(8, 5), pady=6)

        text_lbl = ctk.CTkLabel(frame, text=label, anchor="w")
        text_lbl.pack(side="left", fill="x", expand=True, pady=6)

        count_lbl = ctk.CTkLabel(frame, text="0", text_color="gray", width=30)
        count_lbl.pack(side="right", padx=(0, 8), pady=6)

        self._sidebar_items[key] = (frame, count_lbl, text_lbl)

        # Click binding on frame and all children
        for widget in (frame, icon_lbl, text_lbl, count_lbl):
            widget.bind("<Button-1>", lambda e, k=key: self._select_view(k))

        # Highlight if active
        if key == self._active_view:
            frame.configure(fg_color=SIDEBAR_SELECTED)
            text_lbl.configure(font=ctk.CTkFont(weight="bold"))

    def _select_view(self, key):
        # Deselect old
        if self._active_view in self._sidebar_items:
            old_frame, _, old_text = self._sidebar_items[self._active_view]
            old_frame.configure(fg_color="transparent")
            old_text.configure(font=ctk.CTkFont())

        self._active_view = key

        # Select new
        if key in self._sidebar_items:
            new_frame, _, new_text = self._sidebar_items[key]
            new_frame.configure(fg_color=SIDEBAR_SELECTED)
            new_text.configure(font=ctk.CTkFont(weight="bold"))

        # Update header title
        title_map = {s[0]: s[2] for s in SMART_LISTS}
        for cat in VALID_CATEGORIES:
            title_map[cat] = cat.capitalize()
        self._header_title.configure(text=title_map.get(key, key))

        self._close_detail()
        self._refresh_tasks()

    # ── Main Panel ───────────────────────────────────────────────────

    def _build_main_panel(self):
        self._main_panel = ctk.CTkFrame(self, fg_color=MAIN_BG, corner_radius=0)
        self._main_panel.grid(row=0, column=1, sticky="nsew")
        self._main_panel.grid_rowconfigure(1, weight=1)
        self._main_panel.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self._main_panel, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)

        self._header_title = ctk.CTkLabel(
            header, text="My Day",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        self._header_title.grid(row=0, column=0, sticky="w")

        # Search + sort row
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.grid(row=0, column=1, sticky="e")

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_tasks())
        ctk.CTkEntry(
            controls, textvariable=self._search_var, width=160,
            placeholder_text="🔍 Search...",
        ).pack(side="left", padx=(0, 8))

        self._sort_var = ctk.StringVar(value="Created Date")
        ctk.CTkOptionMenu(
            controls, variable=self._sort_var,
            values=list(SORT_OPTIONS.keys()), width=130,
            command=lambda _: self._refresh_tasks(),
        ).pack(side="left", padx=(0, 8))

        self._sort_order_var = ctk.StringVar(value="desc")
        ctk.CTkSegmentedButton(
            controls, values=["asc", "desc"],
            variable=self._sort_order_var,
            command=lambda _: self._refresh_tasks(),
        ).pack(side="left")

        # Task scroll area
        self._task_frame = ctk.CTkScrollableFrame(
            self._main_panel, fg_color=MAIN_BG, corner_radius=0,
        )
        self._task_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Add bar at bottom
        add_bar = ctk.CTkFrame(self._main_panel, fg_color="transparent")
        add_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))
        add_bar.grid_columnconfigure(0, weight=1)

        self._add_entry = ctk.CTkEntry(
            add_bar, placeholder_text="+ Add a task", height=40,
        )
        self._add_entry.grid(row=0, column=0, sticky="ew")
        self._add_entry.bind("<Return>", lambda e: self._add_task())

        # Error label
        self._error_label = ctk.CTkLabel(
            self._main_panel, text="", text_color="red",
        )
        self._error_label.grid(row=3, column=0, sticky="w", padx=20)

    # ── Detail Panel ─────────────────────────────────────────────────

    def _build_detail_panel(self):
        self._detail_panel = ctk.CTkFrame(
            self, width=DETAIL_PANEL_WIDTH, fg_color=DETAIL_BG, corner_radius=0,
        )
        # Hidden by default
        self._detail_visible = False

    def _open_detail(self, task):
        self._detail_task = task
        self._build_detail_content()
        if not self._detail_visible:
            self._detail_panel.grid(row=0, column=2, sticky="ns")
            self._detail_panel.grid_propagate(False)
            self._detail_visible = True

    def _close_detail(self):
        if self._detail_visible:
            self._auto_save_detail()
            self._detail_panel.grid_remove()
            self._detail_visible = False
            self._detail_task = None

    def _build_detail_content(self):
        # Clear existing
        for w in self._detail_panel.winfo_children():
            w.destroy()

        task = self._detail_task
        if not task:
            return

        scroll = ctk.CTkScrollableFrame(
            self._detail_panel, fg_color="transparent",
            width=DETAIL_PANEL_WIDTH - 20,
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Close button
        close_btn = ctk.CTkButton(
            scroll, text="✕", width=30, height=30,
            fg_color="transparent", hover_color=("gray85", "gray30"),
            command=self._close_detail,
        )
        close_btn.pack(anchor="e", padx=5, pady=(5, 0))

        # Checkbox + title row
        title_row = ctk.CTkFrame(scroll, fg_color="transparent")
        title_row.pack(fill="x", padx=10, pady=(0, 10))

        self._detail_completed_var = ctk.BooleanVar(value=task.is_completed)
        ctk.CTkCheckBox(
            title_row, text="", variable=self._detail_completed_var,
            width=30, fg_color=ACCENT_BLUE, hover_color=ACCENT_BLUE_HOVER,
            command=self._toggle_detail_task,
        ).pack(side="left", padx=(0, 8))

        self._detail_title_var = ctk.StringVar(value=task.title)
        title_entry = ctk.CTkEntry(
            title_row, textvariable=self._detail_title_var,
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title_entry.pack(side="left", fill="x", expand=True)
        title_entry.bind("<FocusOut>", lambda e: self._auto_save_detail())

        # ── Field rows ──
        def _add_field(parent, label_text):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(frame, text=label_text, width=100, anchor="w").pack(side="left")
            return frame

        # Priority star
        pri_frame = _add_field(scroll, "Priority")
        self._detail_star_var = ctk.StringVar(
            value="★" if task.priority == "high" else "☆"
        )
        self._detail_star_btn = ctk.CTkButton(
            pri_frame, textvariable=self._detail_star_var, width=35,
            fg_color="transparent",
            text_color=STAR_ACTIVE if task.priority == "high" else STAR_INACTIVE,
            hover_color=("gray85", "gray30"),
            font=ctk.CTkFont(size=18),
            command=self._toggle_detail_star,
        )
        self._detail_star_btn.pack(side="left")

        # Due date
        due_frame = _add_field(scroll, "Due Date")
        self._detail_due_var = ctk.StringVar(
            value=str(task.due_date) if task.due_date else ""
        )
        due_entry = ctk.CTkEntry(
            due_frame, textvariable=self._detail_due_var, width=140,
            placeholder_text="YYYY-MM-DD",
        )
        due_entry.pack(side="left")
        due_entry.bind("<FocusOut>", lambda e: self._auto_save_detail())
        ctk.CTkButton(
            due_frame, text="📅", width=30,
            fg_color="transparent", hover_color=("gray85", "gray30"),
            command=self._open_detail_calendar,
        ).pack(side="left", padx=4)

        # Recurrence
        rec_frame = _add_field(scroll, "Recurrence")
        self._detail_recurrence_var = ctk.StringVar(value=task.recurrence or "None")
        ctk.CTkOptionMenu(
            rec_frame, variable=self._detail_recurrence_var,
            values=list(RECURRENCE_LABELS), width=140,
            command=lambda _: self._auto_save_detail(),
        ).pack(side="left")

        # Due time
        time_frame = _add_field(scroll, "Due Time")
        self._detail_time_var = ctk.StringVar(value=task.due_time or "")
        time_entry = ctk.CTkEntry(
            time_frame, textvariable=self._detail_time_var, width=140,
            placeholder_text="HH:MM",
        )
        time_entry.pack(side="left")
        time_entry.bind("<FocusOut>", lambda e: self._auto_save_detail())

        # Reminder
        rem_frame = _add_field(scroll, "Reminder")
        self._detail_reminder_var = ctk.StringVar(
            value=str(task.reminder_minutes) if task.reminder_minutes is not None else ""
        )
        rem_entry = ctk.CTkEntry(
            rem_frame, textvariable=self._detail_reminder_var, width=140,
            placeholder_text="minutes before",
        )
        rem_entry.pack(side="left")
        rem_entry.bind("<FocusOut>", lambda e: self._auto_save_detail())

        # Category
        cat_frame = _add_field(scroll, "Category")
        self._detail_category_var = ctk.StringVar(value=task.category or "None")
        ctk.CTkOptionMenu(
            cat_frame, variable=self._detail_category_var,
            values=list(CATEGORY_LABELS), width=140,
            command=lambda _: self._auto_save_detail(),
        ).pack(side="left")

        # Description
        ctk.CTkLabel(scroll, text="Description", anchor="w").pack(
            fill="x", padx=10, pady=(10, 2),
        )
        self._detail_desc_textbox = ctk.CTkTextbox(scroll, height=100)
        self._detail_desc_textbox.pack(fill="x", padx=10, pady=(0, 10))
        if task.description:
            self._detail_desc_textbox.insert("1.0", task.description)
        self._detail_desc_textbox.bind("<FocusOut>", lambda e: self._auto_save_detail())

        # Detail error label
        self._detail_error_label = ctk.CTkLabel(scroll, text="", text_color="red")
        self._detail_error_label.pack(padx=10, pady=(0, 5))

        # Delete button
        ctk.CTkButton(
            scroll, text="Delete Task", fg_color="red", hover_color="darkred",
            command=self._delete_detail_task,
        ).pack(padx=10, pady=(5, 15))

    def _toggle_detail_star(self):
        if not self._detail_task:
            return
        if self._detail_star_var.get() == "★":
            self._detail_star_var.set("☆")
            self._detail_star_btn.configure(text_color=STAR_INACTIVE)
        else:
            self._detail_star_var.set("★")
            self._detail_star_btn.configure(text_color=STAR_ACTIVE)
        self._auto_save_detail()

    def _toggle_detail_task(self):
        if not self._detail_task:
            return
        try:
            self._service.toggle_task(self._detail_task.id)
        except KeyError:
            pass
        self._refresh_tasks()

    def _open_detail_calendar(self):
        initial = None
        due_str = self._detail_due_var.get().strip()
        if due_str:
            try:
                initial = date.fromisoformat(due_str)
            except ValueError:
                pass

        def on_select(d):
            if d is None:
                self._detail_due_var.set("")
            else:
                self._detail_due_var.set(str(d))
            self._auto_save_detail()

        CalendarDialog(self, on_select, initial)

    def _auto_save_detail(self):
        """Save detail panel fields back to the task."""
        task = self._detail_task
        if not task:
            return

        title = self._detail_title_var.get().strip()
        if not title:
            return  # don't save empty title

        desc = self._detail_desc_textbox.get("1.0", "end-1c").strip() or None
        priority = "high" if self._detail_star_var.get() == "★" else "medium"
        category = self._detail_category_var.get()
        if category == "None":
            category = None

        due_date = None
        due_str = self._detail_due_var.get().strip()
        if due_str:
            try:
                due_date = date.fromisoformat(due_str)
            except ValueError:
                self._detail_error_label.configure(text="Invalid date format")
                return

        recurrence = self._detail_recurrence_var.get()
        if recurrence == "None":
            recurrence = None

        due_time = self._detail_time_var.get().strip() or None
        reminder_str = self._detail_reminder_var.get().strip()
        reminder_minutes = None
        if reminder_str:
            try:
                reminder_minutes = int(reminder_str)
            except ValueError:
                self._detail_error_label.configure(text="Reminder must be a number")
                return

        try:
            self._service.update_task(
                task.id, title, desc,
                priority=priority, category=category, due_date=due_date,
                recurrence=recurrence, due_time=due_time,
                reminder_minutes=reminder_minutes,
            )
            self._detail_error_label.configure(text="")
            self._refresh_tasks()
        except (ValueError, KeyError) as e:
            self._detail_error_label.configure(text=str(e))

    def _delete_detail_task(self):
        if not self._detail_task:
            return
        task_id = self._detail_task.id
        self._detail_task = None  # prevent auto-save on close
        self._detail_panel.grid_remove()
        self._detail_visible = False
        self._delete_task(task_id)

    # ── Task Cards ───────────────────────────────────────────────────

    def _create_task_card(self, task):
        card = ctk.CTkFrame(
            self._task_frame, fg_color=CARD_BG, corner_radius=10,
        )
        card.pack(fill="x", padx=5, pady=3)

        # Hover effect
        def on_enter(e):
            card.configure(fg_color=("gray93", "#444444"))

        def on_leave(e):
            card.configure(fg_color=CARD_BG)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Left: checkbox
        var = ctk.BooleanVar(value=task.is_completed)
        cb = ctk.CTkCheckBox(
            card, text="", variable=var, width=30,
            fg_color=ACCENT_BLUE, hover_color=ACCENT_BLUE_HOVER,
            command=lambda tid=task.id: self._toggle_task(tid),
        )
        cb.pack(side="left", padx=(12, 8), pady=10)

        # Center content
        center = ctk.CTkFrame(card, fg_color="transparent")
        center.pack(side="left", fill="x", expand=True, pady=8)
        # Click body opens detail
        center.bind("<Button-1>", lambda e, t=task: self._open_detail(t))

        # Title
        title_color = COMPLETED_COLOR if task.is_completed else None
        title_kwargs = {"text": task.title, "anchor": "w"}
        if title_color:
            title_kwargs["text_color"] = title_color
        title_lbl = ctk.CTkLabel(center, **title_kwargs)
        title_lbl.pack(anchor="w")
        title_lbl.bind("<Button-1>", lambda e, t=task: self._open_detail(t))

        # Subtitle line
        parts = []
        if task.due_date:
            due_text = str(task.due_date)
            if task.due_time:
                due_text += f" {task.due_time}"
            parts.append(f"📅 {due_text}")
        if task.recurrence:
            parts.append(f"🔁 {task.recurrence}")
        if task.category:
            parts.append(task.category)

        if parts:
            sub_lbl = ctk.CTkLabel(
                center, text="  ·  ".join(parts),
                text_color="gray", font=ctk.CTkFont(size=11),
                anchor="w",
            )
            sub_lbl.pack(anchor="w")
            sub_lbl.bind("<Button-1>", lambda e, t=task: self._open_detail(t))

        # Right: star toggle
        is_high = task.priority == "high"
        star_text = "★" if is_high else "☆"
        star_color = STAR_ACTIVE if is_high else STAR_INACTIVE
        star_btn = ctk.CTkButton(
            card, text=star_text, width=30,
            fg_color="transparent", text_color=star_color,
            hover_color=("gray85", "gray30"),
            font=ctk.CTkFont(size=16),
            command=lambda t=task: self._toggle_star(t),
        )
        star_btn.pack(side="right", padx=(0, 12), pady=10)

    def _toggle_star(self, task):
        new_priority = "medium" if task.priority == "high" else "high"
        try:
            self._service.update_task(
                task.id, task.title, task.description,
                priority=new_priority, category=task.category,
                due_date=task.due_date, recurrence=task.recurrence,
                due_time=task.due_time, reminder_minutes=task.reminder_minutes,
            )
        except (ValueError, KeyError):
            pass
        self._refresh_tasks()

    # ── Task operations ──────────────────────────────────────────────

    def _add_task(self):
        title = self._add_entry.get().strip()
        if not title:
            return

        # Smart defaults based on active view
        kwargs = {"priority": "medium"}

        if self._active_view == "my_day":
            kwargs["due_date"] = date.today()
        elif self._active_view == "important":
            kwargs["priority"] = "high"
        elif self._active_view in VALID_CATEGORIES:
            kwargs["category"] = self._active_view

        try:
            self._service.add_task(title, **kwargs)
            self._add_entry.delete(0, "end")
            self._error_label.configure(text="")
            self._refresh_tasks()
        except ValueError as e:
            self._error_label.configure(text=str(e))

    def _toggle_task(self, task_id: int):
        try:
            self._service.toggle_task(task_id)
        except KeyError:
            pass
        self._refresh_tasks()

    def _delete_task(self, task_id: int):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        def _build_delete_widgets():
            dialog.grab_set()
            dialog.lift()
            dialog.focus_force()

            ctk.CTkLabel(dialog, text="Are you sure you want to\ndelete this task?").pack(pady=20)
            btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            btn_frame.pack(pady=10)

            def confirm():
                try:
                    self._service.delete_task(task_id)
                except KeyError:
                    pass
                dialog.destroy()
                self._refresh_tasks()

            ctk.CTkButton(btn_frame, text="Delete", fg_color="red", command=confirm, width=80).pack(
                side="left", padx=10
            )
            ctk.CTkButton(
                btn_frame, text="Cancel", fg_color="gray", command=dialog.destroy, width=80
            ).pack(side="left", padx=10)

        dialog.after(200, _build_delete_widgets)

    # ── Refresh & filtering ──────────────────────────────────────────

    def _refresh_tasks(self):
        for widget in self._task_frame.winfo_children():
            widget.destroy()

        search = self._search_var.get().strip() or None
        sort_by = SORT_OPTIONS.get(self._sort_var.get(), "created_at")
        sort_order = self._sort_order_var.get()

        # Build query args based on active view
        status = None
        priority = None
        category = None
        post_filters = []

        view = self._active_view
        if view == "all":
            pass  # no filters
        elif view == "my_day":
            status = "active"
            today = date.today()
            post_filters.append(lambda t: t.due_date == today)
        elif view == "important":
            priority = "high"
            status = "active"
        elif view == "planned":
            status = "active"
            post_filters.append(lambda t: t.due_date is not None)
        elif view in VALID_CATEGORIES:
            category = view

        tasks = self._service.list_tasks(
            search=search, status=status, priority=priority,
            category=category, sort_by=sort_by, sort_order=sort_order,
        )

        for f in post_filters:
            tasks = [t for t in tasks if f(t)]

        if not tasks:
            ctk.CTkLabel(
                self._task_frame, text="No tasks found.",
                text_color="gray",
            ).pack(pady=20)
        else:
            for task in tasks:
                self._create_task_card(task)

        self._update_sidebar_counts()

    def _update_sidebar_counts(self):
        all_tasks = self._service.list_tasks()
        today = date.today()

        counts = {
            "my_day": sum(
                1 for t in all_tasks if not t.is_completed and t.due_date == today
            ),
            "important": sum(
                1 for t in all_tasks if not t.is_completed and t.priority == "high"
            ),
            "planned": sum(
                1 for t in all_tasks if not t.is_completed and t.due_date is not None
            ),
            "all": len(all_tasks),
        }
        for cat in VALID_CATEGORIES:
            counts[cat] = sum(1 for t in all_tasks if t.category == cat)

        for key, (_, count_lbl, _) in self._sidebar_items.items():
            count_lbl.configure(text=str(counts.get(key, 0)))

    # ── Reminder popup (unchanged) ───────────────────────────────────

    def _show_reminder_popup(self, task_id: int, title: str, due_dt: datetime):
        """Show in-app reminder popup. Must be called via self.after() from main thread."""
        def _build():
            popup = ctk.CTkToplevel(self)
            popup.title("⏰ Reminder")
            popup.geometry("350x150")
            popup.resizable(False, False)

            def _build_content():
                popup.grab_set()
                popup.lift()
                popup.focus_force()
                ctk.CTkLabel(
                    popup, text=f"📋 {title}", font=ctk.CTkFont(size=14, weight="bold")
                ).pack(pady=(15, 5))
                ctk.CTkLabel(
                    popup, text=f"Due: {due_dt.strftime('%Y-%m-%d %H:%M')}"
                ).pack(pady=5)
                ctk.CTkButton(
                    popup, text="Dismiss", command=popup.destroy, width=100
                ).pack(pady=10)

            popup.after(200, _build_content)

        self.after(0, _build)
