# CV, SOP and Project Twilight implementation — 2 November 2026

Base: remote `main` at `c65da598eba41cf635d953f2c519225c3787e795`. New branch: `improve/cv-sops-twilight-progress-nov-2026`. Initial worktree was clean; latest owner CV wording is preserved. No changes to main, Pages settings or the live deployment.

The standalone and packaged implementation specifications were compared byte-for-byte and are identical. ZIP instructions, proposed copy, original SOP statement, full project journal and both workbook sheets were inspected directly in memory. No archive files were extracted into public paths. UAS facts use only the supplied journal/workbook and explicitly approved compute-access statement; no external aircraft assumptions or results were added.

## Implementation commits and files

- `cc3de43`: detailed procurement/SOP evidence, Nando's, A-levels and scoped Twilight progress; meaningful replacement for the superseded UAS immutability test.
- `3127a2c`: regenerated both tailored PDFs; source-to-PDF text, page-count and clickable-link validation; tool instructions updated.
- Final documentation commit: see branch history / PR; this report is committed with that verification step.

Modified: `cv.html`, `projects/uas.html`, `projects.html`, `tools/cv-content.json`, `tools/check_site.py`, `tools/README.md`, `assets/documents/Linus_Adzanku-resume.pdf`, `assets/documents/Linus_Adzanku-procurement-CV.pdf`.

Added: `tools/check_cvs.py` and this report. No new deletions. The aircraft-design page remains absent, with no internal route to it.

Homepage, all CSS/JS, compact case studies, full technical reports, existing engineering media and the PDF generator are unchanged from the baseline. The six-section online CV order and public URLs remain intact. No framework or website dependency was introduced.

## Before / after and claims

| Area | Before | After |
| --- | --- | --- |
| Junior Buyer | Generic tender support and documentation | Defined ATS sourcing/evaluation leadership with Talent Acquisition; digital-signage sourcing and purchasing administration; general-building-services requirements/tender/rate-card work; speed-gates coordination; recruitment-expenditure analysis; utility-validation sourcing; contractor information and Oracle Fusion processes |
| SOPs | Generic process-documentation language | Prominent first web/procurement-PDF bullet: authored procurement-wide SOPs from existing workflows, capturing tacit knowledge in maintainable documentation; onboarding, version-control and continuity benefits explicitly described as intentions |
| Procurement Intern | General RFP/data administration | Supplier-agreement/performance review, initial water-cooler-services RFP leadership, Excel charts/pivot tables/comparisons; June–August 2024, ten weeks |
| Additional employment | Missing | Back-of-House Team Member (Griller), Nando's, Bristol, September 2023–August 2026; concurrent work/study and service teamwork, no award claim |
| Education | MEng only | MEng Merit retained; CAIE A-levels at Courtney House Learning Centre, Pretoria, South Africa, 2019–2020: Physics A, Chemistry B, Mathematics B |
| UAS | Generic placeholder and broad future scope | Short progress record, initial September CAD, preliminary sizing targets and clearly planned CFD/manufacturing/testing |

The SOP wording does not claim adoption, operating version controls, reduced onboarding time, measured retention, compliance certification or realised savings. No monetary values, vendor/contract counts, private supplier details, unsupported credentials or award authority were published. The approved email remains `linus.adzankuu@gmail.com` throughout. Earlier owner edits removing tangential online-CV wording and calibrating programming claims are preserved; the engineering PDF programming summary was brought into line with the current web CV.

## Published UAS progress paragraphs (verbatim)

> Project Twilight is a personal fixed-wing unmanned aircraft project intended for cartography and surveying. Development is currently centred on requirements, preliminary sizing and conceptual aircraft design. The configuration being explored uses a straight, unswept high wing, a conventional fuselage and tail, and propellers mounted beneath the wings. An initial CAD model was developed in September 2026 to visualise the arrangement and guide subsequent aerodynamic work.

> A working sizing spreadsheet is being used to explore mission requirements and aerodynamic assumptions. Current preliminary targets are a cruise speed of 15.65 m/s, a maximum speed of 20 m/s, a mission duration of 30–60 minutes and a planned operating-altitude ceiling of 120 m. These are design inputs and objectives, not demonstrated aircraft performance. Estimates of lift-to-drag ratio, battery energy and system efficiency remain provisional as the design is refined.

> The initial approach is to develop the aeromechanical design around off-the-shelf electronics, with 3D printing under consideration for affordable prototyping. Zenotech has provided access to computational resources to support planned CFD investigations as the geometry matures. Detailed aerodynamic validation, final propulsion selection, manufacture and flight testing remain future work.

The page retains its title orientation, historical URL and shared design, with static skip/fallback access and three modest section headings. Its listing and CV blurb now describe initial CAD/preliminary sizing with validation still planned. No source files, new renders, plots or external project links were published.

## UAS evidence decisions

| Item | Treatment and reason |
| --- | --- |
| Cruise / maximum speed | 15.65 / 20 m/s retained as current preliminary targets from Master B20/B21; superseded journal speeds omitted |
| Mission duration | 30–60 minutes retained as intended range from Master B23/B24, not achieved endurance |
| Altitude | 120 m retained as a planned operating ceiling from Master B22; no regulatory-compliance claim |
| Initial geometry | Straight unswept high wing, conventional fuselage/tail and under-wing propellers; initial September 2026 CAD visualisation, not completed design or built hardware |
| Electronics / prototyping | Off-the-shelf electronics intended; 3D printing under consideration, not a manufacturing accomplishment |
| Camera/payload | Exact count and payload mass omitted: September journal requests two cameras; workbook requirement at Master A11 refers to one camera and preliminary payload estimates. The handover's A10 pointer is the requirements header, not the camera cell; source content was checked directly |
| Take-off mass | Omitted: historical 20/15 kg and contemplated 5 kg options do not establish a final MTOW |
| Battery / L/D / efficiency | Numerical assumptions and calculated drag/battery outputs omitted from short copy; described only as provisional model inputs. Workbook stall/sizing sections are incomplete and cannot support validated performance |
| Propulsion and CFD | No final motor selection, completed CFD, convergence, flight, manufacture or validated performance claimed |
| Zenotech | Exact published wording: “Zenotech has provided access to computational resources to support planned CFD investigations as the geometry matures.” No sponsorship, endorsement, funding or partnership claim |

Owner decisions left open: reconcile camera/payload configuration and final take-off mass before publishing either as settled. These do not block the present progress update.

## PDF quality and scope

Both stable PDF URLs were retained. Engineering: **two tagged A4 pages**, 10 pt body text; CFD/aeroacoustics and rocket evidence remain primary on page one, with concise procurement/SOP coverage and the added employment/education on page two. Procurement: **two tagged A4 pages**, same readable body size; sourcing leadership and the SOP example receive substantive space.

The first engineering draft spilled onto a third page. Condensing secondary project content resolved this without reducing type size or changing the generator. The secondary turboprop paragraph was omitted from the engineering PDF, consistent with its removal from the owner's web CV; primary technical-project content remains. Procurement deliberately expanded from one page to two for the new evidence, rather than compressing it.

All four final pages were rendered with Poppler and visually reviewed. Extracted text was checked against every canonical source paragraph/bullet/title. Six engineering and four procurement clickable URLs were checked, including their local portfolio targets. Both download routes return HTTP 200 with PDF signatures on the local server. No PDF content, layout or link mismatch remains.

## Verification actually executed

| Check | Status and evidence |
| --- | --- |
| `python3 tools/check_site.py` | PASS: eight nonempty HTML pages parsed; 167 relative references; unchanged six CV headings, four homepage sections, project order, overview lengths and aircraft deletion protections |
| Updated UAS protection | PASS: current target values/initial CAD/provisional status/compute-access statement/future-work boundaries and short scope checked; old immutable blob guard narrowly replaced; unrelated safeguards retained |
| Source privacy | PASS: no tracked/unignored original handover or source paths; no public links to private evidence; current Markdown and ZIP ignored. Original journal/workbook/SOP byte hashes compared against tracked/unignored files: no matches |
| `python3 tools/check_cvs.py` | PASS: both two-page tagged A4 PDFs, all canonical text, approved email and clickable URL targets. Normalisation accommodates Poppler joining lexical hyphens at line wraps |
| `git diff --check` | PASS |
| Browser regression | PASS: Playwright 1.64.1 / Chromium 156.0.8078.4, Linux headless; localhost port 8767; eight pages × 320/375/390/768/1440 px = 40 combinations. No horizontal overflow, failed page resources or new JS errors |
| Keyboard and interaction | PASS: visible skip/focus, five shared nav routes, Contact from root/nested pages, UAS/report TOC Enter/Escape and heading focus, no TOC on compact overviews, rocket-model arrow input and reset |
| Additional browser checks | PASS: updated CV/UAS full-page screenshots at 390/1440 px, UAS JavaScript-disabled fallback, local PDF downloads, safe external-link attributes on CV |
| Baseline scope comparison | PASS: homepage, CSS, JS, full/compact case studies and generator byte-identical to c65da59 |
| Performance / video playback | NOT RERUN in this scope; no new performance claims and no media/code changes |
| Physical devices / Firefox / Safari / screen reader | NOT RUN; viewport emulation is not physical-device or assistive-technology coverage |
| Merge/deployment | NOT RUN / NOT AUTHORISED |

Screenshots, rendered PDF pages and browser results are retained locally under the ignored handover directory. Temporary browser tooling was installed outside the published repository. No raw journal/workbook/SOP statements are included in public assets or in this report; only the approved editorial update and source-decision summary are present.

The branch is ready for owner review. The narrow UAS approval supersedes the previous byte-for-byte restriction only for this sourced update. Further results, final payload/mass or broader UAS changes require new evidence and authorisation. **NOT MERGED / NOT DEPLOYED.**
