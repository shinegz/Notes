"""
Playwright Python script boilerplate for webapp-e2e skill.
Copy this file as the starting point for each new test script.
Replace all <PLACEHOLDER> values before running.
"""
import json
import os
import re
import shutil
from playwright.sync_api import sync_playwright

# ── Scene identity ─────────────────────────────────────────────────────────────
SCENE_ID = "E0_scene_name"          # e.g. "E5_am_campaign_detail_bidding"
SCREENSHOT_DIR = f"tests/e2e/screenshots/{SCENE_ID}"


# ── Screenshot helper (MANDATORY — use for every screenshot) ───────────────────
def take_screenshot_at_step(page, step_num: str, filename: str,
                             target_selector: str = None) -> str:
    """
    Pre-screenshot routine:
    1. Closes any stray overlay (guide dialogs, onboarding banners, notifications).
    2. Scrolls the target element into viewport (if target_selector provided).
    3. Takes the screenshot.
    """
    # Step 1: Close stray overlays
    page.evaluate("""
        () => {
            const CLOSE_SELECTORS = [
                '.next-dialog-close',
                '.ant-modal-close',
                '[aria-label="close"]',
                '[aria-label="Close"]',
                'button[class*="close"]:not([disabled])',
            ];
            for (const sel of CLOSE_SELECTORS) {
                const visible = [...document.querySelectorAll(sel)].find(b => b.offsetParent);
                if (visible) { visible.click(); return sel; }
            }
            return null;
        }
    """)
    page.wait_for_timeout(400)

    # Step 2: Scroll target into viewport
    if target_selector:
        try:
            el = page.wait_for_selector(target_selector, timeout=5000)
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(400)
        except Exception:
            pass  # target may already be visible or selector not found — proceed

    # Step 3: Screenshot
    path = f"{SCREENSHOT_DIR}/{filename}"
    page.screenshot(path=path)
    print(f"  [step {step_num}] screenshot saved: {path}")
    return path


# ── Global state mock (Object.defineProperty freeze) ──────────────────────────
# ⚠️  CRITICAL: SPA HTML contains an inline <script> that overwrites window globals
# after page load. Plain add_init_script() assignment loses the race.
# Object.defineProperty with a no-op setter makes any later assignment silently
# fail, so the mock value is always the one the app reads. (Rule 4)
MOCK_STATE = {
    # Replace with actual fields from static analysis (§3.2 seven-step method)
    "featureList": [100, 200, 300],
    "seller": {"sellerId": 123456, "hasFeatureX": True},
}
MOCK_STATE_JSON = json.dumps(MOCK_STATE)

FROZEN_INIT_SCRIPT = f"""
(function() {{
  var mockData = {MOCK_STATE_JSON};
  try {{
    Object.defineProperty(window, '__globalVar__', {{
      get: function() {{ return mockData; }},
      set: function(v) {{ /* silently absorb inline <script> overwrite */ }},
      configurable: false,
      enumerable: true
    }});
  }} catch(e) {{
    window.__globalVar__ = mockData;  // already defined — fall back
  }}
}})();
"""


# ── Main ───────────────────────────────────────────────────────────────────────
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--ignore-certificate-errors"])
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    # ⚠️  Register add_init_script BEFORE page.goto().
    # It runs before any page script, so Object.defineProperty wins the race.
    page.add_init_script(FROZEN_INIT_SCRIPT)

    # Console error capture — helps diagnose mock failures (Rule 7)
    page.on("console", lambda msg: print(f"  [console:{msg.type}] {msg.text}")
            if msg.type == "error" else None)

    # Screenshot directory
    if os.path.exists(SCREENSHOT_DIR):
        shutil.rmtree(SCREENSHOT_DIR)
    os.makedirs(SCREENSHOT_DIR)

    # ── API mocks ──────────────────────────────────────────────────────────────
    # Rule: intercept network requests only — never mock the HTML page itself.
    # Route priority: more specific patterns must be registered BEFORE broad ones.
    page.route("**/api/your-endpoint**", lambda r: r.fulfill(
        status=200, content_type="application/json",
        body=json.dumps({"success": True, "result": {}})
    ))
    # Optional catch-all for unmatched API paths → generic success
    # page.route("**/api/**", lambda r: r.fulfill(
    #     status=200, content_type="application/json",
    #     body=json.dumps({"success": True, "result": {}})
    # ))

    # ── Navigation ────────────────────────────────────────────────────────────
    page.goto("https://localhost:<PORT>/#!/<path>")   # #!/ = hash-router SPA
    page.wait_for_load_state("domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass  # networkidle may not settle if there are long-polling requests

    # ── Static interaction analysis output ────────────────────────────────────
    # Fill this block after completing §3.3 Q1–Q4 before writing test steps.
    # Q1: <ElementA> hidden by default, trigger <precondition> first → Rule 12
    # Q2: <ElementA> Form Field controlled → click(3)+type(), not fill() → Rule 6C
    # Q3: iframe overlay present → use dispatch_event for Select trigger → Rule 13/14
    # Q4: submit disabled conditions: [cond1] [cond2] → ensure each is satisfied

    # ── Test steps ────────────────────────────────────────────────────────────
    # Step 1: ...
    # take_screenshot_at_step(page, "01", "step01_landing.png", "[class*='targetSection']")

    # ── Submit button pre-click diagnostic (§3.3 Q4 — use before every Confirm) ──
    # Uncomment if static analysis found multiple disabled conditions.
    # btn_state = page.evaluate("""
    #     () => {
    #         const footer = document.querySelector('<dialog-footer-selector>');
    #         if (!footer) return { found: false };
    #         return Array.from(footer.querySelectorAll('button')).map(b => ({
    #             text: b.textContent.trim(), disabled: b.disabled
    #         }));
    #     }
    # """)
    # print(f"Button state before submit: {btn_state}")
    # If any target button shows disabled=True, diagnose with Rule 15 before proceeding.

    browser.close()
