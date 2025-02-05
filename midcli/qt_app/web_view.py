from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings

class MainWebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._configure_settings()

    def _configure_settings(self):
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        level_str = {
            QWebEnginePage.InfoMessageLevel: "Info",
            QWebEnginePage.WarningMessageLevel: "Warning", 
            QWebEnginePage.ErrorMessageLevel: "Error",
        }.get(level, "Unknown")
        print(f"[{level_str}] {message} (line: {lineNumber}, source: {sourceID})")

class MainWebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_web_page()
        self._configure_global_settings()
        self.loadFinished.connect(self._on_load_finished)

    def _setup_web_page(self):
        self.main_page = MainWebPage(self)
        self.setPage(self.main_page)

    def _configure_global_settings(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

    def _on_load_finished(self, ok):
        if ok:
            js = """
            document.querySelectorAll('iframe').forEach(function(iframe) {
                if (iframe.hasAttribute('sandbox')) {
                    let sandbox = iframe.getAttribute('sandbox')
                        .split(' ')
                        .filter(flag => flag !== 'allow-storage-access-by-user-activation')
                        .join(' ');
                    iframe.setAttribute('sandbox', sandbox);
                }
            });
            """
            self.main_page.runJavaScript(js) 