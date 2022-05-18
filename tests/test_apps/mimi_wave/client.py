try:
    import mimi_wave_ui.qt.client_qt
except ImportError as i:
    print(i)
    try:
        import mimi_wave_ui.tk.client_tk
    except ImportError as i:
        print(i)
        ...
