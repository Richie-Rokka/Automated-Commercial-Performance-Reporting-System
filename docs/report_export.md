# Automated Commercial Performance Reporting System
## Power Automate Desktop — Runbook & Project Documentation

## 1. Purpose
This project automates routine preparation of the `Automated_Commercial_Performance_Report` in Power BI Desktop. The tested flow refreshes the report, saves the PBIX, and navigates through PDF export. The user retains control of reviewing and saving the exported PDF.

## 2. Confirmed End-to-End Workflow
1. **Launch:** Open Power BI Desktop and the `Automated_Commercial_Performance_Report`.
2. **Wait for readiness:** Allow the report window to load before interacting.
3. **Refresh:** Use the configured **Send mouse click** action at the captured Refresh control coordinates. UI-element selector attempts were unsuccessful.
4. **Wait:** Wait **60 seconds** for the refresh to complete.
5. **Save PBIX:** Send **Ctrl+S** to save the Power BI report.
6. **Post-save wait:** Wait **3 seconds**.
7. **Export:** Use configured mouse clicks to navigate **File → Export → Export to PDF**, with the waits configured in the flow.
8. **Review and save PDF:** Review the PDF and decide whether to save it, correct the report, or discard it. PDF saving is intentionally manual.

## 3. Validated Results
- Fresh-start end-to-end test completed successfully.
- Refresh action was confirmed.
- Flow reached PDF export.
- PDF page fit was adjusted and confirmed correct.
- PBIX save and PDF export workflow were confirmed in the successful test.

## 4. Operating Checklist
- [ ] Confirm the source data and report are in the expected locations.
- [ ] Start the PAD flow from a clean, ready desktop state.
- [ ] Allow the configured refresh wait (30 seconds) to finish.
- [ ] Confirm the PBIX save action completes.
- [ ] Confirm the PDF export dialog/workflow is reached.
- [ ] Review the PDF output before saving it.
- [ ] If corrections are needed, correct the report and rerun as appropriate.

The flow relies on captured mouse coordinates for Refresh and export navigation. Coordinate changes, window position, display scaling, or UI layout changes may require re-capturing and validating those actions.

## 5. Explicitly Out of Scope
- Automatically saving# Automated Commercial Performance Reporting System
## Power Automate Desktop — Runbook & Project Documentation

## 1. Purpose
This project automates routine preparation of the `Automated_Commercial_Performance_Report` in Power BI Desktop. The PAD flow refreshes the report, saves the PBIX, and navigates through PDF export. The user retains control of reviewing and saving the exported PDF.

## 2. Confirmed End-to-End Workflow
1. **Run application:** Launch Power BI Desktop and open the `Automated_Commercial_Performance_Report` PBIX.
2. **Wait for window:** Wait for the report window to open.
3. **Refresh:** Use the configured **Send mouse click** action at the captured Refresh control coordinates.
4. **Wait:** Wait **30 seconds** for refresh processing. This was reduced from 60 seconds to shorten the run.
5. **Save PBIX:** Send **Ctrl+S** to save the Power BI report.
6. **Post-save wait:** Wait **3 seconds**.
7. **Export navigation:** Use configured mouse clicks and waits to navigate through **File → Export → Export to PDF**.
8. **Final action:** Action 12 is the final action in the current flow.
9. **Review and save PDF:** Review the PDF and decide whether to save it, correct the report, or discard it. PDF saving is intentionally manual.

## 3. Validated Results
- Fresh-start end-to-end test completed successfully.
- Refresh action was confirmed.
- Flow reached PDF export.
- PDF page fit was adjusted and confirmed correct.
- Action 12 is the final action in the current PAD flow.
- The cyclic-reference issue has been resolved.

## 4. Operating Checklist
- [ ] Confirm the source data and report are in the expected locations.
- [ ] Start the PAD flow from a clean, ready desktop state.
- [ ] Allow the configured 30-second refresh wait to finish; verify refresh completion in Power BI.
- [ ] Confirm the PBIX save action completes.
- [ ] Confirm the PDF export workflow is reached.
- [ ] Review the PDF output before saving it.
- [ ] If corrections are needed, correct the report and rerun as appropriate.

## 5. Known Behavior and Limitations
The current flow uses captured screen-coordinate mouse clicks for Refresh and export navigation. Changes to window position, display scaling, or UI layout may require re-capturing and validating those actions.

The 30-second refresh wait is the current configured delay, not a guarantee that every refresh will finish within that time. Verify refresh completion before relying on the exported report.

## 6. Explicitly Out of Scope
- Automatically saving the PDF without user review.
- Automatically publishing or distributing the report.
- Automatically correcting data, report logic, or layout.

## 7. Configuration Notes
- **Refresh wait:** 30 seconds (reduced from 60 seconds to shorten runtime).
- **Wait after Ctrl+S:** 3 seconds.
- **Refresh/export interaction method:** captured screen-coordinate mouse clicks.
- **Current flow ends at action 12.**
- **PDF review and save decision:** manual.
 the PDF without user review.
- Automatically publishing or distributing the report.
- Automatically correcting data, report logic, or layout.

## 6. Configuration Notes
- **Refresh wait:** 60 seconds.
- **Wait after Ctrl+S:** 3 seconds.
- **Refresh/export interaction method:** captured screen-coordinate mouse clicks.
- **PDF review and save decision:** manual.
