# Python by Building: code

All the code from **Python by Building: A Project-Based Learning Approach** by Ronald Allan V. Tomimbang:
33 chapters, 33 chapter projects, 12 capstone projects and the selected exercise solutions.
Everything runs on Python 3.12 or newer, in VS Code, PyCharm, Jupyter/Colab or IDLE/Thonny.

## How the repository is organised

- `chNN/` holds one chapter. The chapter's project and any complete programs sit at the top of the folder,
  named as in the book. Shorter examples are in `chNN/snippets/`, numbered by section
  (`04-the-for-loop_2.py` is the second example in section 4). Files ending in `_repl.txt` are typed
  into the interactive `>>>` shell, `.sh` files are terminal commands, and `_output.txt` files show
  what a program printed when the book was written.
- `capstones/` holds the twelve Part V projects, one folder each.
- `solutions/` holds the exercise solutions from Appendix C, named `chNN_exM_topic.py`.
- `appendix-b/quick_reference.py` is the Python quick reference.

## Getting started

```bash
git clone https://github.com/<your-account>/python-by-building.git
cd python-by-building
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python ch01/hello.py
```

Run each program from its own folder (`cd ch11 && python sales_report.py`), because many projects read and
write data files next to the script. `requirements.txt` installs every third-party library used in the book;
the early chapters need none of them.

## Chapters and their projects

| Ch | Topic | Real-world project | Main file |
|---:|---|---|---|
| [1](./ch01) | Installing Python and Choosing Your IDE | System info reporter | [`sysinfo.py`](./ch01/sysinfo.py) |
| [2](./ch02) | Variables, Types and Input/Output | Loan and amortization calculator | [`loan.py`](./ch02/loan.py) |
| [3](./ch03) | Making Decisions and Repeating Work | Number-guessing game with statistics | [`guess.py`](./ch03/guess.py) |
| [4](./ch04) | Lists, Tuples, Dictionaries and Sets | Inventory manager | [`inventory.py`](./ch04/inventory.py) |
| [5](./ch05) | Functions and Modules | Payroll calculator module | [`payroll.py`](./ch05/payroll.py) |
| [6](./ch06) | Strings and Text Processing | Log analyzer for web server access logs | [`log_analyzer.py`](./ch06/log_analyzer.py) |
| [7](./ch07) | Files, Paths, CSV and JSON | Expense tracker with CSV storage and monthly summary | [`expenses.py`](./ch07/expenses.py) |
| [8](./ch08) | Errors, Debugging and Testing | A robust bank account module with tests | [`bank.py`](./ch08/bank.py) |
| [9](./ch09) | Object-Oriented Programming | Library management system | [`library.py`](./ch09/library.py) |
| [10](./ch10) | Virtual Environments, pip and the Standard Library | Secure password generator CLI | [`passgen.py`](./ch10/passgen.py) |
| [11](./ch11) | Data Analysis with pandas | Sales performance report | [`sales_report.py`](./ch11/sales_report.py) |
| [12](./ch12) | Graphs and Visualization with matplotlib | Loan amortization graph | [`loan_chart.py`](./ch12/loan_chart.py) |
| [13](./ch13) | Automation and Sysadmin Scripting | Server health monitor with alerts and CSV history | [`healthcheck.py`](./ch13/healthcheck.py) |
| [14](./ch14) | Web Requests, APIs and Scraping | 7-day weather report from a free API | [`weather.py`](./ch14/weather.py) |
| [15](./ch15) | Web Apps with Flask | Team task board web app | [`app.py`](./ch15/app.py) |
| [16](./ch16) | Databases with SQLite | IT helpdesk ticket system | [`helpdesk.py`](./ch16/helpdesk.py) |
| [17](./ch17) | Desktop GUIs with Tkinter | Contact book with search, backed by SQLite | [`contacts.py`](./ch17/contacts.py) |
| [18](./ch18) | Games with pygame | Star Catcher, a complete arcade game | [`star_catcher.py`](./ch18/star_catcher.py) |
| [19](./ch19) | Automating Excel, Word and PDF Files | Certificate mail-merge from Excel to Word and PDF | [`certificates.py`](./ch19/certificates.py) |
| [20](./ch20) | Version Control with Git and GitHub | Git history reporter | [`git_report.py`](./ch20/git_report.py) |
| [21](./ch21) | Concurrency: Threads, Processes and asyncio | Concurrent website uptime checker | [`uptime.py`](./ch21/uptime.py) |
| [22](./ch22) | Fast Numerical Computing with NumPy | Monte Carlo schedule risk | [`risk.py`](./ch22/risk.py) |
| [23](./ch23) | Modern APIs with FastAPI | Typed expense API | [`expense_api.py`](./ch23/expense_api.py) |
| [24](./ch24) | Packaging, Quality and Deployment | Installable password generator package (passgen-tool) | [`passgen-tool/`](./ch24/passgen-tool) |
| [25](./ch25) | Machine Learning Basics with scikit-learn | Learning a server's normal behaviour | [`ml_metrics.py`](./ch25/ml_metrics.py) |
| [26](./ch26) | Testing in Depth | A test suite for two earlier projects | [`test_syncbackup.py`](./ch26/test_syncbackup.py) |
| [27](./ch27) | Browser Automation with Playwright | Website health and screenshot checker | [`pagecheck.py`](./ch27/pagecheck.py) |
| [28](./ch28) | Interactive Dashboards with Streamlit | Sales dashboard | [`dashboard.py`](./ch28/dashboard.py) |
| [29](./ch29) | Automating Email and Chat | Daily server report by email | [`daily_report.py`](./ch29/daily_report.py) |
| [30](./ch30) | Security Essentials for Python Developers | A security scanner for Python code | [`secscan.py`](./ch30/secscan.py) |
| [31](./ch31) | Automating Servers with Ansible and Python | A fleet health check with a report | [`fleet.py`](./ch31/fleet.py) |
| [32](./ch32) | Vulnerability Checking with Python | A dependency vulnerability checker | [`vulncheck.py`](./ch32/vulncheck.py) |
| [33](./ch33) | Building AI Agents with Python | An IT helpdesk agent | [`opsagent.py`](./ch33/opsagent.py) |

## Capstone projects

| # | Project | Files |
|---:|---|---|
| 1 | [Personal finance dashboard](./capstones/01-personal-finance-dashboard) | `finance_dashboard.py` |
| 2 | [Branch sales Excel consolidator](./capstones/02-branch-sales-excel-consolidator) | `excel_consolidate.py` |
| 3 | [Server metrics report with anomaly detection](./capstones/03-server-metrics-report-with-anomaly) | `metrics_report.py` |
| 4 | [SSH brute-force detector](./capstones/04-ssh-brute-force-detector) | `ssh_guard.py` |
| 5 | [Incremental backup with hash verification](./capstones/05-incremental-backup-with-hash) | `syncbackup.py` |
| 6 | [Network inventory scanner](./capstones/06-network-inventory-scanner) | `netscan.py` |
| 7 | [Price tracker with history and alerts](./capstones/07-price-tracker-with-history-and-alerts) | `price_tracker.py` |
| 8 | [Inventory REST API with a Python client](./capstones/08-inventory-rest-api-with-a-python-client) | `inventory_api.py`, `inventory_client.py` |
| 9 | [URL shortener web app](./capstones/09-url-shortener-web-app) | `shortener.py` |
| 10 | [Student grade manager (desktop app)](./capstones/10-student-grade-manager-desktop-app) | `gradebook.py` |
| 11 | [Typing speed trainer (desktop app)](./capstones/11-typing-speed-trainer-desktop-app) | `typing_trainer.py` |
| 12 | [Encrypted password vault](./capstones/12-encrypted-password-vault) | `vault.py` |

## Notes for some chapters

- **Chapter 15**: the hello-world app is in `ch15/hello/`; the task board project is `ch15/app.py` with its
  `templates/` and `static/` folders.
- **Chapter 24**: `passgen-tool/` is a complete installable package (`pip install -e ch24/passgen-tool`). Its
  GitHub Actions workflow is in `passgen-tool/.github/workflows/`, so it runs only if you make that folder
  its own repository. `expense-api/` holds the Dockerfile and systemd unit for the Chapter 23 API.
- **Chapter 26** tests the Capstone 5 backup tool; a copy of `syncbackup.py` is included so the tests run
  on their own (`cd ch26 && pytest`).
- **Chapter 27**: `site/` is the small local test site. Serve it with `python -m http.server 8099 --directory site`.
  Install the browser once with `playwright install chromium`.
- **Chapter 28** reads `orders.csv` from Chapter 11. Create it with `python ch11/sales_report.py` and copy
  `orders.csv` into `ch28/`.
- **Chapter 29** reads `health_history.csv`, written by the Chapter 13 health monitor or Capstone 3.
- **Chapter 30**: `sample/app.py` is **deliberately insecure** test code for the scanner. Never deploy it.
- **Chapter 31** needs Linux, macOS or WSL (`pip install ansible-core ansible-runner`). The lab inventory
  `cmdb.csv` uses local connections, so you can try everything on one machine.
- **Chapter 32**: `osv_sample.json` holds three real OSV advisories for offline runs; drop `--db` to ask the live
  OSV database. `requirements_2023.txt` is the deliberately outdated test project.
- **Chapter 33**: `python opsagent.py --demo "..."` needs no API key. For the real model, set
  `ANTHROPIC_API_KEY` (never commit it). `lab/` holds the runbooks, log and monitoring snapshot.

## Tests

```bash
cd ch08 && pytest            # also: ch23, ch24/passgen-tool, ch26, ch28, ch32, ch33, capstones/10-*
```

## Safety

Several projects touch real systems: file clean-up, backups, network scans, emails, service restarts.
Try them on test folders and your own machines first, and only scan networks and sites you are allowed to.

---
354 files, extracted directly from the book's listings.
