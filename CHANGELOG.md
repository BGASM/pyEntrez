# Version history

We follow [Semantic Versions](https://semver.org/).

## Version 0.1.1
- New feature allows for slower database operations, such as when interacting with a remote DB, to 
  take place asynchronously.
- Plays nice with remote MongoDB. Dev-release has test DB set in the default user config file, on 
  release these will be blanked.
- Doucmentation efforts underway.



## Version 0.1.0

- Initial release
- User may select running in TUI-mode or interactive prompt mode 
- Prototype screens for Fetch, Settings, and Review behave with each other
- Basic entrez features: search a query, retrieve UID list, populate DB with article information
- Plays nice with a local MongoDB
- Configure application setting requirements with the variables module, new settings will be adopted
  and available through Envars (although not automatically added to config file...yet)
- If using a local MongoDB article info can be stored and abstracts can be loaded into review screen


