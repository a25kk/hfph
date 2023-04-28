# Upgrade Plone 5.2 Python3

1. Sync Live DB nach Python2.7 Staging
2. Plone Migration -> 5.2.8
3. Upgrade Extensions via control panel
4. ZMI: Run full uninstall for ATCT in **portal_setup**
5. ZMI: Delete **portal_languages**
6. Sync Data.fs to Python3 Staging
7. Run zodbupgrade script
```python
bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding utf8 --encoding-fallback latin1
```
8. Start instance and reindex catalog
9. Run hph.policy upgrade step
10. Run `plone.app.contenttypes` import profile in **portal_setup**
11. Rename `plone.app.events` Event to *DX Event*  to fix content views