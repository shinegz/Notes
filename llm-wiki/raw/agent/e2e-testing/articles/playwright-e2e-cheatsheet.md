---
title: "Playwright E2E testing cheatsheet"
url: "https://dev.to/olhapi/playwright-e2e-testing-cheatsheet-15gl"
requestedUrl: "https://dev.to/olhapi/playwright-e2e-testing-cheatsheet-15gl"
author: "@"
coverImage: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F95zssh0i7k4ww6us5kyx.png"
siteName: "DEV Community"
publishedAt: "2025-08-19T19:19:20Z"
summary: "Table of Contents    General Playwright E2E testing best practices Test structure and... Tagged with e2e, testing, programming, javascript."
adapter: "generic"
capturedAt: "2026-04-24T04:54:17.274Z"
conversionMethod: "defuddle"
kind: "generic/article"
language: "en"
---

# Playwright E2E testing cheatsheet

## Table of Contents

1. General Playwright E2E testing best practices
2. Test structure and organization patterns
3. Locator strategies and best practices
4. Handling flaky tests and reliability
5. Performance optimization
6. Debugging techniques and tools
7. Writing E2E tests with Playwright and Claude Code
8. Modern testing approaches and anti-patterns

## 1\. General Playwright E2E testing best practices

### Core testing principles

**Test user-visible behavior**: Focus on what users actually see and interact with rather than implementation details. This approach ensures tests remain stable even when underlying code changes.

```
// ✅ Good - Testing user behavior
await page.getByRole('button', { name: 'Add to Cart' }).click();
await expect(page.getByText('Item added to cart')).toBeVisible();

// ❌ Bad - Testing implementation details
await page.locator('.btn-primary.add-cart-btn').click();
await expect(page.locator('#cart-count')).toHaveClass('updated');
```

### Test isolation principles

Each test should run independently with its own browser context, ensuring **complete isolation** of cookies, local storage, and session data. Playwright automatically provides this isolation, but proper test structure is essential:

```
test.beforeEach(async ({ page }) => {
  // Fresh context for each test
  await page.goto('https://example.com/');
  // Each test starts from a known state
});

test('isolated test example', async ({ page }) => {
  // This test has no dependencies on other tests
  await page.getByRole('link', { name: 'Products' }).click();
  await expect(page).toHaveURL('/products');
});
```

### Focus on critical user journeys

Prioritize testing based on business impact rather than achieving 100% coverage. **Essential workflows** include:

- User registration and authentication
- Core business transactions (checkout, payment)
- Data entry and retrieval operations
- Account management features
- Error recovery paths

## 2\. Test structure and organization patterns

### Folder structure

```
├── tests/
│   ├── auth/                    # Authentication flows
│   │   ├── login.spec.ts
│   │   └── registration.spec.ts
│   ├── e2e/                     # End-to-end scenarios
│   │   ├── checkout.spec.ts
│   │   └── user-journey.spec.ts
│   └── api/                     # API integration tests
│       └── backend.spec.ts
├── page-objects/
│   ├── pages/
│   │   ├── login-page.ts
│   │   └── checkout-page.ts
│   └── components/
│       └── navigation.ts
├── fixtures/
│   ├── test-data.ts            # Test data management
│   ├── auth-setup.ts           # Authentication fixtures
│   └── page-objects.ts         # POM fixtures
├── utils/
│   ├── data-factory.ts         # Dynamic data generation
│   └── test-helpers.ts
└── playwright.config.ts
```

### Test organization

**Group by business domain**: Organize tests around user journeys rather than technical implementation:

```
test.describe('User Authentication Flow', () => {
  test('successful login with valid credentials', async ({ page }) => {
    // Clear business intent
  });

  test('password reset journey', async ({ page }) => {
    // Complete user workflow
  });
});
```

### Advanced fixture architecture

Create reusable fixtures for common test patterns:

```
// fixtures/page-objects.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../page-objects/login-page';
import { DashboardPage } from '../page-objects/dashboard-page';

type PageObjects = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = base.extend<PageObjects>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

// Usage in tests
test('user workflow', async ({ loginPage, dashboardPage }) => {
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await dashboardPage.expectWelcomeMessage();
});
```

## 3\. Locator strategies

### Locator priority hierarchy

**1\. Role-based locators (highest priority)**

```
await page.getByRole('button', { name: 'Submit Order' }).click();
await page.getByRole('textbox', { name: 'Email Address' }).fill('user@example.com');
await page.getByRole('heading', { name: 'Welcome Dashboard' });
```

**2\. Test ID locators (stable and recommended)**

```
await page.getByTestId('checkout-submit-button').click();
```

**3\. Text-based locators (user-visible content)**

```
await page.getByText('Welcome back, John!').click();
await page.getByLabel('Password').fill('secure-password');
await page.getByPlaceholder('Enter your email').fill('user@example.com');
```

**4\. CSS/XPath (try to avoid)**

```
// Only when other options aren't viable
await page.locator('.legacy-element').click();
```

### Advanced locator patterns

**Chaining and filtering for complex scenarios**:

```
const productCard = page.getByRole('listitem')
  .filter({ hasText: 'iPhone 15 Pro' })
  .getByRole('button', { name: 'Add to Cart' });

await productCard.click();
```

**Data-testId naming convention**:

```
// Pattern: {scope}-{component}-{element}-{type}
data-testid="header-navigation-login-button"
data-testid="checkout-form-email-input"
data-testid="product-card-price-display"
```

## 4\. Handling flaky tests and improving reliability

### Common causes and solutions

**Root causes of flaky tests**:

- Unstable selectors
- Fixed time delays (hard waits)
- Race conditions and timing issues
- External dependencies
- Test interdependencies

### Auto-waiting mechanisms

Playwright automatically performs **actionability checks** before interacting with elements:

- **Visible**: Non-empty bounding box
- **Stable**: Same position for 2+ animation frames
- **Enabled**: Not disabled
- **Receives Events**: Not obscured
- **Editable**: For input actions
```
// Playwright waits automatically
await page.getByRole('button', { name: 'Submit' }).click();
// No manual wait needed - Playwright ensures button is clickable
```

### Retry strategies

**Global configuration**:

```
export default defineConfig({
  retries: process.env.CI ? 2 : 0, // 2 retries in CI
});
```

**Test-level retries**:

```
test.describe.configure({ retries: 2 });

test('potentially flaky test', async ({ page }, testInfo) => {
  if (testInfo.retry) {
    // Clean up state on retry
    await cleanupTestData();
  }
  // Test logic
});
```

[**Custom retry logic**](https://playwright.dev/docs/test-assertions#expecttopass):

```
await expect(async () => {
  await page.locator('button').click();
  await expect(page.locator('div')).toBeVisible();
}).toPass();
```

### Network stubbing for reliability

```
// Mock external dependencies
await page.route('**/api/users', async (route) => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'John Doe' }
    ])
  });
});

// Block unnecessary resources
await context.route(/\.(css|jpg|png)$/, route => route.abort());
```

## 5\. Performance optimization for E2E tests

### Parallel execution configuration

```
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined, // Optimize for environment

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
});
```

### Test sharding

```
# Split tests across multiple machines/processes
npx playwright test --shard=1/4
npx playwright test --shard=2/4
npx playwright test --shard=3/4
npx playwright test --shard=4/4
```

**GitHub actions sharding**:

```
strategy:
  matrix:
    shard: [1, 2, 3, 4]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}/4
```

### Resource optimization

#### Network cache

Speed up Playwright tests by caching network requests on the filesystem. Try [playwright-network-cache](https://github.com/vitalets/playwright-network-cache)

#### Disable heavy resources when not needed

```
export default defineConfig({
  use: {
    trace: 'retain-on-failure',  // Only on failures
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',

    // Performance settings
    navigationTimeout: 30000,
    actionTimeout: 10000,
  }
});
```

### Browser context management

**Optimized Context Configuration**:

```
const context = await browser.newContext({
  ignoreHTTPSErrors: true,
  serviceWorkers: 'block',  // Prevent interference
  reducedMotion: 'reduce',  // Faster animations

  // Performance optimizations
  viewport: { width: 1280, height: 720 },
  deviceScaleFactor: 1,
});
```

## 6\. Debugging techniques and tools

### Playwright inspector

Launch the interactive debugger:

```
# Debug all tests
npx playwright test --debug

# Debug specific test
npx playwright test example.spec.ts:10 --debug
```

**Inspector features**:

- Step through test execution
- Live edit locators
- Pick locators from page
- View actionability logs
- Record new test actions

### UI Mode (Interactive Testing)

```
npx playwright test --ui
```

**UI Mode Capabilities**:

- **Watch Mode**: Auto-rerun on file changes
- **Time Travel**: Step through execution timeline
- **DOM Snapshots**: Inspect page state at each step
- **Network Tab**: View all requests
- **Console Logs**: Real-time output

### Trace viewer

**Configuration**:

```
export default defineConfig({
  use: {
    trace: 'on-first-retry', // Capture on failures
  },
});
```

**Manual trace recording**:

```
await context.tracing.start({
  screenshots: true,
  snapshots: true,
  sources: true
});

// Test actions...

await context.tracing.stop({
  path: 'trace.zip'
});
```

**View traces**:

```
npx playwright show-trace trace.zip
```

### VS Code integration

**Setup and features**:

1. Install "Playwright Test for VSCode" extension
2. Features include:
	- **Live Debugging**: Click locators to highlight in browser
		- **Breakpoint Debugging**: Step through tests
		- **Pick Locator Tool**: Generate resilient locators
		- **Test Explorer**: Run/debug individual tests

## 7\. Writing E2E tests with Playwright and Claude Code

### Understanding MCP (Model Context Protocol)

The **Model Context Protocol** enables Claude Code and other AI assistants to interact with Playwright-managed browsers through structured data exchange.

### Playwright MCP usage for writing E2E tests

**Key Components**:

- [**MCP Server**](https://github.com/microsoft/playwright-mcp): Exposes Playwright capabilities to AI tools
- [**Playwright Chrome Extension**](https://github.com/microsoft/playwright-mcp/blob/main/extension/README.md): Allows you to connect to pages in your existing browser and leverage the state of your default user profile
- **Accessibility Tree**: Primary data source for element interaction
- **Page Context**: Provides markup, screenshots, and element hierarchy
- **Agentic Tools**: AI assistants that consume and act on page context

### Requirements for Playwright/MCP Server

**Setup Configuration**:

```
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ]
    }
  }
}
```

[**Essential Tools Provided by MCP**](https://github.com/microsoft/playwright-mcp#tools):

```
// Core automation tools available to Claude Code
- browser_snapshot     // Capture accessibility tree
- browser_navigate     // URL navigation
- browser_click        // Element interaction
- browser_type         // Text input
- browser_screenshot   // Visual capture
- browser_evaluate     // JavaScript execution
```

### Page object models for AI consumption

**AI-optimized POM structure**:

```
class LoginPage {
  metadata = {
      purpose: "Handle user authentication",
      businessLogic: "Standard login with username/password",
      testScenarios: ["valid login", "invalid credentials", "password reset"]
  }

  constructor(page) {
    this.page = page;
  }

  // Action methods that AI tools can call directly
  async navigateToLogin() {
    await this.page.goto('/login');
    await this.page.waitForLoadState('networkidle');
  }

  async enterUsername(username) {
    await this.page.fill(this.selectors.usernameInput, username);
  }

  async enterPassword(password) {
    await this.page.fill(this.selectors.passwordInput, password);
  }

  async clickLoginButton() {
    await this.page.click(this.selectors.loginButton);
  }

  async submitLoginForm(username, password) {
    await this.enterUsername(username);
    await this.enterPassword(password);
    await this.clickLoginButton();
  }

  async verifyLoginSuccess() {
    await this.page.waitForURL('/dashboard');
    return await this.page.isVisible(this.selectors.dashboardHeader);
  }

  async getErrorMessage() {
    return await this.page.textContent(this.selectors.errorMessage);
  }

  // Single reliable selector per element with descriptions
  get selectors() {
    return {
      usernameInput: '[data-testid="login-username"]', // Email or username input field
      passwordInput: '[data-testid="login-password"]', // Password input field
      loginButton: '[data-testid="login-submit"]', // Form submission button
      errorMessage: '[data-testid="login-error"]', // Error message container
      dashboardHeader: '[data-testid="dashboard-header"]', // Success indicator
      forgotPasswordLink: '[data-testid="forgot-password-link"]' // Password reset link
    };
  }
}
```

### Best practices for Claude Code integration

**Key Principles**:

1. **Accessibility-first approach**: Leverage accessibility tree over screenshots
2. **Self-documenting code**: Include rich metadata and descriptions
3. **Natural language interfaces**: Map methods to human-readable scenarios
4. **Error recovery patterns**: Built-in retry and fallback mechanisms
5. **Clear action methods**: Expose granular, callable methods for AI orchestration

## 8\. Testing approaches and anti-patterns to avoid

### Common anti-patterns

**1\. Testing implementation details**

```
// ❌ Wrong - Testing CSS classes
await page.locator('.btn-primary.ng-valid').click();

// ✅ Correct - Testing user-visible behavior
await page.getByRole('button', { name: 'Submit' }).click();
```

**2\. Test interdependencies**

```
// ❌ Wrong - Tests depending on each other
test('login first', async ({ page }) => {
  // Sets global state
});

test('depends on login', async ({ page }) => {
  // Assumes previous test ran
});

// ✅ Correct - Isolated tests
test.beforeEach(async ({ page }) => {
  // Fresh setup for each test
});
```

**3\. Hard Waits**

```
// ❌ Wrong - Fixed timeouts
await page.waitForTimeout(5000);

// ✅ Correct - Web-first assertions
await expect(page.getByText('Success')).toBeVisible();
```

**4\. Testing third-party services**

```
// ❌ Wrong - Testing external payment gateway
await page.click('.stripe-button');

// ✅ Correct - Mock external dependencies
await page.route('**/api/payment', route => route.fulfill({
  status: 200,
  body: JSON.stringify({ success: true })
}));
```

### Authentication patterns

**Global authentication setup**:

```
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';

const authFile = '.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Sign In' }).click();

  await page.context().storageState({ path: authFile });
});

// Use in playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'authenticated',
      use: { storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});
```

Remember that successful E2E testing is not about testing everything, but about testing the right things effectively. Focus on user value, maintain test isolation, use stable locators, and continuously optimize your test suite based on real-world feedback and metrics.

DEV Community

[![Google AI Education track image](https://media2.dev.to/dynamic/image/width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fu09y9fffqrb2one15j3g.png)](https://dev.to/deved/build-apps-with-google-ai-studio?bb=238781)

## Build Apps with Google AI Studio 🧱

This track will guide you through Google AI Studio's new "Build apps with Gemini" feature, where you can turn a simple text prompt into a fully functional, deployed web application in minutes.