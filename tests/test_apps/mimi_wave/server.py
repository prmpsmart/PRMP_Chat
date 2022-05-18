try:
    import mimi_wave_ui.qt.server_qt
except ImportError as i:
    print(i)
    try:
        import mimi_wave_ui.tk.server_tk
    except ImportError as i:
        print(i)
