# TODO - Admin Meals Import hardening + testing

- [x] Read and isolate `/admin/meals/template` implementation in `app.py`
- [x] Remove second worksheet creation (`Import 7 ngày`)
- [x] Keep single-sheet structure compatible with `/admin/meals/import`
- [x] Verify no dependent import logic requires second sheet
- [x] Update import date parsing: drop overflow days (e.g. 34, 35...) and only keep valid dates in that month

- [ ] Update logic: empty date rows should be skipped (no auto-fill)
- [ ] Add strict single-month import rule (rows outside target month are skipped)
- [ ] Keep one-row mapping: 1 normal meal + 1 special meal per valid date

- [ ] Run critical-path test for import
- [ ] Run thorough tests (UI/API/edge cases)
- [ ] Summarize findings and improvements
