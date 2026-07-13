# apps/api_v0.py

def add_dark_mode_toggle(view_func):
    """Enhanced dark mode for Swagger UI with VS Code Dark+ color scheme"""
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        if hasattr(response, 'content') and b'<!DOCTYPE html>' in response.content:
            content = response.content.decode('utf-8')
            
            dark_mode_code = """
            <style>
                /* VS Code Dark+ theme colors */
                body.dark-mode,
                body.dark-mode .swagger-ui {
                    background-color: #1e1e1e !important;
                    color: #cccccc !important;
                }
                
                /* Info section */
                body.dark-mode .swagger-ui .info .title {
                    color: #ffffff !important;
                }
                body.dark-mode .swagger-ui .info .description,
                body.dark-mode .swagger-ui .info .info__description {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .info a {
                    color: #3794ff !important;
                }
                body.dark-mode .swagger-ui .info a:hover {
                    color: #5caeff !important;
                }
                
                /* Top bar */
                body.dark-mode .swagger-ui .topbar {
                    background-color: #252526 !important;
                    border-bottom: 1px solid #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .topbar .download-url-wrapper .download-url-button {
                    background-color: #0e639c !important;
                }
                
                /* Operation blocks */
                body.dark-mode .swagger-ui .opblock {
                    background-color: #252526 !important;
                    border-color: #3c3c3c !important;
                    box-shadow: none !important;
                    border-radius: 4px !important;
                }
                body.dark-mode .swagger-ui .opblock .opblock-summary {
                    border-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .opblock .opblock-summary-method {
                    background-color: #1e1e1e !important;
                    color: #d4d4d4 !important;
                    font-weight: 600 !important;
                }
                body.dark-mode .swagger-ui .opblock .opblock-summary-path {
                    color: #d4d4d4 !important;
                }
                body.dark-mode .swagger-ui .opblock .opblock-summary-description {
                    color: #9cdcfe !important;
                }
                
                /* Method-specific header backgrounds */
                body.dark-mode .swagger-ui .opblock-get .opblock-summary-method {
                    background-color: #0e639c !important;
                    color: white !important;
                }
                body.dark-mode .swagger-ui .opblock-post .opblock-summary-method {
                    background-color: #2b7e2b !important;
                    color: white !important;
                }
                body.dark-mode .swagger-ui .opblock-put .opblock-summary-method {
                    background-color: #b8860b !important;
                    color: white !important;
                }
                body.dark-mode .swagger-ui .opblock-delete .opblock-summary-method {
                    background-color: #a31515 !important;
                    color: white !important;
                }
                body.dark-mode .swagger-ui .opblock-patch .opblock-summary-method {
                    background-color: #6a1b9a !important;
                    color: white !important;
                }
                
                /* Operation content */
                body.dark-mode .swagger-ui .opblock-description-wrapper p,
                body.dark-mode .swagger-ui .opblock-external-docs-wrapper p,
                body.dark-mode .swagger-ui .opblock-title_normal p {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .opblock .opblock-section-header {
                    background-color: #2d2d2d !important;
                    border-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .opblock .opblock-section-header h4 {
                    color: #d4d4d4 !important;
                }
                
                /* Parameters and responses */
                body.dark-mode .swagger-ui .parameter__name {
                    color: #9cdcfe !important;
                }
                body.dark-mode .swagger-ui .parameter__type,
                body.dark-mode .swagger-ui .parameter__in {
                    color: #ce9178 !important;
                }
                body.dark-mode .swagger-ui .response-col_status,
                body.dark-mode .swagger-ui .response-col_description {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .responses-inner h5,
                body.dark-mode .swagger-ui .responses-inner h4 {
                    color: #d4d4d4 !important;
                }
                
                /* Tables */
                body.dark-mode .swagger-ui table thead tr td,
                body.dark-mode .swagger-ui table thead tr th {
                    color: #d4d4d4 !important;
                    border-bottom-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui table tbody tr td {
                    color: #cccccc !important;
                    border-bottom-color: #2d2d2d !important;
                }
                body.dark-mode .swagger-ui table tbody tr td code {
                    color: #ce9178 !important;
                }
                
                /* Buttons */
                body.dark-mode .swagger-ui .btn {
                    color: #d4d4d4 !important;
                    background-color: #3c3c3c !important;
                    border-color: #4c4c4c !important;
                }
                body.dark-mode .swagger-ui .btn:hover {
                    background-color: #4c4c4c !important;
                }
                body.dark-mode .swagger-ui .btn.cancel {
                    background-color: #a31515 !important;
                    border-color: #c72a2a !important;
                    color: white !important;
                }
                body.dark-mode .swagger-ui .btn.authorize {
                    border-color: #3794ff !important;
                    color: #3794ff !important;
                    background-color: transparent !important;
                }
                body.dark-mode .swagger-ui .btn.authorize svg {
                    fill: #3794ff !important;
                }
                body.dark-mode .swagger-ui .btn.execute {
                    background-color: #0e639c !important;
                    border-color: #1177bb !important;
                    color: white !important;
                }
                
                /* Tabs */
                body.dark-mode .swagger-ui .tab li {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .tab li.selected {
                    border-bottom-color: #3794ff !important;
                    color: #d4d4d4 !important;
                }
                
                /* Models / Schemas */
                body.dark-mode .swagger-ui .model-title {
                    color: #d4d4d4 !important;
                }
                body.dark-mode .swagger-ui .model .property {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .model .property.primitive {
                    color: #9cdcfe !important;
                }
                body.dark-mode .swagger-ui .model .property.string {
                    color: #ce9178 !important;
                }
                body.dark-mode .swagger-ui .model .property.number,
                body.dark-mode .swagger-ui .model .property.integer {
                    color: #b5cea8 !important;
                }
                body.dark-mode .swagger-ui .model .property.boolean {
                    color: #ce9178 !important;
                }
                body.dark-mode .swagger-ui .model .property.array {
                    color: #9cdcfe !important;
                }
                body.dark-mode .swagger-ui .model-toggle:after {
                    filter: invert(0.8);
                }
                
                /* Schema viewer (JSON) */
                body.dark-mode .swagger-ui .highlight-code {
                    background-color: #1e1e1e !important;
                }
                body.dark-mode .swagger-ui .highlight-code > div {
                    background-color: #1e1e1e !important;
                }
                body.dark-mode .swagger-ui .microlight {
                    background-color: #1e1e1e !important;
                    color: #d4d4d4 !important;
                }
                
                /* Response examples */
                body.dark-mode .swagger-ui .live-responses-table .response-col_description,
                body.dark-mode .swagger-ui .response-col_description__inner {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .response-col_description__inner pre {
                    background-color: #1e1e1e !important;
                }
                
                /* Models container */
                body.dark-mode .swagger-ui .models {
                    border-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .models h4 {
                    color: #d4d4d4 !important;
                }
                body.dark-mode .swagger-ui .models .model-container {
                    background-color: #252526 !important;
                }
                
                /* Copy button */
                body.dark-mode .swagger-ui .copy-to-clipboard {
                    background-color: #3c3c3c !important;
                    border-color: #4c4c4c !important;
                }
                body.dark-mode .swagger-ui .copy-to-clipboard svg {
                    fill: #cccccc !important;
                }
                
                /* Arrow icons */
                body.dark-mode .swagger-ui .arrow,
                body.dark-mode .swagger-ui .expand-operation svg,
                body.dark-mode .swagger-ui .opblock-control-arrow svg {
                    filter: invert(0.8);
                }
                
                /* Section headers */
                body.dark-mode .swagger-ui .opblock-tag {
                    color: #d4d4d4 !important;
                    border-bottom-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .opblock-tag small {
                    color: #9cdcfe !important;
                }
                
                /* Authorization modal */
                body.dark-mode .swagger-ui .dialog-ux .modal-ux {
                    background-color: #252526 !important;
                    border-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .dialog-ux .modal-ux-header {
                    border-bottom-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .dialog-ux .modal-ux-header h3 {
                    color: #d4d4d4 !important;
                }
                body.dark-mode .swagger-ui .dialog-ux .modal-ux-content {
                    color: #cccccc !important;
                }
                body.dark-mode .swagger-ui .auth-container .auth-btn-wrapper {
                    border-top-color: #3c3c3c !important;
                }
                body.dark-mode .swagger-ui .scopes h2,
                body.dark-mode .swagger-ui .scopes p {
                    color: #cccccc !important;
                }
                
                /* Input fields */
                body.dark-mode .swagger-ui input,
                body.dark-mode .swagger-ui select,
                body.dark-mode .swagger-ui textarea {
                    background-color: #3c3c3c !important;
                    color: #d4d4d4 !important;
                    border-color: #4c4c4c !important;
                }
                body.dark-mode .swagger-ui input:focus,
                body.dark-mode .swagger-ui select:focus,
                body.dark-mode .swagger-ui textarea:focus {
                    border-color: #3794ff !important;
                }
                
            /* Dark mode toggle button */
            .dark-mode-toggle {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
                background: #0e639c;
                color: white;
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                transition: transform 0.2s, background 0.2s;
            }
            .dark-mode-toggle:hover {
                transform: scale(1.1);
                background: #1177bb;
            }
            body.dark-mode .dark-mode-toggle {
                background: #d9534f;  /* reddish‑orange */
            }
            body.dark-mode .dark-mode-toggle:hover {
                background: #e67a6b;  /* lighter reddish‑orange on hover */
            }
            </style>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()" title="Toggle dark mode">🌓</button>
            <script>
                function toggleDarkMode() {
                    document.body.classList.toggle('dark-mode');
                    localStorage.setItem('swagger-dark-mode', document.body.classList.contains('dark-mode'));
                }
                
                // Load saved preference
                if (localStorage.getItem('swagger-dark-mode') === 'true') {
                    document.body.classList.add('dark-mode');
                }
                
                // Auto-detect system preference on first visit if no saved preference
                if (localStorage.getItem('swagger-dark-mode') === null) {
                    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                        document.body.classList.add('dark-mode');
                        localStorage.setItem('swagger-dark-mode', 'true');
                    }
                }
            </script>
            """
            
            # Insert the dark mode code before the closing </body> tag
            if '</body>' in content:
                content = content.replace('</body>', f'{dark_mode_code}</body>')
                response.content = content.encode('utf-8')
        
        return response
    return wrapper